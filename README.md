# Python FastApi Project

### First Steps
* Install [Python 3](https://www.python.org/) < or latest
* Install [VsCode](https://code.visualstudio.com/)
* Install Python plugin (vsCode) Microsoft Version
* After deploying your app, you can use Swagger by add '/docs' on the url

## Dependency
* Virtual environment
```
pip install virtualenv
virtualenv -p python3 venv
.\venv\Scripts\activate
```
> [!CAUTION]
> if failure, open PowerShell as Admin and type 'Set-ExecutionPolicy Unrestricted'

* Install
```
pip list
pip install fastapi
pip install "uvicorn[standard]" // server
pip install pymssql             // SQL Server
pip install psycopg2            // PosgreSQL
pip install python-multipart    // OAuth2
pip install python-dotenv       // .env
pip freeze > requirements.txt
uvicorn app.main:app --reload

pip install -r requirements.txt
```

* Server
> http://127.0.0.1:8000/

> http://127.0.0.1:8000/docs

## File .env
```
MSSQL_USER="************"
MSSQL_HOST="************"
MSSQL_PASSWORD="************"
MSSQL_DATABASE="************"

POSTGRES_USER="************"
POSTGRES_HOST="************"
POSTGRES_PASSWORD="************"
POSTGRES_DATABASE="************"
```

## Folder Structure
```
project
│
├── app/
│   ├── routes/
│   │   ├── project.py
│   │   └── public.py
│   ├── tests/
│   ├── main.py
│   ├── models.py
│   └── mssql.py
├── venv/
├── .env
├── .env.local
├── .gitignore
├── README.md
├── requirements.txt
└── vercel.json
```