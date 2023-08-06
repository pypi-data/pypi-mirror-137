import mailchimp_transactional as MailchimpTransactional
from .init_creds import mailchimp_key, test
from mailchimp_transactional.api_client import ApiClientError
import iso8601
import typing

mailchimp = MailchimpTransactional.Client(mailchimp_key)


def send_mail_to_template(receiver: dict, template: str, plan: str = "None") -> dict:
    """ Enviar mail con un template determinado

    :param receiver: objeto de cliente del destinatario
    :type receiver: dict
    :param template: nombre del template
    :type template: str
    :param plan: nombre del plan, defaults to "None"
    :type plan: str, optional
    :return: informacion del mail
    :rtype: dict
    """
    try:
        sdate = receiver["last_subscription_date"].strftime("%d/%m/%Y")

    except AttributeError:
        sdate = iso8601.parse_date(receiver["last_subscription_date"]).strftime("%d/%m/%Y")
    except:
        return {}

    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "apellido", "content": receiver["apellido"]},
                   {"name": "documento", "content": receiver["documento"]},
                   {"name": "plan", "content": plan},
                   {"name": "fecha_subscripcion", "content": sdate}
                   ]
    send_mail(receiver["email"], global_vars, template)


def send_alert(reciever_mail: str, proceso: str, mensaje: str, referencia: str) -> typing.Union[dict, None]:
    """ Enviar mensaje de alerta a ignacio@muvinai.com
    :param reciever_mail: email de quien recibe la alerta
    :type reciever_mail: str
    :param proceso: nombre del proceso
    :type proceso: str
    :param mensaje: mensaje
    :type mensaje: str
    :param referencia: referencia
    :type referencia: str
    :return: Respuesta de mailchimp o None en caso de error
    :rtype: dict | None
    """

    global_vars = [{"name": "proceso", "content": proceso},
                   {"name": "mensaje", "content": mensaje},
                   {"name": "referencia", "content": referencia}
                   ]
    return send_mail(reciever_mail, global_vars, "alertas")


def send_mail_inactivo(receiver):
    """ Enviar mail indicando al cliente que está inactivo.

        :param receiver: documento de cliente del destinatario
        :type receiver: dict
        :return: informacion del mail
        :rtype: dict
        """

    global_vars = [{"name": "nombre", "content": receiver["nombre"]}]
    return send_mail(receiver["email"], global_vars, "inactivo")


def send_mail_rejected_payment(receiver):
    """ Enviar mail indicando al cliente que sus pagos están rechazados, y que agregue una nueva tarjeta.

        :param receiver: documento de cliente del destinatario
        :type receiver: dict
        :return: informacion del mail
        :rtype: dict
        """

    global_vars = [{"name": "nombre", "content": receiver["nombre"]}]
    return send_mail(receiver["email"], global_vars, "inactivo")


def send_mail(receiver_mail, params, template):
    """ Estructura y envía mail

    :param receiver_mail: mail del receptor
    :type receiver_mail: str
    :param params: lista de objetos que son parámetros a pasar al template
    :type params: list
    :param template: nombre del template
    :type template: str

    :return: informacion del mail
    :rtype: dict
    """
    print("Enviando mail" + template)
    sender = 'no-responder@sportclub.com.ar'
    if test:
        to_mail = [{"email": "ignacio@muvinai.com"}]
    else:
        to_mail = [{"email": receiver_mail}]
    msg = {
        "from_email": sender,
        "from_name": "SportClub",
        "to": to_mail,
        "global_merge_vars": params}

    try:
        response = mailchimp.messages.send_template(
            {"template_name": template, "template_content": [], "message": msg})
        print(response)
        return response[0]
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return {}

