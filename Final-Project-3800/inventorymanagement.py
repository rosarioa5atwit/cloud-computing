from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests 
import definitions as d
import connection as conn
import uvicorn

#port 3804

app = FastAPI() #routing

@app.put("/inventory/additem") #add cd
async def addcd(cd: d.Cd, first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last": last, "type":"all"})
    if res.status_code == 400:
        return html(status_code=400) #checks for vendor privileges

    con = conn.get_db()
    cur = con.cursor()
    
    # Insert without cd_id to let it auto-increment
    cur.execute("INSERT INTO cd (cd_name, artist, genre_id, release_date, price, quantity, vendor_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (cd.cd_name, cd.artist, cd.genre_id, cd.release_date, cd.price, cd.quantity, cd.vendor_id))
    
    # Get the auto-generated cd_id
    new_cd_id = cur.lastrowid
    con.commit()
    con.close()
    
    return {"message": f"cd with id: {new_cd_id} was added to the database", "cd_id": new_cd_id}

@app.get("/inventory/removeitem") #remove item that vendor sells
async def removecd(pid:int, first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last": last, "type":"all"})
    if res.status_code == 400:
        return html(status_code=400) #checks for vendor privileges

    con = conn.get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM cd WHERE cd_id = %s", (pid, )) #change to recieve vendor id
    con.commit()
    con.close()

    return {"message": f"cd with id: {pid} was removed from the database"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3804)