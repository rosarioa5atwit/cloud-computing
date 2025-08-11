from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests
import definitions as d
import idp as i
import connection as conn
import uvicorn

#port 3801

app = FastAPI() #routing

@app.put("/user/signup") #add customer
async def signup(c: d.Customer):
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO customers (first_name, last_name, email, shipping_address, billing_address) VALUES (%s, %s, %s, %s, %s)", (c.first_name, c.last_name, c.email, c.shipping_address, c.billing_address))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"{c.first_name} {c.last_name} was added to the database."})

    return {"message": ress.text}

@app.get("/user/profile") #view customer details
async def viewprofile(first: str, last: str, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    #print(res.status_code)
    if res.status_code == 400:
        return html(status_code=400)
    
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("SELECT first_name, last_name, email, shipping_address, billing_address FROM customers WHERE first_name = %s AND last_name = %s",
    (first, last))
    rows = cur.fetchall()
    con.close()
    return rows

@app.get("/user/profile/edit") #change customer details 
async def editprofile(first: str, last:str, shipaddr: int, billaddr: int, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    #print(res.status_code)
    if res.status_code == 400:
        return html(status_code=400)
    
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("UPDATE customers SET shipping_address = %s, billing_address = %s WHERE first_name = %s AND last_name = %s", (shipaddr, billaddr, first, last))

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"{first} {last}'s shipping address was set to {shipaddr} and billing address to {billaddr}"})

    return {"message": ress.text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3801)