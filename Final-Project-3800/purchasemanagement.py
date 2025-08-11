from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
from fastapi.requests import Request as req
import requests
import definitions as d
import connection as conn
import uvicorn

#port 3802

app = FastAPI() #routing

@app.get("/store") #view offerings
async def store(token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    #print(res.status_code)
    if res.status_code == 400:
        return html(status_code=400)
    
    con = conn.get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM cd")
    rows = cur.fetchall()
    con.close()
    return rows
    

@app.put("/purchase/orderitem") #add order_item
async def newpurchase(o: d.Order_items, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)

    con = conn.get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO order_items (cd_id, quantity) VALUES (%s, %s)", (o.cd_id, o.quantity))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"CD orderitem with id: {o.cd_id}, quantity {o.quantity} was added to the database."})

    return {"message": ress.text}


@app.put("/purchase/order") #add order and link to order_item
async def newpurchase(o: d.Order, i_id:int, r:bool = False, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    con = conn.get_db()
    cur = con.cursor()
    #send to process cards for payment confirm
    cur.execute("INSERT INTO orders (customer_id, purchase_date, is_rental, ship_date, order_status, shipped_amount, card_type, card_number, card_expiration, card_cvv, billing_address) VALUES "
    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        (o.customer_id, o.purchase_date, r, o.ship_date, "processing", o.shipped_amount, o.card_type, o.card_number,
        o.card_expiration, o.card_cvv, o.billing_address))
    cur.execute("UPDATE order_items SET order_id = %s WHERE item_id = %s", (cur.lastrowid, i_id))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"Order: {cur.lastrowid}, for {o.customer_id} was added to the database."})

    return {"message": ress.text}

@app.get("/purchase/orderstatus")
async def orderstatus(oid: int, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)
    
    con = conn.get_db()
    cur = con.cursor()
    #send to process cards for payment confirm
    cur.execute("SELECT * FROM orders WHERE order_id = %s", (oid,))
    rows = cur.fetchall()
    con.close()

    return rows


@app.get("/purchase/cancel") #delete order and related items
async def cancel(oid:int, token:str = Header(default = None)):
    res = requests.get(url="http://localhost:3800/isvalid", headers = {"token": token})
    if res.status_code == 400:
        return html(status_code=400)

    con = conn.get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM order_items WHERE order_id = %s", (oid,))
    cur.execute("DELETE FROM orders WHERE order_id = %s", (oid, ))
    con.commit()
    con.close()

    ress = requests.get(url="http://localhost:3805/reports/document", params={"action":f"Order {oid} and its items were removed from the database."})

    return {"message": ress.text}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3802)