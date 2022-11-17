# Intro

## Setup
Two folders: backend and web

* Install fastapi: ```pip install "fastapi[all]"```
* Download and install nodejs and run ```npm install``` in the web folder

## Run

Open the repo folder in VS code and launch both configs or run both tasks, or run the following in command line

Backend:
```uvicorn main:app --app-dir=backend --reload --host 0.0.0.0 --port 8001```

Website:
```npm --prefix ./web/ run start```

Website will be hosted on [localhost:8000](http://localhost:8000)