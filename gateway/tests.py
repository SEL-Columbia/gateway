import unittest
from sqlalchemy.orm.query import Query
from webob.exc import HTTPFound
from pyramid import testing


class GatewayTests(unittest.TestCase):
    """ Unit tests for the Gateway UI """
    def setUp(self):
        self.config = testing.setUp()
        from gateway.models import DBSession
        from gateway.models import initialize_sql
        initialize_sql('sqlite://')
        self.session = DBSession()

    def tearDown(self):
        testing.tearDown()

    def testAddKannelInterface(self):
        from gateway.models import KannelInterface
        interface = KannelInterface(name='Kannel',
                                    location='USA',
                                    host='localhost',
                                    port='5432',
                                    provider='Ivan',
                                    username='kannel',
                                    password='kannel')
        self.session.add(interface)
        self.session.flush()
        query = self.session.query(KannelInterface)
        self.assertEqual(query.count(), 1)

    def testAddNetbookInterface(self):
        from gateway.models import NetbookInterface
        interface = NetbookInterface(name='Netbook',
                                     provider='Ivan',
                                     location='USA')
        self.session.add(interface)
        self.session.flush()
        query = self.session.query(NetbookInterface)
        self.assertEqual(query.count(), 1)

    def testAddingMeters(self):
        from gateway.models import Meter
        meter = Meter(
            name='Test meter',
            phone='181812345',
            location='USA',
            battery=100,
            status=1,
            panel_capacity=100)
        self.session.add(meter)
        self.session.flush()
        query = self.session.query(Meter)
        self.assertEqual(query.count(), 1)

    def testAddingAccount(self):
        from gateway.models import Account
        a = Account(name='default',
                    phone='19291212',
                    lang='fr')
        self.session.add(a)
        self.session.flush()
        q = self.session.query(Account)
        self.assertEqual(q.count(), 1)

    def testAddingCircuits(self):
        from gateway.models import Circuit
        c = Circuit(meter=None,
                    account=None,
                    energy_max=100,
                    power_max=100,
                    ip_address='192.168.1.200',
                    status=1,
                    credit=1)
        self.session.add(c)
        self.session.flush()
        q = self.session.query(Circuit)
        self.assertEquals(q.count(), 1)

    def testAddingAnIncomingMessage(self):
        from gateway.models import IncomingMessage
        import uuid
        msg = IncomingMessage(number='181812345',
                              text='Hello world',
                              uuid=str(uuid.uuid4()),
                              communication_interface=None)
        self.session.add(msg)
        self.session.flush()
        q = self.session.query(IncomingMessage)
        self.assertEquals(q.count(), 1)

    def testDashboardIndex(self):
        request = testing.DummyRequest()
        from gateway.handlers import Dashboard
        from formalchemy.tables import Grid
        handler = Dashboard(request)
        # test index
        index = handler.index()
        self.assertEqual(type(index['logs']), Grid)
        self.assertEqual(type(index['breadcrumbs']), list)

    def testManage(self):
        request = testing.DummyRequest()
        from gateway.handlers import ManageHandler
        handler = ManageHandler(request)
        index = handler.index()
        self.assertEqual(type(index['breadcrumbs']), list)

    def testAlerts(self):
        from gateway.handlers import AlertHandler
        handler = AlertHandler(testing.DummyRequest())
        make = handler.make()
        self.assertEqual(type(make['breadcrumbs']),list)
        self.assertEqual(type(make['interfaces']),list)

## Below need to be functional tests.

    # def testAlertsSend(self):
    #     from gateway.handlers import AlertHandler
    #     request = testing.DummyRequest(params={'interface' : 1,
    #                                            'text'      : 'This is an test',
    #                                            'number'    : '181812345'})
    #     handler = AlertHandler(request)        
    #     send = handler.send_test()

    def testAddModels(self):
        # test adding a Meter
        # totally broken from within the testing
        # request. FIXME
        from gateway.handlers import AddClass

    def testUser(self):
        request = testing.DummyRequest()
        from gateway.handlers import UserHandler
        handler = UserHandler(request)

        # test login
        login = handler.login()
        self.assertEqual(login['url'], 'http://example.com/login',)
        self.assertEqual(login['login'], '')
        self.assertEqual(login['password'], '')
        self.assertEqual(login['came_from'], '/')

        logout = handler.logout()
        self.assertEqual(type(logout), HTTPFound)
        self.assertEqual(logout.status, '302 Found')
