"""

"""
import csv
import cStringIO
import datetime
import inspect
from webob import Response
from pyramid_handlers import action
from sqlalchemy.ext.declarative import declarative_base
from gateway.models import Base
from gateway import models
from gateway.utils import nice_print

session = models.DBSession()

def findModel(modelName):
    """ Inspects model module and returns dict """
    klass = getattr(models,modelName)
    if klass:
        query = session.query(klass).all()
        mapper = klass.__mapper__        
        return {"class" : klass, "query" : query, "mapper" : mapper}
    else:
        return None

def findTable(possible):
    if inspect.isclass(possible[1]):
        if issubclass(possible[1],Base):
            return possible[1]

class ExportLoadHandler(object):
    def __init__(self,request):
        self.request = request

    @action(renderer="sys/index.mako")
    def index(self):
        return {} 

    @action()
    def export(self):
        s = cStringIO.StringIO()
        csvWriter = csv.writer(s)
        modelName = str(self.request.params.get("model"))
        results = findModel(modelName)
        if results:
            csvWriter.writerow(nice_print(results["query"][0]).keys())            
            csvWriter.writerows([nice_print(x).values() for x in results["query"]])
            s.reset()
            resp = Response(s.getvalue())
            resp.content_type = 'application/x-csv'
            resp.headers.add('Content-Disposition',
                             'attachment;filename=%s:data.csv' % modelName)
            return resp        
        else:
            return Response("Unable to find table") 

    @action(renderer="sys/download.mako",permission="admin")
    def download(self):
        tables = []
        members = inspect.getmembers(models)
        for member in members:
            table = findTable(member)
            if table:
                tables.append(table)
        return {"tables" : tables}


