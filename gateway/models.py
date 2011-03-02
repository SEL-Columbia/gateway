"""
Models for the Gateway software.
"""
import random
import uuid
import datetime
import urllib2
import urllib
import transaction
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import Numeric
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker, relation
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Allow
from pyramid.security import Everyone


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class RootFactory(object):

    __acl__ = [(Allow, Everyone, 'view'),
                (Allow, 'group:admins', 'admin') ]

    def __init__(self, request):
        pass


def get_now():
    return datetime.datetime.now()


class CommunicationInterface(Base):
    """
    Configures how the Gateway communicates with a Meter
    Subclasses
       KannelInterface
       Netbook interface
    """
    __tablename__ = 'communication_interface'
    type = Column(String)
    __mapper_args__ = {'polymorphic_on': type}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    provider = Column(String)
    location = Column(String)
    phone = Column(String)

    def __init__(self, name=None, provider=None, location=None):
        self.name = name
        self.provider = provider
        self.location = location

    def getUrl(self):
        return '/interface/index/%s' % self.id

    def __str__(self):
        return "Communication Interface %s" % self.name


class KannelInterface(CommunicationInterface):
    """
    Kannel Interface supports sending messages via a Kannel SMPP system.
    Stores some basic information about where to post url
    """
    __tablename__ = 'kannel_interface'
    __mapper_args__ = {'polymorphic_identity': 'kannel_interface'}

    id = Column(Integer,
                ForeignKey('communication_interface.id'),
                primary_key=True)
    host = Column(String)
    port = Column(Integer)
    username = Column(String)
    password = Column(String)

    def __init__(self, name=None, location=None, host=None, port=None,
                 provider=None, username=None, password=None):
        CommunicationInterface.__init__(self, name, provider, location)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.provider = provider

    def sendData(self, message):
        """
        Method to post message object to a Kannel server
        Requires a Message object
        Returns the results of a post
        XXX TODO, clean up results
        """
        data = urllib.urlencode({'username': self.username,
                                 'password': self.password,
                                 'to': message.number,
                                 'text': message.text })
        request = urllib2.Request(
               url='http://%s:%s/cgi-bin/sendsms?%s' % (self.host,
                                                        self.port,
                                                        data))
        return urllib2.urlopen(request)

    def sendMessage(self, number, text, incoming=None):
        session = DBSession()
        msg = KannelOutgoingMessage(
            number,
            text,
            incoming)
        session.add(msg)
        session.flush()
        self.sendData(msg)

    def sendJob(self, job, incoming=None):
        session = DBSession()
        msg = KannelJobMessage(job,
                               incoming=incoming)
        session.add(msg)
        session.flush()
        self.sendData(msg)


class NetbookInterface(CommunicationInterface):
    """
    Supports sending messages via a Netbook system.
    """
    __tablename__ = 'netbook_interface'
    __mapper_args__ = {'polymorphic_identity': 'netbook_interface'}

    id = Column(Integer, ForeignKey('communication_interface.id'),
                primary_key=True)

    def __init__(self, name=None, provider=None, location=None):
        CommunicationInterface.__init__(self, name, provider, location)

    def sendMessage(self, number, text, incoming):
        session = DBSession()
        msg = OutgoingMessage(number,
                        text,
                        incoming=incoming)
        session.add(msg)
        session.flush()
        return msg

    def sendJob(self, job, incoming=None):
        session = DBSession()
        msg = JobMessage(job,
                         incoming=incoming)
        session.add(msg)
        session.flush()
        return msg

class Meter(Base):
    """
    A class that repsents a meter in the gateway
    """
    __tablename__ = 'meter'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    name = Column(String)
    phone = Column(String)
    location = Column(String)
    status = Column(Boolean)
    date = Column(DateTime)
    battery = Column(Integer)
    panel_capacity = Column(Integer)
    communication_interface_id = Column(
        Integer,
        ForeignKey('communication_interface.id'))

    communication_interface = relation(
        CommunicationInterface,
        lazy=False,
        primaryjoin=communication_interface_id == CommunicationInterface.id)

    def __init__(self, name=None, phone=None, location=None,
                 battery=None, status=None,panel_capacity=None,
                 communication_interface_id=None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.phone = phone
        self.location = location
        self.date = get_now()
        self.battery = battery
        self.communication_interface_id = communication_interface_id
        self.panel_capacity = panel_capacity

    def getMessageType(self, job=False):
        """
        Issue, I need one place to look up what type of Job is going out.
        """
        error = 'Unsupported communication type'
        if job:
            if self.communication == 'netbook':
                return JobMessage
            elif self.communication == 'kannel':
                return KannelJobMessage
            else:
                raise NameError(error)
        else:
            if self.communication == 'netbook':
                return OutgoingMessage
            elif self.communication == 'kannel':
                return KannelOutgoingMessage
            else:
                raise NameError(error)

    def get_circuits(self):
        session = DBSession()
        return list(session.\
                    query(Circuit).\
                    filter_by(meter=self).order_by(Circuit.ip_address))

    def getJobs(self):
        session = DBSession()
        l = []
        for circuit in self.get_circuits():
            [l.append(x)
             for x in session.query(Job).\
                 filter_by(circuit=circuit).filter_by(state=True)]
        return l

    @staticmethod
    def slugify(name):
        slug = name.lower()
        return slug.replace(' ', '-')

    def getUrl(self):
        return "/meter/index/%s" % self.id

    def edit_url(self):
        return "/edit/Meter/%s" % self.id

    def remove_url(self):
        return "meter/remove/%s" % self.id

    def __str__(self):
        return "Meter %s" % self.name


class Account(Base):
    """
    """
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    lang = Column(String)

    def __init__(self, name="default", phone=None, lang="en"):
        self.name = name
        self.phone = phone
        self.lang = lang

    def url(self):
        return "account/index/%s" % self.id

    def __str__(self):
        return "Account id:%s phone:%s" % (self.id, self.phone)


class Circuit(Base):
    """
    """
    __tablename__ = "circuit"

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    date = Column(DateTime)
    pin = Column(String)
    meter_id = Column("meter", ForeignKey("meter.id"))
    meter  = relation(Meter,
                      lazy=False, primaryjoin=meter_id == Meter.id)
    energy_max = Column(Float)
    power_max = Column(Float)
    status = Column(Integer)
    ip_address = Column(String)
    credit = Column(Float)
    account_id  = Column(Integer, ForeignKey('account.id'))
    account  = relation(Account, lazy=False,
                        backref='circuit',
                        primaryjoin=account_id == Account.id)

    def __init__(self, meter=None, account=None, pin=None,
                 energy_max=None, power_max=None,
                 ip_address=None, status=1, credit=0):
        self.date = get_now()
        self.uuid = str(uuid.uuid4())
        self.pin = pin
        self.meter = meter
        self.energy_max = energy_max
        self.power_max = power_max
        self.ip_address = ip_address
        self.status = status
        self.credit = credit
        self.account = account

    @staticmethod
    def get_pin():
        chars = "qwertyuipasdfghjkzxcvbnm"
        ints = "23456789"
        return "%s%s" % ("".join(random.sample(chars, 3)),
                      "".join(random.sample(ints, 3)))

    def get_jobs(self):
        session = DBSession()
        return session.query(Job).\
            filter_by(circuit=self).order_by(Job.id.desc())

    def get_logs(self):
        session = DBSession()
        return session.query(PrimaryLog).\
            filter_by(circuit=self).order_by(PrimaryLog.id.desc())

    def genericJob(self, cls, incoming=""):
        session = DBSession()
        interface = self.meter.communication_interface
        job = cls(self)
        session.add(job)
        session.flush()
        interface.sendJob(job,
                          incoming=incoming)

    def turnOn(self, incoming=""):
        self.genericJob(TurnOn, incoming)

    def turnOff(self, incoming=""):
        self.genericJob(TurnOff, incoming)

    def ping(self, request=None):
        self.genericJob(Cping)

    def get_rich_status(self):
        if self.status == 0:
            return "Off"
        elif self.status == 1:
            return "On"

    def url(self):
        return "/circuit/index/%s" % self.id

    def getUrl(self):
        return "/circuit/index/%s" % self.id

    def edit_url(self):
        return "/edit/Circuit/%s" % self.id

    def remove_url(self):
        return "/circuit/remove/%s" % self.id

    def toggle_url(self):
        return "/circuit/toggle/%s" % self.id

    def toJSON(self):
        return {"id": self.id,
                 "ip_address": self.ip_address,
                 "date": str(self.date),
                 "url": self.url(),
                 "pin": self.pin,
                 "uuid": self.uuid,
                 "energy_max": self.energy_max,
                 "power_max": self.power_max,
                 "status": self.status }

    def __str__(self):
        return "Circuit id:%s account:%s" % (self.id, self.pin)


class Message(Base):
    """
    Abstract class for all messages
    """
    __tablename__  = "message"
    type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': type}
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sent = Column(Boolean)
    number = Column(String)
    uuid = Column(String)

    def __init__(self, number=None, uuid=None, sent=False):
        self.date = get_now()
        self.sent = sent
        self.number = number
        self.uuid = uuid
        
    def url(self):
        return "message/index/%s" % self.uuid

    def get_incoming(self):
        session = DBSession()
        # I hope no one ever sees this. God I am a hack.
        if isinstance(self,
                      OutgoingMessage)\
                      or isinstance(self,
                                    JobMessage)\
                      or isinstance(self,
                                    KannelOutgoingMessage)\
                      or isinstance(self, KannelJobMessage):

            incoming = session.query(IncomingMessage).\
                       filter_by(uuid=self.incoming).first()
            if incoming:
                return incoming.text
            else:
                return "Message not based on incoming message"
        else:
            return "Incoming message"

    def toDict(self):
        return {"number": int(self.number),
                 "time": str(self.date),
                 "uuid": self.uuid,
                 "text": self.text,
                 "id": self.id }

    def __unicode__(self):
        return "Messsage <%s>" % self.uuid

    def respond(self):
        return


class TestMesssage(Message):
    """
    Message for testing communication interfaces
    """
    __tablename__ = "test_message"
    __mapper_args__ = {'polymorphic_identity': 'test_message'}
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    text = Column(String)    
    communication_interface_id = Column(
        Integer,
        ForeignKey('communication_interface.id'))
    communication_interface = relation(
        CommunicationInterface,
        lazy=False,
        primaryjoin=communication_interface_id == CommunicationInterface.id)
    
    def __init__(self, text=None,number=None, communication_interface=None):
        Message.__init__(self,number=number,uuid = uuid.uuid4())
        self.communication_interface = communication_interface                     
    
      
class IncomingMessage(Message):
    """
    """
    __tablename__ = "incoming_message"
    __mapper_args__ = {'polymorphic_identity': 'incoming_message'}
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    text = Column(String)
    communication_interface_id = Column(
        Integer,
        ForeignKey('communication_interface.id'))
    communication_interface = relation(
        CommunicationInterface,
        lazy=False,
        primaryjoin=communication_interface_id == CommunicationInterface.id)

    def __init__(self, number=None, text=None, uuid=None,
                 communication_interface=None,
                 sent=True):
        Message.__init__(self, number, uuid)
        self.text = text
        self.communication_interface = communication_interface


class OutgoingMessage(Message):
    """
    """
    __tablename__ = "outgoing_message"
    __mapper_args__ = {'polymorphic_identity': 'outgoing_message'}
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    text = Column(String)
    incoming = Column(String, nullable=True)

    def __init__(self, number=None, text=None, incoming=None):
        Message.__init__(self, number, str(uuid.uuid4()))
        self.text = text
        self.incoming = incoming


class KannelOutgoingMessage(Message):
    """
    A class for sending messages to Kannel... Kind of a hack right now
    In the __init__ function we send a post to the Kannel address
    """
    __tablename__ = 'kannel_outgoing_message'
    __mapper_args__ = {'polymorphic_identity': 'kannel_outgoing_message'}
    id = Column(Integer, ForeignKey('message.id'), primary_key=True)
    text = Column(String)
    incoming = Column(String, nullable=True)

    def __init__(self, number=None, text=None, incoming=None):
        Message.__init__(self, number, str(uuid.uuid4()))
        self.text = text
        self.incoming = incoming


class TokenBatch(Base):
    """
    A class that groups tokens based on when they are created
    """
    __tablename__ = "tokenbatch"
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    created = Column(DateTime)

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.created = datetime.datetime.now()

    def getUrl(self):
        return "token/show_batch/%s" % self.uuid

    def get_tokens(self):
        session = DBSession()
        return session.query(Token).filter_by(batch=self)


class Token(Base):

    __tablename__  = "token"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    token = Column(Numeric)
    value = Column(Numeric)
    state = Column(String)
    batch_id = Column(Integer, ForeignKey('tokenbatch.id'))
    batch  = relation(TokenBatch, lazy=False,
                      primaryjoin=batch_id == TokenBatch.id)

    def __init__(self, token=None, batch=None, value=None, state="new"):
        self.created = datetime.datetime.now()
        self.token = token
        self.value = value
        self.state = state
        self.batch = batch

    @staticmethod
    def get_random():
        r = int(random.random() * 10 ** 11)
        if r > 10 ** 10: return r
        else: return Token.get_random()

    def toDict(self):
        return {
            "id": self.id,
            "state": self.state,
            "value": int(self.value),
            "token": int(self.token),
            "created": self.created.ctime()}


class Alert(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(String)
    message_id = Column(Integer, ForeignKey('message.id'))
    message = relation(Message, lazy=False,
                       primaryjoin=message_id == Message.id)
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit, lazy=False,
                       primaryjoin=circuit_id == Circuit.id)

    def __init__(self, text=None, circuit=None, message=None):
        self.date = get_now()
        self.circuit = circuit
        self.message = message


class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    uuid = Column(String)
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit, lazy=False,
                       primaryjoin=circuit_id == Circuit.id)

    def __init__(self, date=None, circuit=None):
        self.date = date
        self.uuid = str(uuid.uuid4())
        self.circuit = circuit


class SystemLog(Base):
    __tablename__ = "system_log"
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    text = Column(String)
    created = Column(String)

    def __init__(self, text=None):
        self.uuid = str(uuid.uuid4())
        self.text = text
        self.created = get_now()


class SystemAlert(object):
    """
    """
    def __init__(self, ):
        """
        """


class PrimaryLog(Log):
    __tablename__ = "primary_log"
    __mapper_args__ = {'polymorphic_identity': 'primary_log'}
    id = Column(Integer, ForeignKey('log.id'), primary_key=True)
    watthours = Column(Float)
    use_time = Column(Float)
    status = Column(Integer)
    created = Column(DateTime)
    credit = Column(Float, nullable=True)
    status = Column(Integer)

    def __init__(self, date=None, circuit=None, watthours=None,
                 use_time=None, status=None, credit=0):
        Log.__init__(self, date, circuit)
        self.circuit = circuit
        self.watthours = watthours
        self.use_time = use_time
        self.credit = credit
        self.created = get_now()
        self.status = status

    def get_property(self, string):
        if string == "credit":
            return self.credit
        elif string == "watt":
            return self.watthours
        elif string == "power":
            return self.use_time
        else:
            raise NameError("Unable to find Property")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    _type = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': _type}
    uuid  = Column(String)
    start = Column(String)
    end = Column(String)
    state = Column(Boolean)
    circuit_id = Column(Integer, ForeignKey('circuit.id'))
    circuit = relation(Circuit,
                       lazy=False, primaryjoin=circuit_id == Circuit.id)

    def __init__(self, circuit=None, state=True):
        self.uuid = str(uuid.uuid4())
        self.start = get_now()
        self.circuit = circuit
        self.state = state

    def getMessage(self, session):
        if len(self.job_message) is not 0:
            incoming_uuid = job.job_message[0]
        elif len(self.kannel_job_message) is not 0:
            incoming_uuid = job.kannel_job_message[0].incoming
        return session.query(IncomingMessage).\
                            filter_by(uuid=incoming_uuid).first()


    def url(self):
        return "jobs/job/%s/" % self.id

    def toDict(self):
        return {"uuid": self.uuid,
                "state": self.state,
                "date": self.start,
                "type": self._type}

    def __str__(self):
        return "job"


class AddCredit(Job):
    __tablename__ = "addcredit"
    __mapper_args__ = {'polymorphic_identity': 'addcredit'}
    description = "This job adds energy credit to the remote circuit"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    credit = Column(Integer)

    def __init__(self, credit=None, circuit=None):
        Job.__init__(self, circuit)
        self.credit = credit

    def __str__(self):
        return "job=cr&jobid=%s&cid=%s&amt=%s;" % (self.id,
                                                self.circuit.ip_address,
                                                float(self.credit))


class TurnOff(Job):
    __tablename__ = "turnoff"
    __mapper_args__ = {'polymorphic_identity': 'turnoff'}
    description = "This job turns off the circuit on the remote meter"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, circuit=None):
        Job.__init__(self, circuit)

    def __str__(self):
        return "job=coff&jobid=%s&cid=%s;" % (self.id, self.circuit.ip_address)


class TurnOn(Job):
    __tablename__ = "turnon"
    __mapper_args__ = {'polymorphic_identity': 'turnon'}
    description = "This job turns on the circuit off the remote meter"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, circuit=None):
        Job.__init__(self, circuit)

    def __str__(self):
        return "job=con&jobid=%s&cid=%s;" % (self.id, self.circuit.ip_address)


class Mping(Job):
    """ Job that allows the admin to 'ping' a meter"""
    __tablename__ = 'mping'
    __mapper_args__ = {'polymorphic_identity': 'mping'}
    description = "This job turns on the circuit off the remote meter"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, meter=None):
        Job.__init__(self, self.getMain(meter))

    def getMain(self, meter):
        return meter.get_circuits()[0]

    def __str__(self):
        return "job=mping&jobid=%s" % self.id


class Cping(Job):
    """ Job that allows the admin to 'ping' a meter"""
    __tablename__ = 'cping'
    __mapper_args__ = {'polymorphic_identity': 'cping'}
    description = "This job turns on the circuit off the remote meter"
    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, circuit=None):
        Job.__init__(self, circuit)

    def __str__(self):
        return "job=cping&jobid=%s&cid=%s" % (self.id, self.circuit.ip_address)


class JobMessage(Message):
    """
    A class that repsents the text message for each message
    """
    __tablename__ = "job_message"
    __mapper_args__ = {'polymorphic_identity': 'job_message'}
    id = Column(Integer,
                ForeignKey('message.id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    job = relation(Job, lazy=False,
                   backref='job_message', primaryjoin=job_id == Job.id)
    incoming = Column(String)
    text = Column(String)

    def __init__(self, job=None, incoming=""):
        Message.__init__(self, job.circuit.meter.phone, str(uuid.uuid4()))
        self.uuid = str(uuid.uuid4())
        self.job = job
        self.incoming = incoming
        self.text = job.__str__()

    def getIndexUrl(self, request):
        return "%s/message/index/%s" % (request.application_url, self.id)


class KannelJobMessage(Message):
    """
    """
    __tablename__ = "kannel_job_message"
    __mapper_args__ = {'polymorphic_identity': 'kannel_job_message'}
    id = Column(Integer,
                ForeignKey('message.id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    job = relation(Job, lazy=False,
                   backref='kannel_job_message', primaryjoin=job_id == Job.id)
    incoming = Column(String)
    text = Column(String)

    def __init__(self, job=None, incoming=""):
        Message.__init__(self, job.circuit.meter.phone, str(uuid.uuid4()))
        self.uuid = str(uuid.uuid4())
        self.job = job
        self.incoming = incoming
        self.text = job.__str__()


def populate():
    DBSession.flush()
    transaction.commit()


def initialize_sql(db_string, db_echo=False):
    engine = create_engine(db_string, echo=db_echo)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        pass
