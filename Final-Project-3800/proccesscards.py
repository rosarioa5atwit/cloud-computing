from fastapi import FastAPI, Cookie, Header
from fastapi.responses import HTMLResponse as html
import uvicorn

#simulates valid holder numbers categorized by banks
banksinfo = [["Visa", ["1234", "2345", "3456", "4567"]], ["MasterCard", ["1111", "2222", "3333", "4444"]], ["Capital One", ["1122", "2233", "3344", "4455"]]]

app = FastAPI() #routing

@app.get("/validatecard")
async def validate(bank:str, cardnum:str):
    cardnums = findcard(bank)
    if cardnum in cardnums:
        return html(status_code=200)
    else:
        return html(status_code=400)

def findcard(bank_name):
    for i in banksinfo:
        if i[0] == bank_name:
            return i[1]  # Return the card numbers list, not the whole entry
    return []