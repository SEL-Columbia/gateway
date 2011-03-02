"""
Handler objects of web interface
"""
import datetime
import csv
from urlparse import parse_qs
import uuid
import cStringIO
import simplejson

from dateutil import parser
from webob import Response
from webob.exc import HTTPFound

from pyramid_handlers import action
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget

from sqlalchemy import or_, desc
from formalchemy import FieldSet, Field
from formalchemy import Grid

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy 

from gateway import dispatcher
from gateway import models
from gateway.models import DBSession
from gateway.models import Meter
from gateway.models import Circuit
from gateway.models import PrimaryLog
from gateway.models import Job
from gateway.models import AddCredit
from gateway.models import Account
from gateway.models import TokenBatch
from gateway.models import Token
from gateway.models import Message
from gateway.models import IncomingMessage
from gateway.models import OutgoingMessage
from gateway.models import SystemLog
from gateway.models import Mping
from gateway.models import CommunicationInterface
from gateway.models import TestMesssage
from gateway.security import USERS
from gateway.utils import get_fields
from gateway.utils import model_from_request
from gateway.utils import make_table_header
from gateway.utils import make_table_data

breadcrumbs = [{"text":"Manage Home", "url":"/"}]

    

class RestView(object):
    """
    Abstract class to make doing views easier.
    """
    def __init__(self, request):
        self.request = request

    def __call__(self):
        method = self.request.method.lower()
        if hasattr(self, method):
            func = getattr(self, method)
            return func()
        else:
            raise NameError("Method not supported")

    def look_up_class(self, module=models):
        """
        Looks up a class from a request.
        Returns the class.
        """
        try:
            cls = getattr(module, self.request.matchdict.get('class'))
            return cls
        except:
            return Response("Unable to locate resource")

    def look_up_instance(self):
        if self.cls is not None:
            return self.session.query(self.cls).get(self.request.matchdict['id'])

class AddClass(RestView):
    """
    An genertic view that allows for adding models to our system.
    """
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.cls = self.look_up_class()

    def get(self):
        fs = FieldSet(self.cls,session=self.session)
        return {'fs': fs, 'cls': self.cls}
    def post(self):
        fs = FieldSet(self.cls, session=self.session).\
             bind(self.cls(),data=self.request.POST)
        if fs.validate():
            fs.sync()
            self.session.flush()
            return HTTPFound(location=fs.model.getUrl())
        else:
            return {'fs': fs, 'cls' : self.cls}

class EditModel(RestView):
    """
    A view that allows models to be edited.  Takes the class name as a
    string parameter and returns the correct html form.
    """    
    def __init__(self,request ):
        self.request = request
        self.session = DBSession()
        self.cls = self.look_up_class()
        self.instance = self.look_up_instance()

    def get(self):
        fs = FieldSet(self.instance)
        return {'fs': fs,
                'instance': self.instance,
                'cls': self.cls}

    def post(self):
        fs = FieldSet(self.instance,
                      data=self.request.POST)
        if fs.validate():
            fs.sync()
            self.session.flush()
            return HTTPFound(location=fs.model.getUrl())
        

class GraphView(RestView):
    """
    """    
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.cls = self.look_up_class()
        self.instance = self.look_up_instance()
        self.column = self.request.params.get('column',None)
        self.figsize = tuple(map(lambda item: int(item),
                                 self.request.params.get('figsize',
                                                         "1,2").split(",")))
        self.columns = self.request.params.get('columns',None)

    def get_circuit_logs(self, circuit):
        return self.session.query(PrimaryLog).filter_by(circuit=circuit)

    def graphCircuit(self):
        fig = Figure(figsize=self.figsize)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111,
                             title='%s graph for %s' % (FieldSet.prettify(
                                 self.column), self.instance))
        logs = self.get_circuit_logs(self.instance)            
        x = [date2num(log.date) for log in logs]
        y = [getattr(log,self.column) for log in logs]
        ax.plot_date(x,y,linestyle='-')
        ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
        ax.set_xlabel('Date')
        output = cStringIO.StringIO()
        canvas.print_figure(output)        
        return Response(
            body=output.getvalue(),
            content_type='image/png')

    def graphMeter(self):
        return Response()

    def get(self):
        if isinstance(self.instance, Circuit):
            return self.graphCircuit()
        elif isinstance(self.instance, Meter):
            return self.graphMeter()
        else:
            return Response("Class not supported")

class AlertHandler(object):
    """
    """        
    def __init__(self, request):
        self.request = request
        self.session = DBSession()

    @action(renderer='alerts/make.mako', permission='admin')
    def make(self):
        return {'interfaces':self.session.query(CommunicationInterface).all()}

    @action(permission="admin")
    def send_test(self):
        interface = self.session\
                    .query(CommunicationInterface)\
                    .get(self.request.params['interface'])
        number = self.request.params['number']
        text = self.request.params['text']
        msg = interface.sendMessage(number,text)
        return HTTPFound(location="%s/message/index/%s" %
                         (self.request.application_url,msg.uuid))
    

class Dashboard(object):
    """
    Home page for the gateway
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    @action(renderer='index.mako', permission='view')
    def index(self):
        meters = Grid(Meter, self.session.query(Meter).all())
        meters.configure(readonly=True, exclude=meters._get_fields()[:2])
        meters.insert(meters._get_fields()[2],
                      Field('Name',
                            value=lambda item:'<a href=%s>%s</a>' % (item.getUrl()
                                                                     ,item.name)))

        interfaces = Grid(CommunicationInterface,
                          self.session.query(CommunicationInterface).all())
        interfaces.configure(readonly=True, exclude=[interfaces._get_fields()[0]])
        interfaces.append(
            Field('Name',
                  value=lambda item:'<a href=%s>%s</a>' % (item.getUrl()
                                                           ,item.name)))

        logs = Grid(SystemLog,
                    self.session.query(SystemLog)\
                    .order_by(desc(SystemLog.created)).all())
        logs.configure(readonly=True)
        return {
            'interfaces': interfaces,
            'logged_in': authenticated_userid(self.request),
            'tokenBatchs': self.session.query(TokenBatch).all(),
            'logs': logs,
            'meters': meters,
            'breadcrumbs': self.breadcrumbs }

    @action(renderer="dashboard.mako", permission="admin")
    def dashboard(self):
        return {
            "logged_in": authenticated_userid(self.request)}

    @action(permission="admin")
    def add_tokens(self):
        batch = TokenBatch()
        self.session.add(batch)
        amount = self.request.params.get("amount", 100)
        value = int(self.request.params.get("value", 10))
        for number in xrange(0, int(amount)):
            self.session.add(Token(
                    token=Token.get_random(),
                    value=value,
                    batch=batch))
        return HTTPFound(location=self.request.application_url)

    @action(permission="admin")
    def upload_tokens(self):
        csvReader = csv.reader(self.request.params['csv'].file, delimiter=',')
        batch = TokenBatch()
        self.session.add(batch)
        header = csvReader.next()
        for line in csvReader:
            self.session.add(Token(
                    token=line[1],
                    value=line[2],
                    batch=batch))
        return HTTPFound(location=self.request.application_url)

    @action()
    def system_logs(self):
        return Response(
            simplejson.dumps(
                [x.text for x in self.session.query(SystemLog).all()]))

    @action(permission="admin")
    def send_message(self):
        params = self.request.params
        msgClass = getattr(models, params['delivery-type'])
        msg = msgClass(
                number=params.get("number"),
                text=params.get("text"))
        self.session.add(msg)
        self.session.flush()
        return HTTPFound(location=self.request.application_url)


class ManageHandler(object):
    """
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer='manage/index.mako')
    def index(self):
        return {
            'logged_in': authenticated_userid(self.request),
            'breadcrumbs': self.breadcrumbs }


class UserHandler(object):

    def __init__(self, request):
        self.request = request

    @action(renderer="login.mako")
    def login(self):
        came_from = self.request.params.get('came_from',)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in self.request.params:
            login = self.request.params['login']
            password = self.request.params['password']
            if USERS.get(login) == password:
                headers = remember(self.request, login)
                return HTTPFound(location="/",
                                 headers=headers)
            message = 'Failed login'
        return {
            'message': message,
            'url': self.request.application_url + '/login',
            'came_from': came_from,
            'login': login,
            'password': password }

    def logout(self):
        headers = forget(self.request)
        return HTTPFound(
            headers=headers,
            location=self.request.application_url)


class InterfaceHandler(object):
    """
    A handler for managing the interfaces.
    """

    def __init__(self, request):
        self.breadcrumbs = breadcrumbs
        self.request = request
        self.session = DBSession()
        self.interface = self.session.query(
            CommunicationInterface).get(self.request.matchdict.get('id'))

    @action(renderer='interface/index.mako', permission='admin')
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Interface overview'})
        testmessage = FieldSet(TestMesssage,session=self.session)
        return {'interface': self.interface,
                'breadcrumbs': breadcrumbs,
                'testmessage': testmessage,
                'fields': get_fields(self.interface),
                'logged_in': authenticated_userid(self.request)}

    def save_and_parse_message(self, origin, text, id=None):
        """
        """
        if id is None:
            id = str(uuid.uuid4())
        message = IncomingMessage(origin, text, id, self.interface)
        self.session.add(message)
        self.session.flush()
        dispatcher.matchMessage(message)
        return message

    @action()
    def send(self):
        msg = self.save_and_parse_message(self.request.params['number'],
                                          self.request.params['message'])
        return Response(msg.uuid)

    @action()
    def remove(self):
        self.session.delete(self.interface)
        self.session.flush()
        return HTTPFound(location="%s/" % self.request.application_url)


class MeterHandler(object):
    """
    Meter handler, allows for user to edit and manage meters
    """
    def __init__(self, request):
        self.request = request
        self.session  = DBSession()
        self.meter = self.session.query(Meter).\
                     get(self.request.matchdict['id'])
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="meter/index.mako", permission="admin")
    def index(self):
        """
        Main view for meter overview. Also includes circuit gird and
        some graphs
        """
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text": "Meter Overview"})
        grid = Grid(Circuit, self.meter.get_circuits())
        # This was the best way to exclude fields from the grid.    
        # But I am calling a private method... FIXME
        excludes  = []
        excludes.extend(grid._get_fields()[:3]) # remove the first three columns
        excludes.append(grid._get_fields()[-2]) 
        grid.configure(readonly=True, exclude=excludes)
        grid.insert(grid._get_fields()[3],
                    Field('Account Number',
                          value=lambda item: '<a href=%s>%s</a>' % (item.getUrl(),
                                                                    item.pin)))
        return {
            'grid': grid,
            "logged_in": authenticated_userid(self.request),
            "meter": self.meter,
            "fields": get_fields(self.meter),
            "breadcrumbs": breadcrumbs }

    @action(request_method='POST', permission="admin")
    def add_circuit(self):
        """
        A view that allows users to add an circuit to an 
        """
        params = self.request.params
        pin = params.get("pin")
        if len(pin) == 0:
            pin = Circuit.get_pin()
        account = Account(
            lang=params.get("lang"),
            phone=params.get("phone"))
        circuit = Circuit(meter=self.meter,
                          account=account,
                          pin=pin,
                          ip_address=params.get("ip_address"),
                          energy_max=int(params.get("energy_max")),
                          power_max=int(params.get("power_max")))
        self.session.add(account)
        self.session.add(circuit)
        self.session.flush()
        return HTTPFound(location="%s%s" % (
                self.request.application_url, self.meter.getUrl()))

    @action(permission="admin")
    def remove(self):
        """
        Allows users to remove an meter.
        FIXME does not seem to be working!.
        """
        self.session.delete(self.meter)
        [self.session.delete(x)
         for x in self.session.query(Circuit).filter_by(meter=self.meter)]
        return HTTPFound(location="/")

    @action(permission="admin")
    def ping(self):
        job = Mping(self.meter)
        self.session.add(job)
        self.session.flush()
        interface = self.meter.communication_interface
        interface.sendJob(job)
        return HTTPFound(location=self.meter.getUrl())


class CircuitHandler(object):
    """
    Circuit handler. Has all of the most
    important urls for managing circuits
    """

    def __init__(self, request):
        self.session = DBSession()
        self.request = request
        self.circuit = self.session.\
                       query(Circuit).get(self.request.matchdict["id"])
        self.meter = self.circuit.meter
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="circuit/index.mako", permission="admin")
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.extend([
                    {"text": "Meter Overview", "url": self.meter.getUrl()},
                    {"text": "Circuit Overview"}])
        jobs = Grid(Job, self.circuit.get_jobs())
        jobs.configure(readonly=True, exclude=[jobs._get_fields()[0]])
        logs = Grid(PrimaryLog, self.circuit.get_logs())
        logs.configure(readonly=True, exclude=[logs._get_fields()[1]])
        return {
            "logged_in": authenticated_userid(self.request),
            "breadcrumbs": breadcrumbs,
            "jobs": jobs,
            "logs" : logs,
            "fields": get_fields(self.circuit),
            "circuit": self.circuit }

    @action(permission="admin")
    def turn_off(self):
        self.circuit.turnOff()
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def turn_on(self):
        self.circuit.turnOn()
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def ping(self):
        self.circuit.ping()
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def remove_jobs(self):
        [self.session.delete(job) for job in self.circuit.get_jobs()]
        return HTTPFound(
            location="%s%s" % (self.request.application_url,
                                self.circuit.getUrl()))

    @action(renderer="circuit/build_graph.mako", permission="admin")
    def build_graph(self):
        return {
            "logged_in": authenticated_userid(self.request),
            "circuit": self.circuit }

    @action(renderer="circuit/show_graph.mako", permission="admin")
    def show_graph(self):
        query = self.session.query(PrimaryLog)
        params = self.request.params
        # parse the date from the request
        origin = parser.parse(params["from"])
        to = parser.parse(params["to"])
        yaxis = params["yaxis"]
        logs = [x for x in query.all() if x.created > origin]
        logs = [x for x in logs if x.created < to]
        return {
            "logged_in": authenticated_userid(self.request),
            "data": [{"time": str(x.created.ctime()),
                      "value": x.get_property(yaxis)} for x in logs ],
            "y_units": simplejson.dumps(params["yaxis"]),
            "origin": simplejson.dumps(params["from"]),
            "to": simplejson.dumps(params["to"])}

    @action()
    def jobs(self):
        return Response([x.toJSON() for x in self.circuit.get_jobs()])

    @action(permission="admin")
    def add_credit(self):
        interface = self.circuit.meter.communication_interface
        job = AddCredit(circuit=self.circuit,
                  credit=self.request.params.get("amount"))
        self.session.add(job)
        self.session.flush()
        interface.sendJob(job)
        return HTTPFound(location=self.circuit.getUrl())

    @action(permission="admin")
    def remove(self):
        self.session.delete(self.circuit)
        return HTTPFound(location=self.meter.getUrl())


class AccountHandler(object):
    """
    """

    def __init__(self, request):
        self.session = DBSession
        self.request = request
        self.account = self.session.\
            query(Account).get(self.request.matchdict.get("id"))

    def index(self):
        return Response(str(self.account))

    @action(renderer="account/edit.mako", permission="admin")
    def edit(self):
        return {"account": self.account,
                 "fields": get_fields(self.account)}

    @action(permission="admin")
    def update(self):
        account = model_from_request(self.request,
                                     self.account)
        self.session.add(account)
        return Response()


class LoggingHandler(object):

    def __init__(self, request):
        session = DBSession()
        self.request = request
        matchdict = self.request.matchdict
        circuit_id = matchdict["circuit"].replace("_", ".")
        self.meter = session.\
            query(Meter).filter_by(name=matchdict["meter"]).first()
        self.circuit = session.\
            query(Circuit).filter_by(ip_address=circuit_id).first()

    @action()
    def pp(self):
        """
        Primary log action. Should force the meter to provide authentication
        """
        params = parse_qs(self.request.body)
        session = DBSession()
        if not self.meter or not self.circuit:
            return Response(status=404)
        log = PrimaryLog(circuit=self.circuit,
                   watthours=params["wh"][0],
                   use_time=params["tu"][0],
                   credit=params["cr"][0],
                   status=int(params["status"][0]))
        self.circuit.credit = float(log.credit)
        self.circuit.status = int(params["status"][0])  # fix
        session.add(log)
        session.merge(self.circuit)
        return Response("ok")

    @action()
    def sp(self):
        return Response(self.request)


class JobHandler(object):

    def __init__(self, request):
        self.request = request

    @action()
    def meter(self):
        session = DBSession()
        matchdict = self.request.matchdict
        meter = session.query(Meter).filter_by(slug=matchdict["id"]).first()
        return Response("".join([str(x) for x in meter.getJobs()]))

    @action()
    def job(self):
        session = DBSession()
        job = session.query(Job).get(self.request.matchdict["id"])
        if self.request.method == "DELETE":
            job.state = False
            job.end = datetime.datetime.now()
            session.merge(job)
            return Response(job.toString())
        else:
            return Response(simplejson.dumps(job.toDict()))


class TokenHandler(object):

    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.batch = self.session.\
            query(TokenBatch).filter_by(
            uuid=self.request.matchdict["id"]).first()

    @action(permission="admin")
    def show_batch(self):
        return Response(simplejson.dumps(
                [x.toDict() for x in self.batch.get_tokens()]))

    @action(permission="admin")
    def export_batch(self):
        tokens = self.batch.get_tokens()
        s = cStringIO.StringIO()
        csvWriter = csv.writer(s)
        mapper = tokens[0].__mapper__
        csvWriter.writerow(mapper.columns.keys())
        csvWriter.writerows(map(
                lambda model:
                map(lambda k: getattr(model, k),
                    mapper.columns.keys()), tokens))
        s.reset()
        resp = Response(s.getvalue())
        resp.content_type = 'application/x-csv'
        resp.headers.add('Content-Disposition',
                         'attachment;filename=tokens.csv')
        return resp

    @action(permission="admin")
    def refresh(self):
        return Response("stuff")


class MessageHandler(object):
    def __init__(self, request):
        self.session = DBSession()
        self.request = request
        self.message = self.session.\
                       query(Message).filter_by(
            uuid=self.request.matchdict["id"]).first()

    @action(renderer='sms/index_msg.mako')
    def index(self):
        global breadcrumbs
        breadcrumbs.extend({})
        return {
            'breadcrumbs': breadcrumbs,
            'message': self.message }

    @action(request_method="POST")
    def remove(self):
        self.message.sent = True
        self.session.merge(self.message)
        return Response("ok")

    @action(renderer='sms/delete_msg.mako')
    def delete(self):
        if self.request.method == 'POST':
            return Response("Removed Message")
        elif self.request.method == 'GET':
            return {'message': self.message }


class SMSHandler(object):
    """
    Handler for most SMS operations
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    @action(renderer="sms/index.mako", permission="admin")
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text": "SMS Message"})
        limit = self.request.params.get('limit', 1000)
        count = self.session.query(Message).count()
        messages = self.session.\
            query(Message).order_by(desc(Message.id)).limit(limit)
        return {
            "logged_in": authenticated_userid(self.request),
            "limit": limit,
            "count": count,
            "messages": messages,
            "table_headers": make_table_header(OutgoingMessage),
            "breadcrumbs": breadcrumbs }

    @action(permission="admin")
    def remove_all(self):
        [self.session.delete(msg) for msg in self.session.query(Message).all()]
        return HTTPFound(
            location="%s/sms/index" % self.request.application_url)

    @action()
    def ping(self):
        return Response('ok')

    @action()
    def received(self):
        msgs = [msg.toDict() for msg in self.session.query(Message).\
                filter_by(sent=False).filter(or_(Message.type == "job_message",
                  Message.type == "outgoing_message")).all()
                  if msg.number != '']
        return Response(
            content_type="application/json",
            body=simplejson.dumps(msgs))
