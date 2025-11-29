from fastapi import FastAPI, Request, HTTPException, Form, BackgroundTasks, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.send_mail import send_invoice_email
from app.db import init_db, get_session
from app import curd
from app.models import Product
from typing import List
import math
import json

app = FastAPI(title ="Billing System")

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.on_event("startup")
def on_startup():
    init_db()
    curd.seed_data()

@app.get("/")
def billing_page(request: Request, session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    denoms = curd.get_denominations(session)
    return templates.TemplateResponse("billing.html", {"request": request, "products": products, "denoms": denoms})

@app.post("/generate")
async def generate_bill(request: Request, 
                        background_tasks: BackgroundTasks, 
                        customer_email: str = Form(...), 
                        paid_amount: float = Form(...), 
                        lines_json: str = Form(...), 
                        session: Session = Depends(get_session)):
    try:
        lines = json.loads(lines_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid lines JSON")
    purchase = curd.create_purchase(session, customer_email, lines)
    purchase_data, detailed_items = curd.get_purchase_with_items(session, purchase.id)
    paid = float(paid_amount)
    change_due = round(paid - purchase.rounded_total, 2)
    change_rupees = int(math.floor(max(0.0, change_due)))
    denoms = curd.get_denominations(session)
    denom_map, remainder = curd.compute_change(denoms, change_rupees)

    html = templates.get_template("invoice.html").render({
        "purchase": purchase_data,
        "items": detailed_items,
        "paid": paid,
        "change_due": change_due,
        "denom_map": denom_map,
        "denom_remainder": remainder
    })

    email_html = templates.get_template("invoice_email.html").render({
        "purchase": purchase_data,
        "items": detailed_items,
        "paid": paid,
    })

    background_tasks.add_task(send_invoice_email, customer_email, email_html)
    return templates.TemplateResponse("invoice.html", 
                                      {"request": request, 
                                       "purchase": purchase_data, 
                                       "items": detailed_items, 
                                       "paid": paid, 
                                       "change_due": change_due, 
                                       "denom_map": denom_map, 
                                       "denom_remainder": remainder})

@app.get("/customers/{email}/purchases")
def view_purchases(email: str, request: Request, session: Session = Depends(get_session)):
    print(f"Fetching purchases for {email}")
    purchases = curd.get_purchases_by_email(session, email)
    products = session.exec(select(Product)).all()
    denoms = curd.get_denominations(session)
    return templates.TemplateResponse("billing.html", {
        "request": request,
        "previous_purchases": purchases,
        "products": products,
        "denoms": denoms
    })

@app.get("/purchases/{purchase_id}")
def view_purchase(purchase_id: int, request: Request, session: Session = Depends(get_session)):
    purchase_data, detailed_items = curd.get_purchase_with_items(session, purchase_id)
    if not purchase_data:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return templates.TemplateResponse("invoice_email.html", {
        "request": request,
        "purchase": purchase_data,
        "items": detailed_items,
        "paid": purchase_data.rounded_total,
    })