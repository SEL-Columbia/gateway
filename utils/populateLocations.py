import transaction
from shapely.geometry import Point
from gateway.models import DBSession
from gateway.models import Meter
from gateway.models import SystemLog
from gateway.models import initialize_sql

import csv

db_string = "postgresql://ivan:password@localhost:5432/gateway"
initialize_sql(db_string)
session = DBSession()


if __name__ == '__main__': 
    query = session.query(Meter)
    try:
        locations = csv.reader(open("locations.csv"))
        
        for line in locations: 
            with transaction:
                point = Point(float(line[2]), float(line[1]))
                print point.wkt
                meter = query.filter_by(name= line[0]).first()
                meter.geometry = point.wkt
                session.flush()

    except Exception as error:
        print error
