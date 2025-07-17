from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class cd(BaseModel):
    cd_id : int
    title : str
    price : float
    artist : str
    Genera : str
    cd_id : int

class order(BaseModel):
    order_id: int
    cd_id: int
    user_id: int
    quantity: int
    total_price: float


class User(BaseModel):
    username: str
    phone_number: str
    address: str 
    user_id: int

tables = {
    "users": {
       1: {"username": "john_doe", "phone_number": "123-456-7890", "address": "123 Main St", "user_id": 1},
       2: {"username": "jane_doe", "phone_number": "987-654-3210", "address": "456 Oak Ave", "user_id": 2},
       3: {"username": "alice_smith", "phone_number": "555-555-5555", "address": "789 Pine Rd", "user_id": 3},
       4: {"username": "bob_jones", "phone_number": "444-444-4444", "address": "321 Maple Dr", "user_id": 4},
    },
    "cd": {
        1: {"cd_id": 1, "title": "The Dark Side of the Moon", "price": 19.99, "artist": "Pink Floyd", "Genera": "Rock"},
        2: {"cd_id": 2, "title": "Abbey Road", "price": 17.99, "artist": "The Beatles", "Genera": "Rock"},
        3: {"cd_id": 3, "title": "Thriller", "price": 15.99, "artist": "Michael Jackson", "Genera": "Pop"},
        4: {"cd_id": 4, "title": "Back in Black", "price": 18.99, "artist": "AC/DC", "Genera": "Rock"},
    },
    "orders": {
        1: {"order_id": 1, "cd_id": 1, "user_id": 1, "quantity": 2, "total_price": 39.98},
        2: {"order_id": 2, "cd_id": 2, "user_id": 2, "quantity": 1, "total_price": 17.99},
        3: {"order_id": 3, "cd_id": 3, "user_id": 3, "quantity": 3, "total_price": 47.97},
        4: {"order_id": 4, "cd_id": 4, "user_id": 4, "quantity": 1, "total_price": 18.99},
    }
}
@app.get("/users/{username}")
async def get_user(username: str, user:User):
    if username not in tables["users"]:
        return {"error": "User not found, please enter a valid username."}
    return tables["users"][username]

@app.get("/cd/{cd_id}")
async def get_cd(cd_id: int):
    if cd_id not in tables["cd"]:
        return {"error": "CD not found, please enter a valid CD ID."}
    return tables["cd"][cd_id]

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    if order_id not in tables["orders"]:
        return {"error": "Order not found, please enter a valid Order ID."}
    return tables["orders"][order_id]

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Lab 3"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test")
async def test_route():
    return {"message": "FastAPI is working correctly"}

@app.get("/info")
async def info():
    return {
        "app": "FastAPI Lab 3",
        "version": "1.0.0",
        "framework": "FastAPI"
    }

def maindriver():
    continueLoop = True
    while continueLoop:
        print("Main Menu")
        print("1. Execute FastAPI Routes")
        print("2. Execute Express Routes")
        print("3. Exit")

        choice = input("Enter your choice (1, 2 or 3): ")
        if choice == '1':
            print("Executing FastAPI Routes...")
            print("FastAPI server should be running on http://127.0.0.1:8000")
            print("Visit these endpoints:")
            print("- http://127.0.0.1:8000/")
            print("- http://127.0.0.1:8000/health")
            print("- http://127.0.0.1:8000/test")
            print("- http://127.0.0.1:8000/info")
            print("- http://127.0.0.1:8000/docs (for API documentation)")
            
        elif choice == '2':
            print("Executing Express Routes...")
            print("Express server should be running on http://localhost:3030")
            
        elif choice == '3':
            print("Exiting the program.")
            continueLoop = False
        else:
            print("Invalid choice. Please try again.")

# Note: The maindriver() function won't run when using uvicorn
# It's only for demonstration purposes
if __name__ == "__main__":
    maindriver()
