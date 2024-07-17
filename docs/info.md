## Ambient virtual

```bash
python3 -m venv venv # Crea un nou ambient virtual
source venv/bin/activate # activar
which python # verifica que està activat, comprovant la adreça del intèrpret
deactivate # desactiva el ambient virtual
```

## Instal·lar fastapi

```bash
source venv/bin/activate # activar el ambient virtual
pip install fastapi # instal·la fastapi en el venv
pip freeze > requirements.txt # crear fitxer de dependències
```

## Provar el funcionament

- crear el fitxer main.js en el directori app
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def read_root():
    return {"Hello": "World"}
```

- executar en mode de desenvolupament
```bash
fastapi dev ./app/main.py # executar amb uvicorn i auto-recàrrega
```

- obrir el navegador y provar la adreça http://localhost:8000/health

- Parar la execució pulsant ctrl+c

## Mòdul de autenticació

- Crear el directori "auth" dins de app

```bash
pip install "passlib[bcrypt]"
```


## Migracions

- Install alembic

```
pip install alembic
```

- Configurar alembic: obrir el fitxer alembic/env.py i afegir:

```py
from app import settings
from app.auth.persistence.entities import Base as AuthBase
DB_USERNAME = settings.agila_db_username
DB_PASSWORD = settings.agila_db_password
DB_HOSTNAME = settings.agila_db_hostname
DB_PORT = settings.agila_db_port
DB_DATABASE = settings.agila_db_name
DB_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
config = context.config
config.set_main_option("sqlalchemy.url", DB_URL)
target_metadata = [AuthBase.metadata]
```

- Crear el fitxer de la migració

```bash
alembic revision --autogenerate -m "create users table"
```

- Executar la migració

```bash
alembic upgrade head
```

## Tests

- Instal·lar pytest

```bash
pip install pytest
```

- Crear el directory tests i dins el fitxer __init__.py. Dins del directory crear els tests amb el prefix test_

- Crear el fitxer de configuració pytest.ini amb el següent contingut:

```ini
[pytest]
addopts = -p no:warnings
```

- Executar els test amb el comandament:

```bash
pytest
```

