from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests as r
import definitions as d
import connection as conn
import uvicorn

#port 3805

log = []

app = FastAPI() #routing

@app.get("/reports/read") #check reports
async def read():
    return log

@app.get("/reports/document") #document actions
async def document(action:str):
    log.append(action)
    return action

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3805)
    