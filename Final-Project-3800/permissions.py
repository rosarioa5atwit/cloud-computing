from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests as r
import definitions as d
import connection as conn
import uvicorn

#port 3803

recognized = [[], []] #0 = ADMIN, 1 = VENDOR

app = FastAPI() #routing

@app.get("/permissions") #add rental
async def perms(last:str = Header(default=None), first:str = Header(default=None), type:str = Header(default=None)): #type should be table name, administrator or vendors or "all"

    if type == "all":
        if inlist(first, last, "administrator") or inlist(first, last, "vendors"):
            return html(status_code=200)
    else:
        if inlist(first, last, type):
            return html(status_code=200)

    con = conn.get_db()
    cur = con.cursor()

    if type == "administrator" or (type == "all" and last!= None):
        cur.execute("SELECT first_name, last_name FROM administrator WHERE first_name = %s AND last_name = %s", (first, last))
    else:
        cur.execute("SELECT vendor_name FROM vendors WHERE vendor_name = %s", (first,))
    rows = cur.fetchall()
    con.close()

    if len(rows)>0:
        addtolist(first, last, type)
        return html(status_code=200)
    else:
        return html(status_code=400)

def inlist(first, last, type):
    
    if type == "administrator":
         if f"{first}{last}" in recognized[0]:
            return True
    else:
         if first in recognized[1]:
            return True
    return False
    
def addtolist(first, last, type):
    if type == "administrator":
        recognized[0].append(f"{first}{last}")
    else:
        recognized[1].append(f"{first}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3803)