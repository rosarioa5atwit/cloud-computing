from pydantic import BaseModel
from datetime import datetime 
from typing import Optional

class Cd(BaseModel):
    cd_id: Optional[int] = None  # Make optional for auto-increment
    cd_name: str
    artist: str
    genre_id: int
    release_date: datetime
    price: float
    quantity: int
    vendor_id: int

class Order_items(BaseModel):
    item_id: int
    order_id: int
    cd_id: int
    quantity: int


class Administrator(BaseModel):
    admin_id: int
    first_name: str
    last_name: str
    email: str


class Order(BaseModel):
    order_id: int
    customer_id: int
    purchase_date: datetime
    is_rental: bool
    tax_amount: float
    ship_date: datetime
    order_status: str
    shipped_amount: float
    card_type: str
    card_number: str
    card_expiration: datetime   
    card_cvv: str
    date_due: datetime
    billing_address: int


class Genre(BaseModel):
    genre_id: int
    genre_name: str


class Vendor(BaseModel):
    vendor_id: int
    vendor_name: str
    email_address: str
    shipping_address: int
    billing_address: int

class Address(BaseModel):
    address_id: int
    line1: str
    line2: str
    city: str
    state: str
    zip: str
    country: str
    customer_id: int
    vendor_id: int

class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    shipping_address: int
    billing_address: int