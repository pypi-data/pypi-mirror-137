from datetime import datetime
from pprint import pprint

from .init_creds import init_mongo
from .dates import set_next_vigency, calculate_payment_date, get_periodo, localize
from .format import datetime_parser
import mercadopago
from bson import ObjectId


unaware_today = datetime.utcnow()
today = localize(unaware_today)

################
# CALCULATIONS #
################


def get_client_price(client: dict, plan: dict) -> dict:
    """ Obtener el precio a pagar

    :param client: cliente con la estructura que se usa en mongodb
    :type client: dict
    :param plan: plan con la estructura que se usa en mongodb
    :type plan: dict
    :return: informacion del precio
    :rtype: dict
    """    
    db = init_mongo()
    prices = {"native_plan": plan["price"]}
    print(f"    El precio del plan es {plan['price']}")
    corpo = db.corporativo.find_one({"_id": client["plan_corporativo"]})
    if corpo:
        prices["corpo_discount"] = - plan["price"] * corpo["porcentaje-descuento-empleado"] / 100

    if "discounts" in client.keys():
        if client["discounts"]:
            discounts = [i for i in client["discounts"] if i["aplicaciones_restantes"] > 0 and i["fecha_vigencia"] > unaware_today]
            discount_amount = (plan["price"] * sum([i["porcentaje"] for i in discounts])) / 100 + sum([i["monto_absoluto"] for i in discounts])
            prices["discounts"] = - discount_amount

    prices["final_price"] = max(0, sum(prices.values()))
    prices["access"] = get_access_amount(client["_id"])
    
    print(f"    El monto a cobrar es de ${prices['final_price']}")
    return prices


def get_access_amount(c_id: int) -> int:
    """ Obtener monto de acceso

    :param c_id: id del socio
    :type c_id: int
    :return: Monto de acceso
    :rtype: int
    """
    db = init_mongo()
    last_payment = [p["date_created"] for p in db.cobros.find({"socio_id": c_id})]
    if last_payment:
        last_payment_date = max(last_payment)
    else:
        last_payment_date = datetime(year=2000, month=1, day=1)
    uses = db.accesos.find({"socio_id": c_id, "fecha": {"$gt": last_payment_date}, "costo": {"$gt": 0}})
    result = sum([a["costo"] for a in uses])
    return result


def substract_discounts(client: dict):
    """ Descontar aplicaciones de descuento

    :param client: cliente con la estructura que se usa en mongodb
    :type client: dict
    """        
    if client["discounts"]:
        print("Se analizan los descuentos:")
        for discount in client["discounts"]:
            if discount["aplicaciones_restantes"] > 0:
                discount["aplicaciones_restantes"] -= 1
                print("    se descuenta una aplicacion restante.")


############
# PAYMENTS #
############

def resolve_payment(payment_data: dict, card_data: dict, _client: dict, _plan: dict, sdk: mercadopago.SDK) -> dict:
    """ Resolver pago si es posible

    :param payment_data: informacion del pago
    :type payment_data: dict
    :param card_data: informacion de la tarjeta
    :type card_data: dict
    :param _client: informacion del cliente
    :type _client: dict
    :param _plan: informacion del plan
    :type _plan: dict
    :param sdk: sdk de mercadopago
    :type sdk: mercadopago.SDK
    :return: informacion con el resultado del proceso
    :rtype: dict
    """
    if payment_data["charges_detail"]["final_price"] > 0:
        if card_data["card_id"] is None:
            print("    Tarjeta no encontrada. No se puede procesar el pago.")
            payment_result = {"status": "error", "status_detail": "No se puede obtener la tarjeta activa.",
                              "prev_status": payment_data["status"]}
        else:
            print("    Se procede a realizar un pago de $" + str(payment_data["charges_detail"]["final_price"]))

            payment_result = process_payment(payment_data, card_data, _client, _plan, sdk)

    else:
        print("    Pago no realizado por ser precio 0.")
        payment_result = {
            "status": "approved",
            "status_detail": "Pago no realizado por ser precio 0.",
            "id": 11,
            "prev_status": payment_data["status"]
        }
    return payment_result


def process_payment(payment_data: dict, card_data: dict, _client: dict, _plan: dict, sdk: mercadopago.SDK) -> dict:
    """ Procesar pago

    :param payment_data: informacion del pago
    :type payment_data: dict
    :param card_data: informacion de la tarjeta
    :type card_data: dict
    :param _client: informacion del cliente
    :type _client: dict
    :param _plan: informacion
    :type _plan: dict
    :param sdk: sdk de mercadopago
    :type sdk: mercadopago.SDK
    :return: informacion con el resultado del proceso
    :rtype: dict
    """
    print("    Se procede a realizar el pago con MP")
    data = {"card_id": int(card_data["card_id"])}
    card_token_response = sdk.card_token().create(data)

    if card_token_response["status"] > 299:
        print("         Falló la creación de token de tarjeta.")
        print(card_token_response["response"])
        return {"status": "error",
                "status_detail": "Falló la creación de token de la tarjeta.",
                "response": card_token_response["response"]["message"],
                "prev_status": payment_data["status"]
                }

    card_token = card_token_response["response"]["id"]
    print(f"        Token generado OK")
    
    mp_payment_data = {
        "additional_info": {
            "items": [{
                "title": f'{_plan["name"]} - {_client["nombre"]} {_client["apellido"]} - {_client["email"]} -' 
                         f'{payment_data["period"]}',
                "category_id": _plan["nivel_de_acceso"],
                "description": f'{_plan["name"]} - {_client["nombre"]} {_client["apellido"]} - {_client["email"]} -' 
                         f'{payment_data["period"]}'
            }]
        },
        "notification_url": f"https://apisportclub.xyz/notificacion/mp"
                            f"?source_news=webhooks&merchant={str(_plan['merchant_id'])}",
        "transaction_amount": payment_data["charges_detail"]["final_price"],
        "token": card_token,  # ??
        "description": _plan["name"],  # ir a base de datos de planes y traer el name
        "installments": 1,  # ??
        "payer": {
            "id": _client["mercadopago_id"]
        },
        "external_reference": str(payment_data["_id"])
    }
    payment_attempt = sdk.payment().create(mp_payment_data)
    payment_response = payment_attempt["response"]

    print("         El estado del pago es :" + str(payment_response["status"]))

    # si hay algun error en el pago
    if payment_attempt["status"] >= 299:
        pprint(payment_response)
        return {
            "status": "error",
            "status_detail": "Falló el intento de pago",
            "response": payment_attempt["response"],
            "prev_status": payment_data["status"]
        }

    # si el pago es 200
    return {
        "status": payment_response["status"],
        "status_detail": payment_response["status_detail"],
        "id": payment_response["id"],
        "prev_status": payment_data["status"]
    }


def create_payment_data(_client: dict, prices: dict, merchant_id: ObjectId) -> dict:
    """ Crear data del pago y guardalo en la coleccion de boletas de mongodb

    :param _client: cliente con la estructura que se usa en mongodb
    :type _client: dict
    :param prices: informacion de precios
    :type prices: dict
    :param merchant_id: id del merchant
    :type merchant_id: ObjectId
    :return: data que se guardo en la coleccion de boletas
    :rtype: dict
    """
    db = init_mongo()
    print("    Se genera la boleta de pago.")
    data = {"member_id": _client["_id"],
            "date_created": today,
            "original_payment_date": _client["next_payment_date"],
            "source": "recurring_charges",
            "tries": [],
            "status": "pending",
            "merchant_id": merchant_id,
            "charges_detail": prices,
            "period": get_periodo(),
            "plan_id": _client["active_plan_id"]}

    _id = db.boletas.insert_one(data)
    return data


def update_payment_data(payment_result: dict, payment_data: dict, card_data: dict):
    """ Actualizar pago. En payment_data se agrega un nuevo intento de pago

    :param payment_result: Resultado del pago
    :type payment_result: dict
    :param payment_data: data del pago que se quiere actualizar
    :type payment_data: dict
    :param card_data: informacion de la tarjeta
    :type card_data: dict
    """
    n_try = len(payment_data["tries"]) + 1

    if not "id" in payment_result.keys():
        payment_result["id"] = 400  # corresponde a un error 400

    intento = {
        "try_number": n_try,
        "payment_day": today,
        "payment_type": card_data["card_type"],
        "card_brand": card_data["card_brand"],
        "card_id": card_data["card_id"],
        "status": payment_result["status"],
        "status_detail": payment_result["status_detail"],
        "payment_id": payment_result["id"]
    }
    payment_data["tries"].append(intento)
    payment_data["status"] = payment_result["status"]
    return


def get_active_card(_client: dict, price: int, sdk: mercadopago.SDK):
    """ Obtener la tarjeta activa (con la que se realizan los pagos)

    :param _client: Cliente con la estructura que se usa en mongodb
    :type _client: dict
    :param price: Precio que se quiere cobrar. Si es 0 no se busca la tarjeta
    :type price: dict
    :param sdk: sdk de mercado pago
    :type sdk: mercadopago.SDK
    :return: data de la tarjeta
    :rtype: dict
    """
    print("    Se busca la tarjeta activa del cliente.")
    card = {"card_id": None,
            "payer_id": None,
            "card_type": None,
            "card_brand": None}

    if price == 0:
        print("         Por monto $0 no se busca tarjeta.")
        return card

    if "cards" in _client.keys():
        if _client["cards"]:
            try:
                card_complete = next((item for item in _client["cards"] if item["id"] == _client["active_card"]), card)
                if card_complete["id"]:
                    card = card_complete
                else:
                    card = _client["cards"][0]
                return {"card_id": card["id"],
                        "payer_id": card["customer_id"],
                        "card_type": card["payment_method"]["payment_type_id"],
                        "card_brand": card["payment_method"]["name"]}
            except:
                print("         ERROR: No se puede obtener la tarjeta del cliente.")
                return card
        else:
            print("         Cliente sin atributo 'cards'.")

    print(card)
    if not card["card_id"] and "active_card" in _client.keys() and "mercadopago_id" in _client.keys():
        mp_card_data = sdk.card().get(_client["mercadopago_id"], _client["active_card"])
        if mp_card_data["status"] == 200:
            mp_card_data = mp_card_data["response"]
            card["card_id"] = mp_card_data["id"]
            card["payer_id"] = mp_card_data["user_id"]
            card["card_type"] = mp_card_data["payment_method"]["payment_type_id"]
            card["card_brand"] = mp_card_data["payment_method"]["name"]

        elif "active_card" in _client.keys():
            card["card_id"] = _client["active_card"]

    return card


def update_client(_client: dict, _payment_result: dict, _plan: dict):
    """ Actualizar cliente

    :param _client: Cliente con la estructura que se usa en mongodb
    :type _client: dict
    :param _payment_result: Data del resultado del pago
    :type _payment_result: dict
    :param _plan: Plan con la estructura que se usa en mongodb
    :type _plan: dict
    """
    print("    Se procede a updatear al cliente...")
    # si el pago tiene id_mp se los agrego al cliente
    if "id" in _payment_result.keys():
        print("         Se inserta payment id en el cliente.")
        _client["payment_ids"].insert(0,_payment_result["id"])
        _client["last_payment_id"] = _payment_result["id"]

    # actualizaciones de cliente
    _client["lastModified"] = today
    
    if _payment_result["prev_status"] == "pending":
        _client["next_payment_date"] = calculate_payment_date(_client, _plan["cobro"])
        print("         El proximo dia de cobro es el "+ _client["next_payment_date"].strftime("%d/%m/%y"))
        # se resta una aplicacion de descuento
        if "discounts" in _client.keys():
            substract_discounts(_client)

    # updateo de la fecha de vigencia y los cobros recurrentes
    if _payment_result["status"] == "approved":
        _client["cobros_recurrentes"] += 1
        _client["fecha_vigencia"] = set_next_vigency(_client["next_payment_date"])
    else:
        if localize(_client["fecha_vigencia"]) < today:
            _client["status"] = "inactivo"
            print("         El cliente pasa inactivo por vencer la vigencia")
            
    return


def refund_process(payment_id: str, amount: int, sdk: mercadopago.SDK) -> dict:
    """ Hacer un reembolso

    :param payment_id: id del pago a reembolsar
    :type payment_id: str
    :param amount: monto a reembolsar
    :type amount: int
    :param sdk: sdk de mercadopago
    :type sdk: mercadopago.SDK
    :return: respuesta de mercadopago con informacion del reembolso
    :rtype: dict
    """
    refund_data = {
        "amount": amount
    }
    refund_response = sdk.refund().create(payment_id, refund_data)
    refund = refund_response["response"]
    pprint(refund)
    refund_data = datetime_parser(refund)
    return refund_data

