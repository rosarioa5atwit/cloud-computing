from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
from datetime import datetime, timedelta
import requests
import definitions as d
import connection as conn
import uvicorn

app = FastAPI() #routing

@app.put("/rental/create") #add rental
async def rent(o: d.Order, i_id:int, r:bool = True, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.put(url="http://localhost:3802/purchase/order", headers = {"token": token}, json = o.model_dump(mode="json"), params={"i_id":i_id, "r":r})
    #calls /purchase/order by proxy
    return res.text

@app.get("/rental/extend") #extend rental
async def extend(oid:int, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)

    con = conn.get_db()
    cur = con.cursor()
    cur.execute("UPDATE orders SET date_due = %s WHERE order_id = %s", (datetime.now()+timedelta(days=14), oid))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"time updated for order id: {oid}"})

    return {"message": ress.text}


@app.get("/rental/cancel") #cancel rental
async def cancel(oid, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    res = requests.get(url="http://localhost:3802/purchase/cancel", headers = {"token": token}, params={"oid":oid})
    return res.text

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3807)

