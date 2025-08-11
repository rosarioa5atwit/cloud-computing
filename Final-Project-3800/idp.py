import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse as html

#port 3800

tokens = []

app = FastAPI() #routing
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/login")
async def login(usrID: str = Header(default=None)):
    if usrID in tokens:
        return usrID
    else:
        tokens.append(usrID)
        return usrID


@app.get("/isvalid")
async def isvalid(token:str = Header(default=None)):
    if token in tokens:
        return html(status_code=200)
    else:
        return html(status_code=400)
    
if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=3800)