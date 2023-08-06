from typing import Any, Dict, List
import requests
from requests import HTTPError, RequestException
import logging
import os
import shutil
from pathlib import Path
import psycopg2
import sys
from redmail import EmailSender

try:
    from pycomunefirenze.working_dir import WorkingDir
except ModuleNotFoundError:
    from working_dir import WorkingDir

proxies = {
    "http": "http://proxyhttp.comune.intranet:8080",
    "https": "http://proxyhttp.comune.intranet:8080",
}


def general_request(method: str, url: str, **kwargs) -> str:
    """Esegue una richiesta custom ad un url, utilizzando il metodo request

    Args:
        method (str): metodo (POST, GET, etc...)
        url (str): url da interrogare

    Raises:
        ConnectionError: Errore di rete
        HTTPError: Errore di protocollo HTTP (401, 404, 500, etc...)
        TimeoutError: Errore di timeout
        RequestException: Errore generale

    Returns:
        str: contenuto della risposta
    """
    try:
        r = requests.request(method, url, proxies=proxies, **kwargs)
        r.raise_for_status()
        logging.info("API called")
        return r.text
    except ConnectionError as exc:
        error_type = str(exc)
        raise Exception("Netowork error (DNS, refused connection, etc)")
    except HTTPError as exc:
        error_type = str(exc)
        raise Exception(f"{r.status_code} {r.reason}")
    except TimeoutError as exc:
        error_type = str(exc)
        raise Exception("Timeout error from API")
    except RequestException as exc:
        error_type = str(exc)
        raise Exception("General error in getting data from API")


def create_directory(directory_name: str) -> WorkingDir:
    """Crea la directory richiesta nella cartella di lavoro dello script

    Args:
        directory_name (str): Il nome della directory da creare

    Returns:
        path: Il path della directory creata
    """
    if directory_name is None or not directory_name:
        logging.error("Attempted to create directory with no name")
        sys.exit(1)
    path = Path(rf"{directory_name}")
    logging.info(f"Trying to create {path}")
    os.mkdir(path)
    logging.info(f"Created {path}")
    return WorkingDir(directory_name)


def delete_directory(directory: WorkingDir) -> bool:
    """Cancella una directory precedentemente creata ed il suo contenuto

    Args:
        directory (WorkingDir): La directory di lavoro precedentemente creata
    """
    if not isinstance(directory, WorkingDir):
        logging.error(
            f"Trying to delete a directory that is NOT a previosly created working directory"
        )
        raise ValueError("Can't delete not WorkingDir directory")
    logging.info(f"Trying to delete {directory.path}")
    shutil.rmtree(directory.path, ignore_errors=True)
    logging.info(f"Deleted {directory.path}")
    return True


def __create_sql_query(table_name, data: Dict[str, Any]) -> str:
    """Metodo private, che crea una query sql del tipo 'INSERT INTO [table_name] (col1, col2, etc...) VALUES (%(col1)s, %(col2)s, etc..)

    Args:
        table_name (str): nome della tabella in cui inserire i dati
        data (Dict[str,Any]): dizionario contenente i dati da inserire in tabella

    Returns:
        str: query
    """
    if not isinstance(table_name, str):
        raise ValueError(
            f"The name of the table must be a string, and {table_name} is a {type(table_name)}"
        )
    columns_comma = ",".join(data.keys())
    columns = f"({columns_comma})"
    values_comma = ")s, %(".join(data.keys())
    values = f"({values_comma})"
    return f"INSERT INTO {table_name} {columns} VALUES (%{values}s)"


def insert_on_db(
    user: str,
    password: str,
    host: str,
    port: str,
    database: str,
    table_name: str,
    data: Dict[str, Any],
    truncate = False
) -> bool:
    """Genera la connessione al db PGSQL specificato ed esegue la query

    Args:
        user (str): username
        password (str): password
        host (str): hostname
        port (str): porta
        database (str): database
        table_name (str): nome della tabella in cui inserire i dati
        data (Dict[str,Any]): dizionario contenente i dati da inserire in tabella

    Returns:
        boolean: controllo per verificare se la scrittura è andata a buon fine o no
    """
    connection = None
    try:
        connection = psycopg2.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        logging.info(f"Connected to {database} on {host}")
        cursor = connection.cursor()
        if truncate:
            cursor.execute('TRUNCATE %s', (table_name,))
        cursor.execute(__create_sql_query(table_name, data), data)
        connection.commit()
        logging.info(f"Queries executed")
    except Exception as error:
        logging.error(error)
        return False
    finally:
        if connection is not None:
            connection.close()
    return True


def send_email(
    subject: str, sender: str, receivers: List[str], text: str, **kwargs
) -> Any:
    """Manda una mail utilizzando il server mail interno

    Args:
        subject (str): oggetto della mail
        sender (str): mittende
        receivers (List[str]): lista di destinatari
        text (str): testo della mail
        **kwargs: argomenti opzionali, vedi https://pypi.org/project/redmail/

    Returns:
        EmailMessage: [description]
    """
    email = EmailSender(host="mailint.comune.intranet", port=25)
    return email.send(
        subject=subject, sender=sender, receivers=receivers, text=text, **kwargs
    )
