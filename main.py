from http import HTTPStatus
from os import environ

from fastapi import FastAPI
from models.payment import Payment

from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1

app = FastAPI()
db = []
client = CloudantV1.new_instance()

@app.get("/")
def read_root():
    server_information = client.get_server_information().get_result()

    return {
        "message": "Hello world!",
        "server": server_information
    }


#! Remove or improve this endpoint
@app.get("/api/cloudant")
def create_cloudant_database():
    try:
        db_name = environ["PAYMENTS_BALANCE_DATABASE_NAME"]
        put_database_result = client.put_database(db=db_name).get_result()
        if put_database_result["ok"]:
            print(f'"{db_name}" database created.')
    except ApiException as api_exception:
        if api_exception.code == HTTPStatus.PRECONDITION_FAILED:
            print(f'Cannot create "{db_name}" database, it already exists.')


@app.post("/api/payments/")
async def create_payment(payment: Payment):
    return {
        "operation": "Create",
        "details": payment
    }


@app.get("/api/payments/")
async def read_payments():
    return {
        "operation": "Read all",
        "details": None
    }


@app.get("/api/payments/{payment_id}")
async def read_payment(payment_id: str):
    return {
        "operation": "Read one",
        "details": payment_id
    }


@app.put("/api/payments/{payment_id}")
async def update_payment(payment_id: str):
    return {
        "operation": "Update",
        "details": payment_id
    }


@app.delete("/api/payments/{payment_id}")
async def delete_payment(payment_id: str):
    return {
        "operation": "Delete",
        "details": payment_id
    }

