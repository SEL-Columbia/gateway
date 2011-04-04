"""
Ivan Willig
Modi Labs
Simple twisted application to check if meters are MIA.
"""

from operator import sub
from datetime import datetime
from datetime import timedelta
from string import Template
import transaction

from twisted.internet import task
from twisted.internet import reactor
from twisted.application import service
from twisted.application.internet import TimerService

from gateway.models import DBSession
from gateway.models import Meter
from gateway.models import SystemLog
from gateway.models import initialize_sql

hour = 3600.00
db_string = "postgresql://postgres:password@localhost:5432/gateway"
initialize_sql(db_string)
session = DBSession()


def checkMeters():
    error = Template('The last time we heard from\
 $circuit was on $date, over $timediff ago')
    with transaction:
        meters = session.query(Meter).all()
        for meter in meters:
            print('====================')
            now = datetime.now()
            time_difference = now - timedelta(hours=1)
            print(meter)
            for circuit in meter.get_circuits():
                last_log = circuit.getLastLog()
                if last_log:
                    if time_difference > last_log.created:
                        log = SystemLog(
                            text=error\
                                .substitute(circuit=circuit,
                                            timediff=sub(now, last_log.created)
                                            date=last_log.created,))
                        print(log)
                        session.add(log)


application = service.Application(__name__)
ts = TimerService(hour, checkMeters)
ts.setServiceParent(application)
