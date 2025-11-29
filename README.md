🧾 Billing System – FastAPI + SQLite + Real Email Sending
=========================================================

A complete Billing System built using **FastAPI**, **SQLModel**, **SQLite**, **Jinja2**, and **real SMTP email sending**.

This app allows you to:

*   Generate customer bills
    
*   Automatically compute totals, taxes, and rounded amounts
    
*   Calculate change using available denominations
    
*   Preview invoices instantly on the same page
    
*   Send customer invoices **via real email (SMTP)**
    
*   View previous purchases in a modal popup
    
*   Persist purchasing history in SQLite
    

📂 Folder Structure
-------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML   

```

BILLING_SYSTEM/
│
├── app/
│   ├── __init__.py
│   ├── curd.py              # Business logic (product lines, totals, change calc)
│   ├── db.py                # DB engine + session + initialization
│   ├── models.py            # SQLModel ORM models
│   └── send_mail.py         # REAL email sending logic (SMTP)
│
├── database/
│   └── billing.db           # SQLite DB
│
├── static/
│   └── style.css            # Styles for billing page + invoice
│
├── templates/
│   ├── billing.html         # Billing UI + invoice preview panel
│   ├── invoice.html         # Invoice HTML template
│   └── invoice_email.html   # Email-friendly HTML invoice
│
├── main.py                  # FastAPI app entrypoint
├── requirements.txt
└── README.md

````

🚀 Features
-----------

### 🧾 Billing Page

*   Select products
    
*   Add/remove multiple items
    
*   Quantity and pricing auto-calculated
    
*   Automatically generates totals & taxes
    

### 💵 Denomination Calculation

*   Uses shop’s available denominations
    
*   Computes optimal change for the customer
    
*   Handles remainders if exact change not possible
    

### 🖼 Live Invoice Preview (AJAX)

*   Clicking **Generate Bill** does NOT redirect
    
*   Sends form with fetch()
    
*   Injects invoice HTML into the right-side panel
    
*   Smooth user experience
    

### ✉️ REAL Time Email Sending

send\_mail.py sends actual emails using SMTP.

This includes:

*   HTML invoice
    
*   Subject + formatting
    
*   Real email delivery to customer inbox
    

Supported SMTP providers:

*   Gmail (App Password)
    
*   Outlook / Hotmail
    
*   Yahoo
    
*   Custom SMTP servers
    
*   Office 365 / Work mail servers
    

### 🗂 View Previous Purchases (Modal Popup)

*   Enter customer email
    
*   Show past bills in a modal window
    
*   Modal fetches /customers//purchases
    
*   Extracts the #previousPurchases HTML section
    

🛠 Installation
---------------

### 1\. Create virtual environment

`   python -m venv venv  source venv/bin/activate   `

### 2\. Install dependencies

`   pip install -r requirements.txt   `

### 3\. Configure Email SMTP

Edit **app/send\_mail.py** and set:

```
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASS = "your_app_password"
````

> **Gmail users:**Generate an **App Password** (Google → Security → App passwords).Regular account password will NOT work.

### 4\. Run the server

`   uvicorn main:app --reload   `

Visit:

👉 http://127.0.0.1:8000

🧩 Key Endpoints
----------------

### **GET /**

Main billing page with invoice preview.

### **POST /generate**

Creates purchase, sends email, returns rendered invoice HTML.

### **GET /customers/{email}/purchases**

Returns purchase history HTML used in the modal.

### **GET /purchases/{id}**

Single invoice view.


📘 Database
-----------

SQLite DB auto-created at:

`   database/billing.db   `

Seeded via curd.seed\_data() on startup.

📌 Future Enhancements 
---------------------------------

*   Printable PDF invoices
    
*   Product management UI
    
*   Real admin dashboard
    
*   Logging + monitoring
    

👨‍💻 Author
------------

Built by **SHIJASMON H**
