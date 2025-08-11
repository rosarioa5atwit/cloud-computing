from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests
import definitions as d
import connection as conn
import uvicorn

app = FastAPI() #routing

#maybe check for admin privileges
@app.get("/vendor/fetchproducts") #get items that vendor sells
async def fetch(table:str):
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM cd WHERE vendor_id = %s", (table, )) #change to recieve vendor id
    rows = cur.fetchall()
    con.close()
    return rows

@app.get("/vendor/removeitem") #remove item that vendor sells
async def removecd(pid:int, token:str = Header(default = None), first:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3804/inventory/removeitem", headers = {"token": token, "first": first}, params= {"pid":pid})
    if res.status_code == 400:
        return html(status_code=400)
    
    return res.text

@app.put("/vendor/additem") #add item that vendor sells
async def addcd(cd: d.Cd, token:str = Header(default = None), first:str = Header(default=None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    # Convert CD object to dictionary for JSON serialization
    cd_data = {
        "cd_id": cd.cd_id,
        "cd_name": cd.cd_name,
        "artist": cd.artist,
        "genre_id": cd.genre_id,
        "release_date": cd.release_date.isoformat() if hasattr(cd.release_date, 'isoformat') else str(cd.release_date),
        "price": cd.price,
        "quantity": cd.quantity,
        "vendor_id": cd.vendor_id
    }
    
    res = requests.put(url="http://localhost:3804/inventory/additem", headers = {"first": first, "last": ""}, json=cd_data)
    if res.status_code >= 400:
        return html(status_code=res.status_code)
    
    return res.text

@app.put("/vendor/signup")
async def vendor_signup(vendor: d.Vendor):
    con = conn.get_db()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO vendors (vendor_id, vendor_name, email_address, shipping_address, billing_address) VALUES (%s, %s, %s, %s, %s)",
            (vendor.vendor_id, vendor.vendor_name, vendor.email_address, vendor.shipping_address, vendor.billing_address)
        )
        con.commit()
        return {"message": "Vendor created successfully", "vendor_id": vendor.vendor_id}
    except Exception as e:
        con.rollback()
        return html(status_code=400)
    finally:
        con.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3809)