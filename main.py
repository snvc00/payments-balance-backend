from http import HTTPStatus
from os import environ

from fastapi import FastAPI
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, Document

from models.payment import Payment

app = FastAPI()
client = CloudantV1.new_instance()
db_name = environ["PAYMENTS_BALANCE_DATABASE_NAME"]

@app.get("/api/cloudant")
def cloudant_server_info():
    server_information = client.get_server_information().get_result()

    return server_information


#! Remove or improve this endpoint
@app.get("/api/cloudant/databases/{new_db_name}")
def create_cloudant_database(new_db_name: str):
    try:
        result = client.put_database(db=new_db_name).get_result()

        return result
    except ApiException as api_exception:
        if api_exception.code == HTTPStatus.PRECONDITION_FAILED:
            print(f"Existing database with name: {new_db_name}")

        return api_exception


@app.post("/api/payments/")
async def create_payment(payment: Payment):
    new_payment = Document.from_dict(payment.dict())
    response = client.post_document(db=db_name, document=new_payment)

    return response.result


@app.get("/api/payments/")
async def read_payments():
    payments = client.post_all_docs(db=db_name, include_docs=True).get_result()

    return payments


@app.get("/api/payments/{payment_id}")
async def read_payment(payment_id: str):
    payment = client.get_document(db=db_name, doc_id=payment_id).get_result()

    return payment


@app.put("/api/payments/{payment_id}")
async def update_payment(payment_id: str, payment: Payment):
    payment.id = payment_id
    updated_payment = Document.from_dict(payment.dict())
    response = client.post_document(db=db_name, document=updated_payment)

    return response.result


@app.delete("/api/payments/{payment_id}")
async def delete_payment(payment_id: str):
    try:
        payment = client.get_document(db=db_name, doc_id=payment_id).get_result()
        response = client.delete_document(
            db=db_name, doc_id=payment_id, rev=payment["_rev"]
        ).get_result()

        return response
    except ApiException as api_exception:
        if api_exception.code == HTTPStatus.NOT_FOUND:
            print(f"Payment with ID: {payment_id} not found")

        return api_exception
