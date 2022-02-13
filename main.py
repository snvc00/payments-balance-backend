from fastapi import FastAPI
from models.payment import Payment

app = FastAPI()
db = []


@app.get("/")
def read_root():
    return {"message": "Hello world!"}


@app.get("/api/payments/")
async def fetch_payments():
    return db


@app.post("/api/payments/")
async def create_payment(payment: Payment):
    db.append(payment)
    return payment
