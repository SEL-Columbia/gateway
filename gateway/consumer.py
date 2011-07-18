"""
Functions to response to consumer messages
"""
from datetime import datetime
from datetime import timedelta
from gateway.models import DBSession
from gateway.models import Circuit
from gateway.models import Token
from gateway.models import AddCredit
from gateway.utils import make_message_body

delimiter = "."


def get_circuit(message):
    """Queris the database to find circuit
    Returns the circuit or false
    """
    session = DBSession()
    pin = message.text.split(delimiter)[1].lower()
    circuit = session.query(Circuit).filter_by(pin=pin).first()
    if circuit:
        return circuit
    else:
        interface = message.communication_interface
        interface.sendMessage(
            message.number,
            make_message_body("no-circuit.txt", lang=message.language),
            incoming=message.uuid)
        return False


def get_token(message):
    """Tries to match message to token."""
    session = DBSession()
    tokenNumber = message.text.split(delimiter)[2]
    token = session.query(Token).\
        filter_by(state="new").filter_by(token=tokenNumber).first()
    if token:
        return token
    else:
        interface = message.communication_interface
        interface.sendMessage(
            message.number,
            make_message_body("no-token.txt", lang=message.language),
            incoming=message.uuid)
        return False


def get_balance(message):
    """Allows users to check blance"""
    circuit = get_circuit(message)
    language = circuit.account.lang
    if circuit:
        interface = circuit.meter.communication_interface
        interface.sendMessage(
            message.number,
            make_message_body("bal.txt",
                              lang=language,
                              account=circuit.pin,
                              credit=circuit.credit),
            incoming=message.uuid)


def set_primary_contact(message):
    """Allows users to set their primary contact number"""
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:
        interface = circuit.meter.communication_interface
        new_number = message.text.split(delimiter)[2]
        old_number = circuit.account.phone
        messageBody = make_message_body("tel.txt",
                                        lang=circuit.account.lang,
                                        old_number=old_number,
                                        new_number=new_number)
        interface.sendMessage(
            message.number,
            messageBody,
            incoming=message.uuid)
        if new_number != message.number:
            interface.sendMessage(
                new_number,
                messageBody,
                incoming=message.uuid)
        account = circuit.account
        account.phone = new_number
        session.merge(account)


def add_credit(message):
    """Allows consumer to add credit to their account.
    Sends an outgoing message to the consumer.
    """
    session = DBSession()
    circuit = get_circuit(message)
    token = get_token(message)
    if circuit:
        interface = circuit.meter.communication_interface
        if token:
            job = AddCredit(circuit=circuit, credit=token.value, token=token)
            session.add(job)
            session.flush()
            interface.sendJob(job,
                              incoming=message.uuid)
            session.merge(circuit)
            session.flush()


def turn_circuit_on(message):
    """Allows the consumer to turn their account on."""
    circuit = get_circuit(message)
    if circuit:
        circuit.turnOn(incoming=message.uuid)


def turn_circuit_off(message):
    """ Creates a new job called turn_off """
    circuit = get_circuit(message)
    if circuit:
        circuit.turnOff(incoming=message.uuid,)


def set_primary_lang(message, *kwargs):
    """ Allows consumer to set their account lang
    """


def use_history(message, **kwargs):
    """
    Calculates use based on last 30 days of account activity
    account-number
    avg watt hours pre day :  (total watthours for time/number of days)
    max watt hours         :  max(watthours)
    min watt hours         :  min(watthours)
    """
    circuit = get_circuit(message)
    if circuit:
        now = datetime.now()
        last_month = now - timedelta(days=30)
        interface = circuit.meter.communication_interface
        message = make_message_body('use.txt',
                                    lang=circuit.account.lang,
                                    account=circuit.pin,
                                    amount=circuit.calculateCreditConsumed(dateStart=last_month, dateEnd=now))
        interface.sendMessage(circuit.account.phone, message)
