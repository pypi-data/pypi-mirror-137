from datetime import datetime, date
import typing
import iso8601
import json
from bson import ObjectId


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def datetime_parser(dct: typing.Union[dict, str]) -> typing.Union[dict, str]:
    """ Parsear las fechas de un diccionario a formato iso 8601

    :param dct: Diccionario o string a parsear
    :type dct: Diccionario o string
    :return: Diccionario o string a parseado
    :rtype: Diccionario o string
    """
    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(v, dict):
                dct[k] = datetime_parser(v)
            if isinstance(v, str) and len(v) > 12:
                try:
                    dct[k] = iso8601.parse_date(v)
                except:
                    pass
    return dct


def json_serial(dct: typing.Union[dict, list]) -> typing.Union[dict, list]:
    for k, v in dct.items():
        if isinstance(v, dict):
            dct[k] = json_serial(v)
        elif isinstance(v, (datetime, date)):
            dct[k] = v.isoformat()
        elif isinstance(v, list):
            dct[k] = [json_serial(e) if isinstance(e, dict) else e for e in v]
        else:
            if not is_jsonable(v):
                dct[k] = str(v)
    return dct


def format_ids(dct: dict) -> dict:
    """ Cambiar las claves de diccionario "_id" a "id"

    :param dct: diccionario con claves "_id"
    :type dct: dict
    :return: Diccionario modificado
    :rtype: dict
    """    
    r = dict()
    for k, v in dct.items():
        if k == "_id":
            r["id"] = v
        else:
            r[k] = v
    return r


def format_object_ids(dct: dict) -> dict:
    """ Crear un diccionario igual al que se recibe por parametro pero las \
        claves "id" se actualizan a "_id" y los valores de estas claves se \
        convierten a ObjectId

    :param dct: diccionario original
    :type dct: dict
    :return: diccionario actualizado
    :rtype: dict
    """    
    r = dict()
    for k, v in dct.items():
        if k == "id":
            r["_id"] = ObjectId(v)
        else:
            r[k] = v
    return r
