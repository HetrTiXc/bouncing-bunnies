# Intro

## Setup
Two folders: backend and web

* Install fastapi: ```pip install "fastapi[all]"```
* Download and install nodejs and run ```npm install```

## Run

Backend:
```uvicorn main:app --app-dir=backend --reload --host 0.0.0.0 --port 8001```

Website:
```npm --prefix ./web/ run start```

Website will be hosted on [localhost:8000](http://localhost:8000)