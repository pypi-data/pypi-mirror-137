import requests
from requests import HTTPError, RequestException
import logging
import os
import shutil


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

def create_directory(directory_name: str) -> str:
    """Crea la directory richiesta nella cartella di lavoro dello script

    Args:
        directory_name (str): Il nome della directory da creare

    Returns:
        path: Il path della directory creata
    """
    working_path = os.path.realpath(__name__)
    path = os.path.join(working_path, directory_name)
    os.mkdir(path)
    return path

def delete_directory(directory_name: str) -> None:
    """Cancella una directory ed il suo contenuto ricorsivamente, ignorando tutti gli errori

    Args:
        directory_name (str): Il nome della directory da cancellare
    """
    working_path = os.path.realpath(__name__)
    path = os.path.join(working_path, directory_name)
    shutil.rmtree(path, ignore_errors=True)


