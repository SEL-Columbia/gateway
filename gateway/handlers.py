"""
Handler objects of web interface
"""

import csv
from urlparse import parse_qs
import uuid
import cStringIO
import simplejson
from datetime import timedelta
from datetime import datetime
import collections
import hashlib

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


from matplotlib.figure import Figure
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg

from shapely.wkt import loads

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
from gateway.models import MeterConfigKey
from gateway.models import Users
from gateway.models import Groups
from gateway.models import KannelInterface
from gateway.models import NetbookInterface
from gateway.models import AirtelInterface
from gateway.models import MeterChangeSet
from gateway.models import CommunicationInterface

# random junk that needs to be cleaned up.
from gateway.utils import get_fields
from gateway.utils import model_from_request
from gateway.utils import make_table_header


breadcrumbs = [{"text":"Manage Home", "url":"/"}]


def forbidden_view(request):
    """
    View to handle forbidden requests
    Checks to see if a user is authenitcated
    Gives the user the reason why they can't view a page.
    """
    return {'logged_in': authenticated_userid(request)}


def not_found(request):
    """ View to handle 404s
    """
    return Response("Unable to find resource")


class Index(object):
    """
    Index class to the / url. Very simple.
    """

    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]

    def __call__(self):
        return {'breadcrumbs': self.breadcrumbs}


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
            return self.session\
                .query(self.cls).get(self.request.matchdict['id'])


class AddClass(RestView):
    """
    An genertic view that allows for adding models to our system.
    """
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.cls = self.look_up_class()
        self.breadcrumbs = breadcrumbs[:]
        self.breadcrumbs\
            .append({'text': 'Add a new %s' % self.cls.__name__})

    def get(self):
        fs = FieldSet(self.cls, session=self.session)
        return {
            'breadcrumbs': self.breadcrumbs,
            'fs': fs, 'cls': self.cls}

    def post(self):
        fs = FieldSet(self.cls, session=self.session).\
             bind(self.cls(), data=self.request.POST)
        if fs.validate():
            fs.sync()
            self.session.flush()
            return HTTPFound(location=fs.model.getUrl())
        else:
            return {'fs': fs, 'cls': self.cls}


class EditModel(RestView):
    """
    A view that allows models to be edited.  Takes the class name as a
    string parameter and returns the correct html form.
    """
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.cls = self.look_up_class()
        self.instance = self.look_up_instance()
        self.breadcrumbs = breadcrumbs[:]
        self.breadcrumbs.append({'text': 'Edit %s' % self.instance})

    def get(self):
        fs = FieldSet(self.instance)
        return {'fs': fs,
                'breadcrumbs': self.breadcrumbs[:],
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
        self.now = datetime.now()
        self.days30 = timedelta(days=30)
        self.request = request
        self.session = DBSession()
        self.cls = self.look_up_class()
        self.instance = self.look_up_instance()
        self.column = self.request.params.get('column', None)
        self.figsize = tuple(map(lambda item: int(item),
                                 self.request.params.get('figsize',
                                                         "1,2").split(",")))
        self.columns = self.request.params.get('columns', None)
        self.start = self.request.params.get('start', None)
        self.end = self.request.params.get('end', None)
        if self.end is not None:
            self.end = parser.parse(self.end)
        if self.end is None:
            self.end = self.now
        if self.start is not None:
            self.start = parser.parse(self.start)
        if self.start is None:
            self.start = self.end - self.days30

    def get_circuit_logs(self, circuit):
        return self.session.query(PrimaryLog).filter_by(circuit=circuit)\
               .filter(PrimaryLog.created > self.start)\
               .filter(PrimaryLog.created < self.end).order_by(PrimaryLog.date)

    def get_ylabel(self):
        """
        """
        return {'credit': 'Credit',
                'watthours': 'Energy (Wh)',
                'use_time': 'Time used (sec)'}[self.column]

    def graphCircuit(self):
        fig = Figure(figsize=self.figsize)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111,
                             title='%s graph for %s' % (FieldSet.prettify(
                                 self.column), self.instance))
        logs = self.get_circuit_logs(self.instance)
        x = [date2num(log.date) for log in logs]
        y = [getattr(log, self.column) for log in logs]
        ax.plot_date(x, y, 'x-')
        ax.set_ylabel(self.get_ylabel())
        ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
        ax.set_ylim(ymin=0)
        ax.grid(True, linestyle='-', color='#e0e0e0')
        fig.autofmt_xdate()
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
    This handler allows admin to send test messages.
    Will be expaned to include more types of alerts.
    """
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer='alerts/make.mako', permission='admin')
    def make(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Send Alerts'})
        return {
            'breadcrumbs': breadcrumbs,
            'interfaces': self.session.query(CommunicationInterface).all()}

    @action(permission='admin')
    def send_test(self):
        """
        Method to send a test message via a comm interface
        """
        interface = self.session\
                    .query(CommunicationInterface)\
                    .get(self.request.params['interface'])
        number = self.request.params['number']
        text = self.request.params['text']
        msg = interface.sendMessage(number, text)
        return HTTPFound(location="%s/message/index/%s" %
                         (self.request.application_url, msg.uuid))


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

        logs = Grid(SystemLog,
                    self.session.query(SystemLog)\
                    .order_by(desc(SystemLog.created)).limit(10))
        logs.configure(readonly=True)
        return {
            'logs': logs,
            'breadcrumbs': self.breadcrumbs}

    @action(renderer="dashboard.mako", permission='view')
    def dashboard(self):
        return {
            "logged_in": authenticated_userid(self.request)}


class ManageHandler(object):
    """
    """
    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer='manage/index.mako')
    def index(self):
        return {
            'breadcrumbs': self.breadcrumbs}

    @action(renderer='manage/meters.mako')
    def show_meters(self):
        session = DBSession()
        return {
            'breadcrumbs': self.breadcrumbs,
            'meters': simplejson\
                .dumps([{'name': m.name,
                         'id': m.id,
                         'number_of_circuits': len(m.get_circuits()),
                         'pv': m.panel_capacity,
                         'phone': m.phone,
                         'battery': m.battery,
                         'location': m.location
                         }
                        for m in session.query(Meter).all()])}

    @action()
    def metersAsGeoJson(self):
        session = DBSession()
        meters = session.query(Meter).filter(Meter.geometry != None)
        return Response(
            content_type='application/json',
            body = simplejson.dumps(
                {'type' : 'FeatureCollection',
                 'features' : 
                 [ { 'type': 'Feature',
                     'properties': {'name': x.name},
                     'geometry': {'type': 'Point',
                                  'coordinates': list(loads(
                                        x.geometry).coords)[0]} }
                   for x in meters]
                 }))

    @action(renderer='map.mako')
    def map(self):
        return {}

    def makeGrid(self, cls):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': "%ss" % cls.__name__})
        grid = Grid(cls, self.session.query(cls).all())
        grid.configure(readonly=True, exclude=[grid._get_fields()[0]])
        grid.insert(grid._get_fields()[1],
            Field('%s overview page' % cls.__name__,
                  value=lambda item:'<a href=%s>%s</a>' % (item.getUrl()
                                                           , str(item))))
        return {'grid': grid,
                'cls': cls,
                'breadcrumbs': breadcrumbs}

    @action(renderer='manage/genertic.mako', permission='view')
    def show(self):
        cls = getattr(models, self.request.params['class'])
        return self.makeGrid(cls)

    @action(permission='view', renderer='manage/tokens.mako')
    def tokens(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Manage Tokens'})
        grid = Grid(TokenBatch, self.session.query(TokenBatch).all())
        grid.configure(readonly=True, exclude=[grid._get_fields()[0]])
        grid.append(Field('Export to CSV file',
                          value = lambda item: '<a href="/%s">%s</a>' %\
                              (item.exportTokens(),
                               str(item))))
        grid.append(Field('Number of token',
                          value = lambda item: self.session.query(Token)\
                          .filter_by(batch=item).count()))
        grid.append(Field('Number of unused tokens',
                          value = lambda item: self.session\
                          .query(Token)\
                          .filter_by(batch=item)\
                          .filter_by(state='new').count()))

        return {'breadcrumbs': breadcrumbs,
                'grid': grid}

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
        return HTTPFound(
            location='%s%s' % (self.request.application_url,
                               '/manage/tokens'))

    @action(permission='admin', renderer='manage/pricing-models.mako')
    def pricing_models(self):
        return Response()


class UserHandler(object):
    """
    Handler to manage user system.
    Allows users to log in and out.
    Also allows users to
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    def findUser(self):
        name = authenticated_userid(self.request)
        return self.session.query(Users).filter_by(name=name).first()

    @action(renderer='users/profile.mako', permission='view')
    def profile(self):
        """
        Allows users to edit their current password.
        """
        error = None
        user = self.findUser()
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Edit your profile'})

        if self.request.method == 'POST':
            user = self.findUser()
            old_password = hashlib\
                .md5(self.request.params['old_password']).hexdigest()
            new_password = hashlib\
                .md5(self.request.params['new_password']).hexdigest()
            verify = hashlib\
                .md5(self.request.params['verify_password']).hexdigest()
            if unicode(old_password) == user.password:
                if new_password == verify:
                    user.password = unicode(new_password)
                    self.session.merge(user)
                    self.session.flush()
                    return HTTPFound(location='/')
                else:
                    error = 'You entered two different new passwords'
            else:
                error = 'Old password did not match'
        return {'user': user,
                'error': error,
                'breadcrumbs': breadcrumbs}

    @action(renderer='users/add.mako', permission='admin')
    def add(self):
        errors = None
        session = DBSession()
        groups = session.query(Groups).all()
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Add a new user'})
        if self.request.method == 'GET':
            return {'breadcrumbs': breadcrumbs,
                    'groups': groups,
                    'errors': errors}
        elif self.request.method == 'POST':
            name = self.request.params['name']
            email = self.request.params['email']
            password = self.request.params['password']
            group = self.request.params['group']
            user = Users(name=name, email=email,
                         group_id=group,
                         password=password)
            session.add(user)
            session.flush()
            return HTTPFound(location='/')

    @action(permission='admin')
    def show(self):
        session = DBSession()
        users = session.query(Users).all()
        return Response(str([(user.name, user.group.name) for user in users]))

    @action(renderer='login.mako')
    def login(self):
        session = DBSession()
        came_from = self.request.params.get('came_from', '/')
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in self.request.params:
            name = self.request.params['name']
            hash = hashlib.md5(self.request.params['password']).hexdigest()
            print(name, hash)
            user = session.query(Users)\
                .filter_by(name=name)\
                .filter_by(password=unicode(hash)).first()
            if user:
                headers = remember(self.request, user.name)
                return HTTPFound(
                    location="%s" % came_from,
                    headers=headers)
            message = 'Failed login'
        return {
            'message': message,
            'url': self.request.application_url + '/login',
            'came_from': came_from,
            'login': login,
            'password': password}

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
        return {'interface': self.interface,
                'breadcrumbs': breadcrumbs,
                'fields': get_fields(self.interface)}

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
        if isinstance(self.interface, KannelInterface)\
                or isinstance(self.interface, AirtelInterface):
            msg = self.save_and_parse_message(self.request.params['number'],
                                              self.request.params['message'])
            return Response(msg.uuid)

        if isinstance(self.interface, NetbookInterface):
            message = simplejson.loads(self.request.body)
            msg = self.save_and_parse_message(message['number'],
                                          message['message'])
            return Response(msg.uuid)
        else:
            return Response("error")

    @action(permission='admin')
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
        self.session = DBSession()
        self.meter = self.session.query(Meter).\
                     get(self.request.matchdict['id'])
        self.breadcrumbs = breadcrumbs[:]

    @action(renderer="meter/index.mako", permission="view")
    def index(self):
        """
        Main view for meter overview. Also includes circuit gird and
        some graphs
        """
        session = DBSession()
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({'text': 'Meters',
                            'url': '/manage/show_meters'})
        breadcrumbs.append({"text": "Meter Overview"})
        return {
            'meter': self.meter,
            'changesets': session\
                .query(MeterChangeSet).filter_by(meter=self.meter),
            'meter_config_keys': session.query(MeterConfigKey).all(),
            'breadcrumbs': breadcrumbs}

    @action()
    def update_config(self):
        return Response('ok')

    @action(renderer='meter/messsage_graph.mako', permission='view')
    def message_graph(self):
        """ Message table.
        """
        output = cStringIO.StringIO()
        d = collections.defaultdict(list)
        logs = self.meter.getLogs()
        cids = sorted([c.id for c in self.meter.get_circuits()])
        for log in logs:
            d[log.date.strftime('%Y.%m.%d.%H.%M')].append(log)
        for key in sorted(d.iterkeys(), reverse=True):
            log_cids = [log.circuit.id for log in d[key]]
            output.write(str(key) + " | ")
            output.write(" ".join([str(x).ljust(3) if x in
                                   log_cids else ' - ' for x in cids]))
            output.write("\n")
        return Response(output.getvalue(), content_type="text/plain")

    @action(permission='admin')
    def show_account_numbers(self):
        """ Returns the account numbers as a csv file.
        """
        output = cStringIO.StringIO()
        output.write('Pin, IpAddress \n')
        for c in self.meter.get_circuits():
            output.write('%s, %s\n' % (c.pin, c.ip_address))
        resp = Response(output.getvalue())
        resp.content_type = 'application/x-csv'
        resp.headers.add('Content-Disposition',
                         'attachment;filename=%s:accounts.csv' % \
                         str(self.meter.name))
        return resp

    # this serialization should be a class method.
    @action(permission='view')
    def circuits(self):
        """Dumps the circuits assoicted with Meter to a json file.
        Used in SlickGrid
        """
        return Response(
            content_type="application/json",
            body=simplejson.dumps(
                [{'id':x.id,
                  'ipaddress': x.ip_address,
                  'language': x.account.lang,
                  'last_msg': x.getLastLogTime()[0],
                  'status': x.status,
                  'account': x.pin,
                  'credit': x.credit
                  }
                 for x in self.meter.get_circuits()]))

    @action()
    def geometry(self):
        point = loads(self.meter.geometry)
        return Response(
            content_type='application/json',
            body=simplejson.dumps(
                {'type': 'FeatureCollection',
                  'features': [{
                            'type':'Feature',
                            'geometry': {'type': 'Point',
                                         'coordinates': list(point.coords)[0]},
                            'properties': {}
                            }]}))

    @action(request_method='POST', permission="admin")
    def add_circuit(self):
        """A view that allows users to add an circuit to an
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
                          ip_address=params.get("ip_address"),
                          energy_max=int(params.get("energy_max")),
                          power_max=int(params.get("power_max")))
        self.session.add(account)
        self.session.add(circuit)
        self.session.flush()
        return Response(simplejson.dumps(circuit.id))

    @action(permission="admin")
    def remove(self):
        """Allows users to remove an meter.
        """
        self.session.delete(self.meter)
        [self.session.delete(x)
         for x in self.session.query(Circuit).filter_by(meter=self.meter)]
        return HTTPFound(location="/manage/show?class=Meter")

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

    @action(renderer="circuit/index.mako", permission="view")
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
            "logs": logs,
            "fields": get_fields(self.circuit),
            "circuit": self.circuit}

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


class DeleteJobs(object):
    def __init__(self, request):
        self.request = request

    def __call__(self):
        jobids = simplejson.loads(self.request.body)
        print jobids


class JobHandler(object):

    def __init__(self, request):
        self.request = request

    @action(permission='view')
    def meter(self):
        session = DBSession()
        matchdict = self.request.matchdict
        meter = session.query(Meter).get(matchdict["id"])
        return Response("".join([str(x) for x in meter.getJobs()]))

    @action(permission='view')
    def delete(self):
        jobids = simplejson.loads(self.request.body)
        print(jobids)
        return Response('Hi Rajesh')

    @action(permission='view')
    def job(self):
        session = DBSession()
        job = session.query(Job).get(self.request.matchdict["id"])
        if self.request.method == "DELETE":
            job.state = False
            job.end = datetime.now()
            session.merge(job)
            return Response(str(job))
        else:
            return Response(simplejson.dumps(job.toDict()))


class TokenHandler(object):

    def __init__(self, request):
        self.request = request
        self.session = DBSession()
        self.batch = self.session.\
            query(TokenBatch).filter_by(
            uuid=self.request.matchdict["id"]).first()

    @action(permission="view")
    def show_batch(self):
        return Response(simplejson.dumps(
                [x.toDict() for x in self.batch.get_tokens()]))

    @action(permission="admin")
    def export_batch(self):
        tokens = self.batch.getTokens()
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

    @action(renderer='sms/index_msg.mako', permission='admin')
    def index(self):
        global breadcrumbs
        breadcrumbs.extend({})
        return {
            'breadcrumbs': breadcrumbs,
            'message': self.message}

    @action(request_method="POST")
    def remove(self):
        self.message.sent = True
        self.session.merge(self.message)
        return Response("ok")

    @action(permission='admin')
    def delete(self):
        self.session.delete(self.message)
        self.session.flush()
        return HTTPFound(location='/')


class SMSHandler(object):
    """
    Handler for most SMS operations
    """
    def __init__(self, request):
        self.request = request
        self.breadcrumbs = breadcrumbs[:]
        self.session = DBSession()

    @action(renderer="sms/index.mako", permission="view")
    def index(self):
        breadcrumbs = self.breadcrumbs[:]
        breadcrumbs.append({"text": "SMS Message"})
        limit = self.request.params.get('limit', 1000)
        count = self.session.query(Message).count()
        messages = self.session.\
            query(Message).order_by(desc(Message.id)).limit(limit)
        return {
            "limit": limit,
            "count": count,
            "messages": messages,
            "table_headers": make_table_header(OutgoingMessage),
            "breadcrumbs": breadcrumbs}

    @action(permission="view")
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
