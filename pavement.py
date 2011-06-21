"""

"""
import os
from os import path
from datetime import datetime
import shutil

from paver.easy import task
from paver.easy import options
from paver.easy import Bunch
from paver.easy import needs
from paver.easy import pushd
from paver.easy import sh
from paver.ssh import scp
from paver.tasks import BuildFailure
from paver import setuputils
from clint.textui import colored
from clint.textui import puts

requires = [
    'psycopg2',
    'shapely',
    'WebTest',
    'pyramid_mailer',
    'fa.jquery',
    'distribute',
    'pyramid_formalchemy',
    'pyramid_handlers', 'python-dateutil', 'simplejson', 'pyramid', 'pyramid_beaker', 'formalchemy',
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
            'pip',
            'clint',
            'virtualenv',
        ],
        dest_dir='./',
        install_paver=True,
        script_name='bootstrap.py',
        paver_command_line='post_bootstrap'
    ),
)

setuputils.install_distutils_tasks()


# location of javascript folder on gateway
javascript_folder = 'gateway/static/js'


def warning(msg):
    puts('--------------------')
    puts(colored.red(msg))
    puts('--------------------')


def info(msg):
    """
    Function to print a info message
    """
    puts('--------------------')
    puts(colored.green(msg))
    puts('--------------------')


@task
def clean():
    """
    Task to remove javascript folders.
    """
    with pushd(javascript_folder):
        if path.exists('openlayers'):
            warning('Removing openlayers')
            shutil.rmtree('openlayers')
        if path.exists('d3'):
            warning('Removing d3')
            shutil.rmtree('d3')
        if path.exists('SlickGrid'):
            warning('Removing SlickGrid')
            shutil.rmtree('SlickGrid')


@task
def check_postgres():
    info('Checking your version of postgresql')
    try:
        sh('pg_config --version')
        puts('--------------------')
    except:
        raise BuildFailure('You don\'t have postgresql installed')


@task
def check_geos():
    info('Checking your version of geos')
    try:
        sh('geos-config --version')
        puts('--------------------')
    except:
        raise BuildFailure('You don\'t have geos installed')


@task
@needs(['check_postgres', 'check_geos'])
def check_os():
    """
    Task to check the user's system
    """
    pass


@task
def build_openlayers():
    """
    Task to install and build a compressed version of OpenLayers from github
    """
    info('Installing Openlayers')
    with pushd(javascript_folder):
        sh('git clone git://github.com/openlayers/openlayers.git', capture=True)
        with pushd('openlayers/build/'):
            info('Building OpenLayers into a compressed file')
            sh('python build.py', capture=True)
            shutil.copy('OpenLayers.js', '../')


@task
def build_d3():
    """
    Task to install d3.js, a graphing lib, from github.
    """
    info('Installing d3.js')
    with pushd(javascript_folder):
        sh('git clone https://github.com/mbostock/d3.git', capture=True)


@task
def build_slick_grid():
    """
    Task to install slick grid from github
    """
    info('Install SlickGrid')
    with pushd(javascript_folder):
        sh('git clone https://github.com/mleibman/SlickGrid.git', capture=True)


@task
@needs(['clean', 'build_openlayers', 'build_d3', 'build_slick_grid'])
def build_javascript():
    """
    Task that builds all of the javascript libraries requried by the Gateway
    """
    pass


@task
def install_python_reqs():
    info('Installing python requirements')
    sh('bin/pip install --upgrade git+git://github.com/iwillig/dispatch.git#egg=dispatch')
    sh('bin/pip install fabric')
    sh('bin/pip install markdown')
    info('Installing Gateway egg')
    sh('bin/python setup.py develop')


@task
@needs(['check_os', 'install_python_reqs', 'build_javascript'])
def build():
    puts('----------------------------------------')
    puts(colored.green('Finished building the SharedSolar Gateway'))
    puts(colored.green('Please run paster serve development.ini --reload'))


db_name = 'gateway'


@task
def drop_and_create_db():
    """Task to drop and create gateway db
    """
    info('Dropping and recreating database')
    try:
        sh('dropdb ' + db_name)
    except:
        pass
    try:
        sh('createdb ' + db_name)
    except:
        raise BuildFailure('Unable to create db table')


@task
@needs(['drop_and_create_db'])
def testing_db():
    from gateway.models import initialize_sql
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open('testing.ini'))
    db_string = config.get('app:gateway', 'db_string')
    initialize_sql(db_string)
    with pushd('migrations'):
        puts('--------------------')
        puts('Creating test tables')
        puts('Loading test data')
        sh('psql -d testing -f load_testing_env.sql')


@task
#@needs(['testing_db'])
def run_tests():
    import unittest
    from gateway.tests import FunctionalTests
    suite = unittest.TestLoader().loadTestsFromTestCase(FunctionalTests)
    unittest.TextTestRunner(verbosity=2).run(suite)


@task
@needs(['drop_and_create_db'])
def syncdb():
    """
    Task that downloads a zip file from the production server and the
    data into your local machine. This is destructive as it first
    removes your local copy of the database and then updates your
    database.
    """
    tmp_folder = 'tmp'
    try:
        shutil.rmtree(tmp_folder)
    except:
        pass
    now = datetime.now().strftime("%y%m%d")
    os.mkdir(tmp_folder)
    with pushd(tmp_folder):
        scp('root@gateway.sharedsolar.org:/var/lib/postgresql/backups/gateway.' + now + '.sql.zip', '.')
        sh('unzip gateway.' + now + '.sql.zip')
        sh('psql -d ' + db_name + ' -f var/lib/postgresql/backups/gateway.' + now + '.sql')
    shutil.rmtree(tmp_folder)


@task
@needs(['build'])
def post_bootstrap():
    pass
