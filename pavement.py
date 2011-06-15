"""

"""
from paver.easy import task
from paver.easy import options
from paver.easy import Bunch
from paver.easy import needs
#import paver.doctools

requires = [
    'psycopg2',
    'shapely',
    'WebTest',
    'pyramid_mailer',
    'fa.jquery',
    'distribute',
    'pyramid_formalchemy',
    'pyramid_handlers',
    'python-dateutil',
    'simplejson',
    'pyramid',
    'pyramid_beaker',
    'formalchemy',
    'SQLAlchemy==0.6.8',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'WebError',
]

options(
    setup=dict(
        name='gateway',
        version='0.1',
        description='The SharedSolar Billing Gateway',
        author='Ivan Willig',
        author_email='iwillig@gmail.com',
        packages=['gateway'],
        install_requires=requires,
        ),
    virtualenv=Bunch(
        packages_to_install=[
            'pip'
            'virtualenv'
        ],
        dest_dir='./',
        install_paver=True,
        script_name='bootstrap.py',
        paver_command_line='post_bootstrap'
    ),
)


@task
def build_javascript():
    print 'building javascript'


@task
@needs(['build_javascript'])
def build():
    print 'Building SharedSolar Gateway'
