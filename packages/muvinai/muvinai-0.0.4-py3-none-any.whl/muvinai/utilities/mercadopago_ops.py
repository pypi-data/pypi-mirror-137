
from init_creds import init_mongo

import mercadopago

db = init_mongo()


def get_payment(payment_id, sdk):
    response = sdk.payment().search(filters={"id": payment_id})
    return response["response"]


def get_merchant_from_payment(payment_id):
    for merchant in db.merchants.find({}):
        sdk = mercadopago.SDK(merchant["keys"]["access_token"])
        payment = get_payment(payment_id, sdk)
        print(payment)


print(get_merchant_from_payment(100781564411))
