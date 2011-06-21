import unittest
import uuid
import urllib2
import urllib
from pyramid import testing


def make_request(msg, interface, phone="+22365489009"):
    data = urllib.urlencode({'message': msg,
                             'number': phone,
                             'uuid': str(uuid.uuid4()) })
    return urllib2.Request(
        data=data, url='http://localhost:6543/interface/send/%s' % interface.id)


class FunctionalTests(unittest.TestCase):
    """ Unit tests for the Gateway UI """
    def setUp(self):
        self.config = testing.setUp()
        import ConfigParser
        from gateway.models import DBSession
        from gateway.models import initialize_sql
        config = ConfigParser.ConfigParser()
        config.readfp(open('testing.ini'))
        db_string = config.get('app:gateway', 'db_string')
        initialize_sql(db_string)
        from gateway import main
        from webtest import TestApp
        app = main(None, **{'db_string': db_string,
                            'mako.directories': config.get('app:gateway', 'mako.directories')})
        self.testapp = TestApp(app)
        self.session = DBSession()

    def tearDown(self):
        testing.tearDown()

    def test_number_of_meter(self):
        from gateway.models import Meter
        meters = self.session.query(Meter).all()
        self.assertEquals(len(meters), 1)

    def test_index(self):
        res = self.testapp.get('/', status=200)
        self.assertEquals(res.status, '200 ok')

    def test_number_of_circuits(self):
        from gateway.models import Circuit
        circuits = self.session.query(Circuit).all()
        self.assertEquals(len(circuits), 11)

    def test_number_of_comm_interfaces(self):
        from gateway.models import CommunicationInterface
        interfaces = self.session.query(CommunicationInterface).all()
        self.assertEquals(len(interfaces), 1)

    def test_balance_english(self):
        from gateway.models import CommunicationInterface
        from gateway.models import Circuit
