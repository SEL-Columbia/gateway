"""
Module for SS Gateway.
Handles all of the meter communcation
"""
from datetime import datetime
from gateway.models import Job
from gateway.models import SystemLog
from gateway.models import PrimaryLog
from gateway.models import IncomingMessage
from gateway.models import AddCredit
from gateway.models import PCULog
from gateway.utils import make_message_body


def respond_to_add_credit(job, circuit, session):
    """
    Function to excute the actions need after the gateways gets a job
    delete about a add credit job.
    """
    token = job.token
    token.state = 'used'
    session.merge(token)
    session.flush()
    return make_message_body("credit.txt",
                             lang=circuit.account.lang,
                             account=circuit.pin,
                             status=circuit.get_rich_status(),
                             credit=circuit.credit)


def find_job_message(job, session):
    """
    Function to look up a job's creating message
    Takes a job and a db session
    Returns a message object or none
    """
    try:
        if len(job.job_message) is not 0:
            incoming_uuid = job.job_message[0].incoming
        elif len(job.kannel_job_message) is not 0:
            incoming_uuid = job.kannel_job_message[0].incoming
        return session.query(IncomingMessage)\
            .filter_by(uuid=incoming_uuid).first()
    except Exception, e:
        print(e)


def update_circuit(msgDict, circuit, session):
    """
    Function to update circuit based on message dictionary parsed from job delete.
    Takes message dictionary, circuit object and session object.
    """
    circuit.status = int(msgDict.get("status", circuit.status))
    circuit.credit = float(msgDict.get("cr", circuit.credit))
    session.merge(circuit)
    session.flush()


def update_job(job, session):
    """
    Function to update job to current time and change the job state
    Takes a job and a db session
    Returns none
    """
    job.state = False
    job.end = datetime.now()
    session.merge(job)
    session.flush()


def make_delete(msgDict, session):
    """
    Responses to a delete messsage from the meter.
    """
    originMsg = None
    messageBody = None
    # locate the job from the job id
    job = session.query(Job).get(msgDict["jobid"])
    if job:
        circuit = job.circuit
        interface = circuit.meter.communication_interface

        originMsg = find_job_message(job, session)
        update_job(job, session)
        update_circuit(msgDict, circuit, session)
        if isinstance(job, AddCredit):
            messageBody = respond_to_add_credit(job, circuit, session)
        elif job._type == "turnon" or job._type == "turnoff":
            messageBody = make_message_body("toggle.txt",
                                            lang=circuit.account.lang,
                                            account=circuit.pin,
                                            status=circuit.get_rich_status(),
                                            credit=circuit.credit)
        else:
            pass
            # double to check we have a message to send
        if messageBody and originMsg:
            interface.sendMessage(
                originMsg.number,
                messageBody,
                incoming=originMsg.uuid)
            session.merge(job)
        else:
            pass


def make_pcu_logs(message, meter, session):
    """
    (pcu#
    timestamp: 11062200#
    cumltve-kwh-solar: 0.00,
    cumltve-khw-bat-charge :0.00,
    cumltve-kwh-dischage: 0.00,
    battery_volds: 0.00,
    battery_charge: 48.01,
    battery_discharge: 0.00,
    solar_amps: 0.00,
    solar_volts: 0.00)
    """
    data = message.text.strip('(').strip(')').split(',')
    header = data[0].split("#")
    timestamp = datetime.strptime(header[1], '%Y%m%d%H')
    log = PCULog(datetime.now(),
                 timestamp,
                 float(header[2]),
                 float(data[1]),
                 float(data[2]),
                 float(data[3]),
                 float(data[4]),
                 float(data[5]),
                 float(data[6]),
                 float(data[7]),
                 meter)
    session.add(log)
    session.flush()


def make_pp(message, circuit, session):
    """
    Saves primary parameter to the database.
    """
    try:
        date = datetime.strptime(message['ts'], "%Y%m%d%H")
        log = PrimaryLog(
            date=date,
            circuit=circuit,
            watthours=message["wh"],
            use_time=message["tu"],
            credit=message.get("cr"),
            status=int(message["status"]))
        # override the credit and status value from the meter.
        circuit.credit = log.credit
        circuit.status = log.status
        session.add(log)
        session.merge(circuit)
    except Exception as e:
        print message
        print e


def make_nocw(message, circuit, session):
    """
    Sends a no credit alert to the consumer
    """
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("nocw-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin))
    session.flush()
    log = SystemLog(
        "No credit alert for circuit %s sent to %s" % (circuit.pin,
                                                        circuit.account.phone))
    session.add(log)


def make_lcw(message, circuit, session):
    """
    Sends a low credit alert to the consumer.
    """
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("lcw-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)
    session.flush()


def make_md(message, circuit, session):
    log = SystemLog(
        "Meter %s just falied, please investagte." % circuit.meter.name)
    session.add(log)


def make_ce(message, circuit, session):
    log = SystemLog(
        "Circuit %s just failed, please investagate." % circuit.ip_address)
    session.add(log)


def make_pmax(message, circuit, session):
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("power-max-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)


def make_emax(message, circuit, session):
    interface = circuit.meter.communication_interface
    interface.sendMessage(
        circuit.account.phone,
        make_message_body("energy-max-alert.txt",
                     lang=circuit.account.lang,
                     account=circuit.pin),
        incoming=message['meta'].uuid)


def make_sdc(message, circuit, session):
    pass
