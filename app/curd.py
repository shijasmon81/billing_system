from sqlmodel import Session, select
from .models import Denomination, Product, Purchase, PurchaseItem
from typing import List, Dict
from .db import engine
from decimal import Decimal, ROUND_HALF_UP

def seed_data():
    with Session(engine) as session:
        if session.exec(select(Product)).first() is None:
            products = [
                Product(product_id="P001", name="Pen", stock=100, price=10.0, tax_percent=5.0),
                Product(product_id="P002", name="Note Book", stock=50, price=40.0, tax_percent=12.0),
                Product(product_id="P003", name="Marker", stock=75, price=80.0, tax_percent=18.0),
            ]
            session.add_all(products)
        if session.exec(select(Denomination)).first() is None:
            denoms = [500, 50, 20, 2, 1]
            for i in denoms:
                session.add(Denomination(value=i, count=20))
        session.commit()

def get_denominations(session: Session):
    return session.exec(select(Denomination).order_by(Denomination.value.desc())).all()

def find_product_by_product_id(session: Session, product_id: str):
    return session.exec(select(Product).where(Product.product_id == product_id)).first()

def create_purchase(session: Session, customer_email: str, items: List[dict]):
    purchase = Purchase(customer_email=customer_email)
    session.add(purchase)
    session.commit()
    session.refresh(purchase)

    total_without_tax = 0.0
    total_tax = 0.0
    for it in items:
        product = find_product_by_product_id(session, it["product_id"])
        if product is None:
            raise ValueError(f"Product {it['product_id']} not found")
        qty = int(it["quantity"])
        unit_price = float(product.price)
        tax = float(product.tax_percent)
        price = unit_price * qty
        tax_amount = price * tax / 100.0
        item = PurchaseItem(
            purchase_id=purchase.id,
            product_id=product.id,
            quantity=qty,
            unit_price=unit_price,
            tax_percent=tax
        )
        session.add(item)
        total_without_tax += price
        total_tax += tax_amount
        product.stock = max(0, product.stock - qty)
    total_payable = total_without_tax + total_tax
    rounded_total = float(Decimal(total_payable).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    purchase.total_without_tax = total_without_tax
    purchase.total_tax = total_tax
    purchase.total_payable = total_payable
    purchase.rounded_total = rounded_total
    session.commit()
    session.refresh(purchase)
    return purchase


def get_purchase_with_items(session: Session, purchase_id: int):
    purchase = session.get(Purchase, purchase_id)
    if not purchase:
        return None
    items = session.exec(select(PurchaseItem).where(PurchaseItem.purchase_id == purchase_id)).all()
    # attach product info
    detailed = []
    for it in items:
        product = session.get(Product, it.product_id)
        detailed.append({
            "product_id": product.product_id,
            "name": product.name,
            "quantity": it.quantity,
            "unit_price": it.unit_price,
            "tax_percent": it.tax_percent,
            "total_price": it.unit_price * it.quantity,
            "tax_amount": it.unit_price * it.quantity * it.tax_percent / 100.0,
            "total_payable": (it.unit_price * it.quantity) + (it.unit_price * it.quantity * it.tax_percent / 100.0)
        })
    return purchase, detailed

def compute_change(available_denoms: List[Denomination], change_amount: int):
    result = {}
    remaining = change_amount
    for d in sorted(available_denoms, key=lambda x: x.value, reverse=True):
        if remaining <= 0:
            break
        use = min(d.count, remaining // d.value)
        if use > 0:
            result[d.value] = use
            remaining -= use * d.value
    return result, remaining 

def get_purchases_by_email(session: Session, email: str):
    return session.exec(select(Purchase).where(Purchase.customer_email == email).order_by(Purchase.created_at.desc())).all()

def get_purchase_with_items(session: Session, purchase_id: int):
    purchase = session.get(Purchase, purchase_id)
    if not purchase:
        return None
    items = session.exec(select(PurchaseItem).where(PurchaseItem.purchase_id == purchase_id)).all()
    # attach product info
    detailed = []
    for it in items:
        product = session.get(Product, it.product_id)
        detailed.append({
            "product_id": product.product_id,
            "name": product.name,
            "quantity": it.quantity,
            "unit_price": it.unit_price,
            "tax_percent": it.tax_percent,
            "total_price": it.unit_price * it.quantity,
            "tax_amount": it.unit_price * it.quantity * it.tax_percent / 100.0,
            "total_payable": (it.unit_price * it.quantity) + (it.unit_price * it.quantity * it.tax_percent / 100.0)
        })
    return purchase, detailed