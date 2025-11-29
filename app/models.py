from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str = Field(index=True, nullable=False, unique=True)
    name: str
    stock: int
    price: float
    tax_percent: float

class PurchaseItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    purchase_id: Optional[int] = Field(foreign_key="purchase.id")
    product_id: Optional[int] = Field(foreign_key="product.id")
    quantity: int
    unit_price: float
    tax_percent: float

class Purchase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_without_tax: float = 0.0
    total_tax: float = 0.0
    total_payable: float = 0.0
    rounded_total: float = 0.0

class Denomination(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int
    count: int 
