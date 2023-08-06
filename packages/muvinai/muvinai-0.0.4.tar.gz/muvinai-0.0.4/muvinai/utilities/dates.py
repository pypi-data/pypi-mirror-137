from datetime import datetime
import pytz
from dateutil.relativedelta import *
import calendar
import typing

DIAS_GRACIA = 10
DIAS_ANTICIPO_DE_PAGO = 7
MID_DAY_HOUR = 12

utc_now = pytz.utc.localize(datetime.utcnow())
arg_tz = pytz.timezone("America/Buenos_Aires")
today = utc_now.astimezone(arg_tz)

def readable_date(f: datetime) -> str:
    """ Convierte una variable de tipo datetime.datetime al formato DD-MM-YYYY

    :param f: valor a convertir
    :type f: datetime
    :return: fecha formateada DD-MM-YYYY
    :rtype: str
    """
    return f.strftime("%d-%m-%Y")


def set_fecha_vigencia(cobro: str) -> str:
    """ Calculo de la fecha de vigencia

    :param cobro: los valores posibles son Mensual, Trimestral, Cuatrimestral, Semestral, Anual
    :type cobro: str
    :return: Fecha de vigencia que corresponde al tipo de cobro recibido por parametro
    :rtype: str
    """
    duration_map = {"Mensual": 1, "Trimestral": 3, "Cuatrimestral": 4, "Semestral": 6, "Anual": 12}
    plan_duration = duration_map[cobro]
    if datetime.utcnow().day < 25:
        aux = datetime.utcnow() + relativedelta(months=+ plan_duration)
    else:
        aux = datetime.utcnow() + relativedelta(months=+ plan_duration + 1)

    end_of_month = calendar.monthrange(aux.year, aux.month)[1]
    f_vigencia = aux.replace(day=end_of_month)

    return f_vigencia


def string_to_datetime(mongo_date: typing.Union[str, datetime]) -> datetime:
    """ Convierte un string a datetime

    :param mongo_date: Fecha a convertir
    :type mongo_date: str | datetime
    :return: Hora local
    :rtype: datetime
    """
    if type(mongo_date) == str:
        try:
            a = datetime.strptime(mongo_date, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(arg_tz)
        except:
            a = datetime.strptime(mongo_date, '%Y-%m-%dT%H:%M:%S%z').astimezone(arg_tz)
        return a
    else:
        mongo_date = arg_tz.localize(mongo_date + relativedelta(hours=-1))
        return mongo_date


def store_datetime_as_string(new_date: datetime) -> str:
    """ Convierte la fecha dada a string

    :param new_date: Fecha a convertir
    :type new_date: datetime.datetime
    :return: el valor recibido por parametro como string
    :rtype: str
    """
    a = new_date.astimezone(arg_tz)
    a = str(a).replace(" ", "T")  # todo    ESTA FORMULA TODAVÍA NO SIRVE.
    return a


def localize(utc_datetime: datetime) -> datetime:
    """ Convierte a hora local

    :param utc_datetime: datetime en UTC+0
    :type utc_datetime: datetime
    :return: Hora recibida por parametro convertida a UTC+3 (hora local)
    :rtype: datetime
    """
    aware = utc_datetime.replace(tzinfo=pytz.utc)
    local_datetime = aware.astimezone(arg_tz)
    return local_datetime


def calculate_payment_date(period_init_date: datetime, cobro: str) -> datetime:
    """ Calcula el próximo día de pago para un cliente según la fecha de inicio de período.

    :param period_init_date: Fecha de inicio del período anterior al período del next_payment_date
    :type period_init_date: datetime
    :param cobro: los valores posibles son Mensual, Trimestral, Cuatrimestral, Semestral, Anual
    :type cobro: str
    :return: Fecha de pago
    :rtype: datetime
    """

    duration_map = {"Mensual": 1, "Trimestral": 3, "Cuatrimestral": 4, "Semestral": 6, "Anual": 12}
    period_day = period_init_date.day
    next_month = (period_init_date + relativedelta(months=duration_map[cobro]))
    end_of_next_month = calendar.monthrange(next_month.year, next_month.month)[1]

    if period_day <= DIAS_ANTICIPO_DE_PAGO:
        payment_month = period_init_date + relativedelta(months=(duration_map[cobro]-1))
        end_of_this_month = calendar.monthrange(payment_month.year, payment_month.month)[1]
        payment_day = end_of_this_month - (DIAS_ANTICIPO_DE_PAGO - period_day)
        return datetime(payment_month.year, payment_month.month, payment_day, MID_DAY_HOUR).astimezone(arg_tz)
    elif period_day > end_of_next_month:
        payment_day = end_of_next_month - DIAS_ANTICIPO_DE_PAGO
    else:
        payment_day = period_day - DIAS_ANTICIPO_DE_PAGO

    return datetime(next_month.year, next_month.month, payment_day, MID_DAY_HOUR).astimezone(arg_tz)



def set_next_vigency(next_payment_date: datetime) -> datetime:
    """ Establece la fecha de vigencia

    :param next_payment_date: Fecha del proximo pago
    :type next_payment_date: datetime
    :return: Fecha de vigencia segun la fecha del proximo pago
    :rtype: datetime
    """
    return (next_payment_date + relativedelta(days = DIAS_GRACIA + DIAS_ANTICIPO_DE_PAGO))


def get_periodo() -> str:
    """ Obtener el periodo

    :return: periodo actual con el formato MM/YYYY
    :rtype: str
    """    
    today = pytz.utc.localize(datetime.utcnow()).astimezone(arg_tz)
    period_init = today + relativedelta(days=DIAS_ANTICIPO_DE_PAGO)
    month = period_init.month
    year = period_init.year
    return f"{month}/{year}"


def last_payment_date_adjust(client):
    day = client["period_init_day"]
    proposed = today + relativedelta(days=DIAS_ANTICIPO_DE_PAGO)

    if proposed.day >= day:
        dif = proposed.day - day
    else:
        prev_month = proposed - relativedelta(months=1)
        month_days = calendar.monthrange(prev_month.year, prev_month.month)[1]
        dif = month_days - day + proposed.day
    return proposed - relativedelta(days=dif)
