import re
from datetime import datetime
from urlparse import parse_qs
from gateway.models import DBSession
from gateway.models import Circuit
from gateway.models import Meter
from gateway.models import SystemLog
from gateway.models import TestMessage
from gateway import meter as meter_funcs
from gateway.meter import make_pcu_logs
import compactsms


def reduce_message(message):
    """
    """
    m = {}
    for k, v in message.iteritems():
        m[k] = v[0]
    return m


def clean_message(messageRaw):
    """  Does the basic cleaning of meter messages.
    Step 1. Removes ()
    Step 2. Returns a new dict with only the first value
    of each key value pair
    """
    messageBody = messageRaw.text.lower()
    messageBody = messageBody.strip(")").strip("(")
    message = reduce_message(parse_qs(messageBody))
    message['meta'] = messageRaw
    return message


def add_test_message(message):
    session = DBSession()
    msg = TestMessage(datetime.now(), message.text)
    session.add(msg)
    session.flush()


def findMeter(message):
    """
    Takes a message object and returns either a meter or none.
    Looks up the meter based on the message's number.
    """
    session = DBSession()
    meter = session.query(Meter).filter_by(phone=str(message.number)).first()
    if meter:
        return meter
    else:
        return False


def findCircuit(message, meter):
    """Looks up circuit from meter and message.
    """
    session = DBSession()
    circuit = session.query(Circuit).\
        filter_by(ip_address=message["cid"]).\
        filter_by(meter=meter).first()
    if circuit:
        return circuit


def parse_meter_message(message):
    """ Parse message from the Meter. Takes a message object and returns
    nothing. Logs an exception if the message is unable to be parsed.
    """
    session = DBSession()
    meter = findMeter(message)
    # compressed primary logs
    if re.match("^\(l.*\)$", message.text):
        inflatedlogs = compactsms.inflatelogs([message.text])
        for log in inflatedlogs:
            m = reduce_message(parse_qs(log))
            circuit = findCircuit(m, meter)
            meter_funcs.make_pp(m, circuit, session)
    # old messages
    elif re.match("^\(.*\)$", message.text.lower()):
        if message.text.startswith('(pcu'):
            make_pcu_logs(message, meter, session)
        else:
            messageDict = clean_message(message)
            if messageDict["job"] == "delete":
                getattr(meter_funcs,
                        "make_" + messageDict["job"])(messageDict, session)
            else:
                circuit = findCircuit(messageDict, meter)
                if circuit:  # double check that we have a circuit
                    if messageDict['job'] == "pp":
                        getattr(meter_funcs,
                                "make_" + messageDict["job"])(messageDict,
                                                             circuit,
                                                             session)
                    elif messageDict['job'] == "alert":
                        getattr(meter_funcs,
                                "make_" + messageDict["alert"])(messageDict,
                                                               circuit,
                                                               session)
    else:
        session.add(SystemLog(
                'Unable to parse message %s' % message.uuid))
