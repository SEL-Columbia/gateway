"""
Ivan Willig
Modi Labs
Simple twisted application to check if meters are MIA.
"""

from operator import sub
from datetime import datetime
from datetime import timedelta
from string import Template
import StringIO
import transaction

from twisted.internet import task
from twisted.internet import reactor
from twisted.application import service
from twisted.application.internet import TimerService

from pyramid.threadlocal import get_current_request
from pyramid_mailer.message import Message
from pyramid_mailer.mailer import Mailer


from gateway.models import DBSession
from gateway.models import Meter
from gateway.models import SystemLog
from gateway.models import initialize_sql

hour = 3600.00
db_string = "postgresql://postgres:password@localhost:5432/gateway"
initialize_sql(db_string)
session = DBSession()
error = Template('$circuit last sent a log on $date, over $timediff ago.')
mailer = Mailer()
_from = 'admin@sharedsolar.org'

def check_circuit(circuit, output):
    now = datetime.now()
    time_difference = now - timedelta(hours=1)
    last_log = circuit.getLastLog()
    if last_log:
        if time_difference > last_log.created:
            log = SystemLog(text=error\
                                .substitute(circuit=circuit.ip_address,
                                            timediff=sub(now, last_log.created),
                                            date=last_log.created,))
            output.write('--------------------\n')
            output.write("\t %s\n" % log.text)
            session.add(log)
    return circuit

def check_meters():
    output = StringIO.StringIO()
    print('++++++++++++++++++++')
    print('Checking system at %s' % datetime.now())
    with transaction:
        meters = session.query(Meter).all()
        for meter in meters:
            output.write('====================\n')
            output.write('Checking circuits for %s\n' % meter)
            for circuit in meter.get_circuits():
                check_circuit(circuit, output)
        msg = Message(subject='Gateway: Alert, Circuit failed',
                      sender=_from, 
                      body=output.getvalue(),
                      recipients=['ifw2104@gmail.com', 
                                  'drdrsoto@gmail.com', 
                                  #'rajeshmenon.mrg@gmail.com'
                                  ])
        mailer.send_immediately(msg, fail_silently=False)

application = service.Application(__name__)
ts = TimerService(hour, check_meters)
ts.setServiceParent(application)
