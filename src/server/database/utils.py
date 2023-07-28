from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = f"https://ptt-app-stage.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

HOST = client.get_secret('SERVICE-DB-HOST').value
USERNAME = client.get_secret('SERVICE-DB-USERNAME').value
PASSWORD = client.get_secret('SERVICE-DB-PWD').value
DBNAME = client.get_secret('SERVICE-DB-NAME').value

pgconfig = {'pguser':USERNAME,
            'pgpasswd':PASSWORD,
            'pghost':HOST,
            'pgport':5432,
            'pgdb':DBNAME}

def get_engine(user, passwd, host, port, db) :
    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'

    engine = create_engine(url, pool_size=50, echo=False)
    return engine

def get_engine_from_pgconfig():
    keys = {'pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb'}
    if not all( key in keys for key in pgconfig ):
        raise Exception('Bad Config file')
    
    return get_engine(pgconfig['pguser'], pgconfig['pgpasswd'], pgconfig['pghost'], pgconfig['pgport'], pgconfig['pgdb'])

def get_session():
    engine = get_engine_from_pgconfig()
    session = sessionmaker(bind=engine)

    return session()

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
