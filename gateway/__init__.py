"""
"""
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.exceptions import Forbidden
from pyramid.exceptions import NotFound
import pyramid_handlers
from dispatch import Dispatcher
from gateway.messaging import findMeter

dispatcher = Dispatcher()
dispatcher.addMatcher(findMeter,
                      'gateway.messaging.parse_meter_message')
dispatcher.addMatcher(r'^job=test', 'gateway.messaging.add_test_message')

# Allow consumers to check their balance
dispatcher.addMatcher(r'^(bal).(\w+)',
                      'gateway.consumer.get_balance', language='en')
dispatcher.addMatcher(r'^(solde).(\w+)',
                      'gateway.consumer.get_balance', language='fr')
dispatcher.addMatcher(r'^(2).(\w+)',
                    'gateway.consumer.get_balance', language='fr')

# Allow consumers to add credit to their account
dispatcher.addMatcher(r'^(add).(\w+).(\d+)',
                      'gateway.consumer.add_credit', language='en')
dispatcher.addMatcher(r'^(recharge).(\w+).(\d+)',
                      'gateway.consumer.add_credit', language='fr')
dispatcher.addMatcher(r'^(9).(\w+).(\w+)',
                    'gateway.consumer.add_credit', language='fr')

# Allow consumers to turn the circuit on
dispatcher.addMatcher(r'^(on).(\w+)',
                      'gateway.consumer.turn_circuit_on', language='fr')
dispatcher.addMatcher(r'^(1).(\w+)',
                      'gateway.consumer.turn_circuit_on', language='fr')

# Allow consumers to turn the circuit off
dispatcher.addMatcher(r'^(off).(\w+)',
                      'gateway.consumer.turn_circuit_off', language='fr')
dispatcher.addMatcher(r'^(0).(\w+)',
                      'gateway.consumer.turn_circuit_off', language='fr')

# Allow consumers to set their telephone numbers
dispatcher.addMatcher(r'(prim).(\w+)',
                      'gateway.consumer.set_primary_contact', language='en')
dispatcher.addMatcher(r'(tel).(\w+)',
                      'gateway.consumer.set_primary_contact', language='fr')
dispatcher.addMatcher(r'(4).(\w+)',
                      'gateway.consumer.set_primary_contact', language='fr')


def main(global_config, **settings):
    """
    This function returns a Pylons WSGI application.
    """
    from paste.deploy.converters import asbool
    from pyramid.config import Configurator
    from gateway.models import initialize_sql
    from gateway.security import groupfinder

    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application "
                         "configuration.")
    initialize_sql(db_string, asbool(settings.get('db_echo')))
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings,
                          autocommit=True,
                          root_factory='gateway.security.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.begin()
    session_factory = session_factory_from_settings(settings)
    config.include(pyramid_handlers.includeme)
    config.set_session_factory(session_factory)

    config.add_static_view('static', 'gateway:static/')
    config.include('pyramid_mailer')

    config.add_view(view='gateway.handlers.forbidden_view',
                    renderer='forbidden.mako',
                    context=Forbidden)

    config.add_view(view='gateway.handlers.not_found',
                    context=NotFound)

    config.add_route('add',
                     '/add/{class}',
                     renderer='add.mako',
                     permission='admin',
                     view='gateway.handlers.AddClass')

    config.add_route('delete',
                     '/delete/jobs',
                     permission='view',
                     view='gateway.handlers.DeleteJobs')

    config.add_route('graph',
                     '/graph/{class}/{id}',
                     view='gateway.handlers.GraphView')

    config.add_route('edit',
                     '/edit/{class}/{id}',
                     renderer='edit.mako',
                     permission='admin',
                     view='gateway.handlers.EditModel',)

    config.add_route('index',
                     '/',
                     renderer='index.mako',
                     view='gateway.handlers.Index')

    config.add_handler('alerts',
                       '/alerts/{action}',
                       'gateway.handlers:AlertHandler')

    config.add_handler('dashboard', '/dashboard',
                       'gateway.handlers:Dashboard',
                       action='index')

    config.add_handler('main', '/:action',
                      handler='gateway.handlers:Dashboard')

    config.add_handler('manage', '/manage/:action',
                       handler='gateway.handlers:ManageHandler')

    config.add_handler('interfaces', '/interface/:action/:id',
                       handler='gateway.handlers:InterfaceHandler'),

    config.add_handler('export-load', 'system/:action',
                       handler='gateway.sys:ExportLoadHandler')

    config.add_handler('users', 'user/:action',
                       handler='gateway.handlers:UserHandler')

    config.add_handler('meter', 'meter/:action/:id',
                       handler='gateway.handlers:MeterHandler')

    config.add_handler('circuit', 'circuit/:action/:id',
                       handler='gateway.handlers:CircuitHandler')

    config.add_handler('logs', 'logs/:action/:meter/',
                       handler='gateway.handlers:LoggingHandler')

    config.add_handler('jobs', 'jobs/:action/:id/',
                       handler='gateway.handlers:JobHandler')

    config.add_handler('sms', 'sms/:action',
                       handler='gateway.handlers:SMSHandler')

    config.add_handler('message', 'message/:action/:id',
                       handler='gateway.handlers:MessageHandler')

    config.add_handler('account', 'account/:action/:id',
                       handler='gateway.handlers:AccountHandler')

    config.add_handler('token', 'token/:action/:id',
                       handler='gateway.handlers:TokenHandler')

    config.add_subscriber('gateway.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')

    config.include('pyramid_formalchemy')
    config.include('fa.jquery')
    config.formalchemy_admin('admin',
                             package='gateway',
                             view='fa.jquery.pyramid.ModelView')

    config.end()
    return config.make_wsgi_app()
