from typing import Any, List
import requests
from requests import HTTPError, RequestException
import logging
import os
import shutil
from working_dir import WorkingDir
from pathlib import Path
import psycopg2
import sys

proxies = {
    'http': 'http://proxyhttp.comune.intranet:8080',
    'https': 'http://proxyhttp.comune.intranet:8080',
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
        logging.error('Attempted to create directory with no name')
        sys.exit(1)
    path = Path(rf'{directory_name}')
    logging.info(f'Trying to create {path}')
    os.mkdir(path)
    logging.info(f'Created {path}')
    return WorkingDir(directory_name)


def delete_directory(directory: WorkingDir) -> bool:
    """Cancella una directory precedentemente creata ed il suo contenuto

    Args:
        directory (WorkingDir): La directory di lavoro precedentemente creata
    """
    if not isinstance(directory, WorkingDir):
        logging.error(
            f'Trying to delete a directory that is NOT a previosly created working directory')
        raise ValueError('Can\'t delete not WorkingDir directory')
    logging.info(f'Trying to delete {directory.path}')
    shutil.rmtree(directory.path, ignore_errors=True)
    logging.info(f'Deleted {directory.path}')
    return True


def __create_sql_query(table_name: str, column_names: List[str]) -> str:
    """Metodo private, che crea una query sql del tipo 'INSERT INTO [table_name] (col1, col2, etc...) VALUES (%s, %s, etc..)

    Args:
        table_name (str): nome della tabella in cui inserire i dati
        column_names (List[str]): lista dei nomi delle colonne

    Returns:
        str: query
    """
    if not isinstance(table_name, str):
        raise ValueError(f'The name of the table must be a string, and {table_name} is a {type(table_name)}')
    columns_declaration = "("
    values_declaration = "("
    for idx, column in enumerate(column_names):
        if not isinstance(column, str):
            raise ValueError((f'The name of each column must be a string, and {column} is a {type(column)}'))
        columns_declaration += f"{column}"
        values_declaration += f"%s"
        if idx != len(column_names)-1:
            columns_declaration += ", "
            values_declaration += f", "
        else:
            columns_declaration += ")"
            values_declaration += f")"
    return f"INSERT INTO {table_name} {columns_declaration} VALUES {values_declaration}"


def insert_on_db(user: str, password: str, host: str, port: str, database: str, table_name: str, column_names: List[str], rows: List[List[Any]]) -> bool:
    """Genera la connessione al db PGSQL specificato ed esegue la query

    Args:
        user (str): username
        password (str): password
        host (str): hostname
        port (str): porta
        database (str): database
        table_name (str): nome della tabella in cui inserire i dati
        column_names (List[str]): lista dei nomi delle colonne
        rows (List[List[Any]]): lista di righe sottoforma di tuple

    Returns:
        cursor: oggetto per effettuare query su db
    """
    # todo far scrivere la insert in automatico passando nome tabella e nome colonne
    connection = None
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        logging.info(f'Connected to {database} on {host}')
        cursor = connection.cursor()
        for row in rows:
            cursor.execute(__create_sql_query(table_name, column_names), row)
        connection.commit()
        logging.info(f'Queries executed')
    except Exception as error:
        logging.error(error)
        return False
    finally:
        if connection is not None:
            connection.close()
    return True
