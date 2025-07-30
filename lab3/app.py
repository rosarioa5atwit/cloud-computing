from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import Dict, Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(title="CD Store API", description="Lab 3 FastAPI Application", version="1.0.0")

class CD(BaseModel):
    cd_id: int
    title: str
    artist: str
    price: float
    release_date: datetime
    category_id: int

class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str

class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    total_amount: float

class OrderItem(BaseModel):
    order_item_id: int
    order_id: int
    cd_id: int
    quantity: int
    price: float

class Address(BaseModel):
    address_id: int
    customer_id: int
    street: str
    city: str
    state: str
    zip_code: str

class Category(BaseModel):
    category_id: int
    name: str

customer_db: Dict[int, Customer] = {
    1: Customer(customer_id=1, first_name="John", last_name="Doe", email="john.doe@gmail.com"),
    2: Customer(customer_id=2, first_name="Jane", last_name="Smith", email="jane.smith@gmail.com"),
    3: Customer(customer_id=3, first_name="Alice", last_name="Johnson", email="alice.johnson@gmail.com"),
    4: Customer(customer_id=4, first_name="Bob", last_name="Brown", email="bob.brown@gmail.com"),
}

cd_db: Dict[int, CD] = {
    1: CD(cd_id=1, title="Greatest Hits", artist="Artist A", price=9.99, release_date=datetime(2020, 1, 1), category_id=1),
    2: CD(cd_id=2, title="Rock Classics", artist="Artist B", price=14.99, release_date=datetime(2019, 5, 20), category_id=2),
    3: CD(cd_id=3, title="Pop Hits", artist="Artist C", price=12.99, release_date=datetime(2021, 3, 15), category_id=3),
    4: CD(cd_id=4, title="Jazz Essentials", artist="Artist D", price=15.99, release_date=datetime(2018, 7, 30), category_id=4),
    5: CD(cd_id=5, title="Classical Masterpieces", artist="Artist E", price=19.99, release_date=datetime(2017, 11, 10), category_id=5),
    6: CD(cd_id=6, title="Indie Vibes", artist="Artist F", price=11.99, release_date=datetime(2022, 2, 25), category_id=6),
}

order_db: Dict[int, Order] = {
    1: Order(order_id=1, customer_id=1, order_date=datetime(2023, 10, 1), total_amount=29.97),
    2: Order(order_id=2, customer_id=2, order_date=datetime(2023, 10, 2), total_amount=14.99),
    3: Order(order_id=3, customer_id=3, order_date=datetime(2023, 10, 3), total_amount=12.99),
    4: Order(order_id=4, customer_id=4, order_date=datetime(2023, 10, 4), total_amount=15.99),
    5: Order(order_id=5, customer_id=1, order_date=datetime(2023, 10, 5), total_amount=9.99),
    6: Order(order_id=6, customer_id=2, order_date=datetime(2023, 10, 6), total_amount=19.99),
}

order_item_db: Dict[int, OrderItem] = {
    1: OrderItem(order_item_id=1, order_id=1, cd_id=1, quantity=2, price=9.99),
    2: OrderItem(order_item_id=2, order_id=1, cd_id=2, quantity=1, price=14.99),
    3: OrderItem(order_item_id=3, order_id=2, cd_id=3, quantity=1, price=12.99),
    4: OrderItem(order_item_id=4, order_id=3, cd_id=4, quantity=1, price=15.99),
    5: OrderItem(order_item_id=5, order_id=4, cd_id=5, quantity=1, price=19.99),
    6: OrderItem(order_item_id=6, order_id=5, cd_id=6, quantity=1, price=11.99),
}

address_db: Dict[int, Address] = {
    1: Address(address_id=1, customer_id=1, street="123 Main St", city="Springfield", state="IL", zip_code="62701"),
    2: Address(address_id=2, customer_id=2, street="456 Elm St", city="Shelbyville", state="IL", zip_code="62565"),
    3: Address(address_id=3, customer_id=3, street="789 Oak St", city="Capital City", state="IL", zip_code="62704"),
    4: Address(address_id=4, customer_id=4, street="321 Pine St", city="Ogdenville", state="IL", zip_code="62550"),
}

category_db: Dict[int, Category] = {
    1: Category(category_id=1, name="Pop"),
    2: Category(category_id=2, name="Rock"),
    3: Category(category_id=3, name="Jazz"),
    4: Category(category_id=4, name="Classical"),
    5: Category(category_id=5, name="Country"),
    6: Category(category_id=6, name="Indie"),
}


@app.get("/helloworld")
async def hello_world_alt():
    return {"message": "Hello from FastAPI"}
@app.get("/cds/{cd_id}")
async def get_cd_id (
    cd_id: int = Path(..., description="The ID of the CD to retrieve")
):
    if cd_id not in cd_db:
        raise HTTPException(status_code=404, detail="CD not found")
    return cd_db[cd_id]

@app.get("/customers/{customer_id}")
async def get_customer_id(
    customer_id: int = Path(..., description="The ID of the customer to retrieve")
):
    if customer_id not in customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_db[customer_id]

@app.get("/orders/{order_id}")
async def get_order_id(
    order_id: int = Path(..., description="The ID of the order to retrieve")
):
    if order_id not in order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_db[order_id]
@app.get("/orderItems/{order_item_id}")
async def get_order_item_id(
    order_item_id: int = Path(..., description="The ID of the order item to retrieve")
):
    if order_item_id not in order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item_db[order_item_id]
@app.get("/addresses/{address_id}")
async def get_address_id(
    address_id: int = Path(..., description="The ID of the address to retrieve")
):
    if address_id not in address_db:
        raise HTTPException(status_code=404, detail="Address not found")
    return address_db[address_id]
@app.get("/categories/{category_id}")
async def get_category_id(
    category_id: int = Path(..., description="The ID of the category to retrieve")
):
    if category_id not in category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_db[category_id]

@app.get("/customers")
async def get_customers(
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    limit: int = Query(10, description="Limit the number of results returned")
):
    customers = list(customer_db.values())
    if customer_id is not None:
        customers = [customer for customer in customers if customer.customer_id == customer_id]
    if first_name is not None:
        customers = [customer for customer in customers if first_name.lower() in customer.first_name.lower()]
    if last_name is not None:
        customers = [customer for customer in customers if last_name.lower() in customer.last_name.lower()]
    if email is not None:
        customers = [customer for customer in customers if email.lower() in customer.email.lower()]
    customers = customers[:limit]
    return {
        "customers": [customer.dict() for customer in customers],
        "total": len(customers),
    }
@app.get("/orders")
async def get_orders(
    order_id: Optional[int] = Query(None, description="Filter by order ID"),
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    limit: int = Query(10, description="Limit the number of results returned")
):
    orders = list(order_db.values())
    if order_id is not None:
        orders = [order for order in orders if order.order_id == order_id]
    if customer_id is not None:
        orders = [order for order in orders if order.customer_id == customer_id]
    if status is not None:
        orders = [order for order in orders if order.status.lower() == status.lower()]
    orders = orders[:limit]
    return {
        "orders": [order.dict() for order in orders],
        "total": len(orders),
    }
@app.get("/orderItems")
async def get_order_items(
    order_item_id: Optional[int] = Query(None, description="Filter by order item ID"),
    order_id: Optional[int] = Query(None, description="Filter by order ID"),
    cd_id: Optional[int] = Query(None, description="Filter by CD ID"),
    limit: int = Query(10, description="Limit the number of results returned")
):
    order_items = list(order_item_db.values())
    if order_item_id is not None:
        order_items = [item for item in order_items if item.order_item_id == order_item_id]
    if order_id is not None:
        order_items = [item for item in order_items if item.order_id == order_id]
    if cd_id is not None:
        order_items = [item for item in order_items if item.cd_id == cd_id]
    order_items = order_items[:limit]
    return {
        "order_items": [item.dict() for item in order_items],
        "total": len(order_items),
    }
@app.get("/addresses")
async def get_addresses(
    address_id: Optional[int] = Query(None, description="Filter by address ID"),
    customer_id: Optional[int] = Query(None, description="Filter by customer ID"),
    limit: int = Query(10, description="Limit the number of results returned")
):
    addresses = list(address_db.values())
    if address_id is not None:
        addresses = [address for address in addresses if address.address_id == address_id]
    if customer_id is not None:
        addresses = [address for address in addresses if address.customer_id == customer_id]
    addresses = addresses[:limit]
    return {
        "addresses": [address.dict() for address in addresses],
        "total": len(addresses),
    }

@app.get("/categories")
async def get_categories(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    name: Optional[str] = Query(None, description="Filter by category name"),
    limit: int = Query(10, description="Limit the number of results returned")
):
    categories = list(category_db.values())
    if category_id is not None:
        categories = [category for category in categories if category.category_id == category_id]
    if name is not None:
        categories = [category for category in categories if name.lower() in category.name.lower()]
    categories = categories[:limit]
    return {
        "categories": [category.dict() for category in categories],
        "total": len(categories),
    }


@app.get("/cds")
async def get_cds(
    cd_id: Optional[int] = Query(None, description="Filter by CD ID"),
    title: Optional[str] = Query(None, description="Filter by CD title"),
    artist: Optional[str] = Query(None, description="Filter by CD artist"),
    release_date: Optional[datetime] = Query(None, description="Filter by CD release date"),
    category_id: Optional[int] = Query(None, description="Filter by CD category ID"),
    limit: int = Query(10, description="Limit the number of results returned")
):
    cds = list(cd_db.values())
    if cd_id is not None:
        cds = [cd for cd in cds if cd.cd_id == cd_id]
    if title is not None:
        cds = [cd for cd in cds if title.lower() in cd.title.lower()]
    if artist is not None:
        cds = [cd for cd in cds if artist.lower() in cd.artist.lower()]
    if release_date is not None:
        cds = [cd for cd in cds if cd.release_date.date() == release_date.date()]
    if category_id is not None:
        cds = [cd for cd in cds if cd.category_id == category_id]
    cds = cds[:limit]
    return {

    "cds": [cd.dict() for cd in cds],
    "total": len(cds),

}

@app.put("/addresses/update/{address_id}")
async def update_address(
    address_id: int = Path(..., gt=0, description="The ID of the address to update"),
    address: Address = Body(..., description="The updated address data")
):
    if address_id not in address_db:
        raise HTTPException(status_code=404, detail="Address not found")
    
    updated_address = Address(
        address_id=address_id,
        customer_id=address.customer_id,
        street=address.street,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code
    )
    
    address_db[address_id] = updated_address
    
    return {
        "address": updated_address.dict()
    }
app.put("/categories/update/{category_id}")
async def update_category(
    category_id: int = Path(..., gt=0, description="The ID of the category to update"),
    category: Category = Body(..., description="The updated category data")
):
    if category_id not in category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    
    updated_category = Category(
        category_id=category_id,
        name=category.name
    )
    
    category_db[category_id] = updated_category
    
    return {
        "category": updated_category.dict()
    }
@app.put("/ordersItem/update/{order_item_id}")
async def update_order_item(
    order_item_id: int = Path(..., gt=0, description="The ID of the order item to update"),
    order_item: OrderItem = Body(..., description="The updated order item data")
):
    if order_item_id not in order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    updated_order_item = OrderItem(
        order_item_id=order_item_id,
        order_id=order_item.order_id,
        cd_id=order_item.cd_id,
        quantity=order_item.quantity,
        price=order_item.price
    )
    
    order_item_db[order_item_id] = updated_order_item
    
    return {
        "order_item": updated_order_item.dict()
    }

@app.put("/orders/update/{order_id}")
async def update_order(
    order_id: int = Path(..., gt=0, description="The ID of the order to update"),
    order: Order = Body(..., description="The updated order data")
):
    if order_id not in order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    updated_order = Order(
        order_id=order_id,
        customer_id=order.customer_id,
        order_date=order.order_date,
        total_amount=order.total_amount
    )
    
    order_db[order_id] = updated_order
    
    return {
        "order": updated_order.dict()
    }
@app.put("/cd/update/{cd_id}")
async def update_cd(
    cd_id: int = Path(..., gt=0, description="The ID of the CD to update"),
    cd: CD = Body(..., description="The updated CD data")
):
    if cd_id not in cd_db:
        raise HTTPException(status_code=404, detail="CD not found")
    
    updated_cd = CD(
        cd_id=cd_id,
        title=cd.title,
        artist=cd.artist,
        price=cd.price,
        release_date=cd.release_date,
        category_id=cd.category_id
    )
    
    cd_db[cd_id] = updated_cd
    
    return {
        "cd": updated_cd.dict()
    }

@app.put("/customers/update/{customer_id}")
async def update_customer(
    customer_id: int = Path(..., gt=0, description="The ID of the customer to update"),
    customer: Customer = Body(..., description="The updated customer data")
):
    if customer_id not in customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    updated_customer = Customer(
        customer_id=customer_id,
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email
    )   
    
    customer_db[customer_id] = updated_customer
    
    return {
        "customer": updated_customer.dict()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
