from pyramid.security import Allow
from pyramid.security import Everyone

from gateway.models import Users
from gateway.models import DBSession


class RootFactory(object):

    __acl__ = [(Allow, Everyone, 'vistor'),
               (Allow, 'viewer', 'viewer'),
               (Allow, 'admin', 'admin')]
    
    def __init__(self, request):
        self.request = request


def groupfinder(userid, request):
    """
    Rough cut of user admin system.
    """
    session = DBSession()
    user = session.query(Users).filter_by(name=userid).first()
    if user:
        if user.group:
            return [user.group.name]
