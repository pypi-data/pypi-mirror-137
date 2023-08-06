# PyComuneFirenze

Utility di uso **interno** al Comune di Firenze per semplificare e aggregare ad uso comune diverse operazioni, come:

- logging
- creare e cancellare cartelle di lavoro
- inserire dati su database
- mandare email


# Installazione
È altamente consigliato installare i proprio pacchetti/librerie tramite virtual environment:

	python -m venv *nome_del_virtual_environment*
	
	cd *nome_del_virtual_environment*/Scripts/activate
		
    pip install pycomunefirenze

# Breve guida all'uso
Importazione del modulo

    from pycomunefirenze import cdf
Per utilizzare le funzioni di logging integrate, inizializzare un logger **generale**, per esempio:

    import logging
    logging.basicConfig(filename='file.log',
					    filemode='a',
					    level=logging.INFO,
                        format='%(asctime)s - CHANGEME - %(levelname)s - %(message)s'
                        )
    logger = logging.getLogger(__name__)
E poi utilizzare il metodo `logging` normalmente
    
    logging.info("log messages go here")

### Interrogazione di API

    response_text = general_request('metodo', 'url', **kwargs)
Per eventuali argomenti extra si riferimento alla documentazione di [requests](https://docs.python-requests.org/en/latest/).

### Creazione directory di lavoro

    wd = cdf.create_directory('directory_a')
### Cancellazione di directory di lavoro

    cdf.delete_directory(wd)


### Inserimento di righe su db

    cdf.insert_on_db(
	    'user'
	    'password'
	    'example.intranet'
	    '5432',
	    'database',
	    'table_name',
	    {
		    'col1': 'data',
		    'col2': 42
		},
	    truncate = False)

È possibile passare come parametro `truncate` per far sì che la tabella venga prima svuotata e poi popolata. Il default è `False`.

### Mandare email

    cdf.send_email(
	    'oggetto', 
	    'mittente', 
	    [
		    'destinatario1@example.org',
		    'destinatario2@example.org'
		],
		'testo della mail', 
		**kwargs
    )
Per eventuali argomenti extra come `cc`, `bcc` etc..., si fa riferimento alla documentazione di [RedMail](https://pypi.org/project/redmail/).