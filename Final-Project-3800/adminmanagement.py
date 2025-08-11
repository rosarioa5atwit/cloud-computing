from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests
import definitions as d
import connection as conn
import uvicorn

app = FastAPI() #routing

@app.get("/admin/fetch") #view all tables
async def fetch(table:str, token:str = Header(default = None), first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last":last, "type":"administrator"})
    if res.status_code == 400:
        return html(status_code=400) #checks for admin privileges

    # Validate table name to prevent SQL injection
    allowed_tables = ["customers", "vendors", "administrator", "cd", "orders", "order_items"]
    if table not in allowed_tables:
        return html(status_code=400)

    con = conn.get_db()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table}")  # Safe now that we validated the table name
    rows = cur.fetchall()
    con.close()
    
    return rows

@app.put("/admin/createvendor")
async def createven(v:d.Vendor,token:str = Header(default = None), first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last":last, "type":"administrator"})
    if res.status_code == 400:
        return html(status_code=400) #checks for admin privileges

    con = conn.get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO vendors (vendor_name, email_address, shipping_address, billing_address) VALUES (%s, %s, %s, %s)", (v.vendor_name, v.email_address, v.shipping_address, v.billing_address))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"Vendor {v.vendor_name} was added to the database."})

    return {"message": ress.text}

@app.get("/admin/delvendor")
async def deleteven(vid:int, token:str = Header(default = None), first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last":last, "type":"administrator"})
    if res.status_code == 400:
        return html(status_code=400) #checks for admin privileges
    
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM vendors WHERE vendor_id = %s", (vid,))
    cur.execute("DELETE FROM cd WHERE vendor_id = %s", (vid,))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"Vendor {vid} and their products were remeoved from the database."})

    return {"message": ress.text}

@app.put("/admin/addadmin")
async def addadmin(a:d.Administrator, token:str = Header(default = None), first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last":last, "type":"administrator"})
    if res.status_code == 400:
        return html(status_code=400) #checks for admin privileges
    
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO administrator (first_name, last_name, email) VALUES (%s, %s, %s)", (a.first_name, a.last_name, a.email))
    con.commit()
    con.close()
    
    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"admin {a.first_name} {a.last_name} added."})

    return {"message": ress.text}
    

@app.put("/admin/deladmin")
async def deladmin(aid:str, token:str = Header(default = None), first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last":last, "type":"administrator"})
    if res.status_code == 400:
        return html(status_code=400) #checks for admin privileges
    
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM administrator WHERE admin_id = %s", (aid,))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"admin id:{aid} deleted."})

    return {"message": ress.text}

@app.get("/admin/reports")
async def readlogs(token:str = Header(default = None), first:str = Header(default=None), last:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)

    res = requests.get(url="http://localhost:3803/permissions", headers = {"first": first, "last":last, "type":"administrator"})
    if res.status_code == 400:
        return html(status_code=400) #checks for admin privileges

    ress = requests.get(url="http://localhost:3805/reports/read")

    return {"logs": ress.text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3808)