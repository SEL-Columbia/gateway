from pyramid.threadlocal import get_current_request
from pyramid.exceptions import ConfigurationError
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from git import Repo


def add_renderer_globals(event):
    """ A subscriber to the ``pyramid.events.BeforeRender`` events.  Updates
    the :term:`renderer globals` with values that are familiar to Pylons
    users."""
    request = event.get('request')
    if request is None:
        request = get_current_request()
    globs = {
        'url': route_url,
        'h': None,
        'a_url': request.application_url,
        'user': authenticated_userid(request),
        'repo': Repo(request.registry.settings.get('git_repo', '.'))
        }
    if request is not None:
        tmpl_context = request.tmpl_context
        globs['c'] = tmpl_context
        globs['tmpl_context'] = tmpl_context
        try:
            globs['session'] = request.session
        except ConfigurationError:
            pass
    event.update(globs)
