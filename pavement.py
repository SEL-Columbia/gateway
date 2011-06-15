"""

"""
from os import path
import shutil

from paver.easy import task
from paver.easy import options
from paver.easy import Bunch
from paver.easy import needs
from paver.easy import pushd
from paver.easy import sh
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
def check_os():
    """
    Task to check the user's system
    """
    try:
        info('Checking Postgresql version')
        sh('pg_config --version')
        puts('--------------------')
    except:
        warning('You must have postgresql installed to run the gateway')


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
@needs(['build_openlayers', 'build_d3', 'build_slick_grid'])
def build_javascript():
    """
    Task that builds all of the javascript libraries requried by the Gateway
    """
    pass


@task
def install_python_reqs():
    info('Installing python requirements')
    sh('bin/pip install --upgrade git+git://github.com/iwillig/dispatch.git#egg=dispatch')
    info('Installing Gateway egg')
    sh('bin/python setup.py develop')


@task
@needs(['check_os', 'install_python_reqs', 'build_javascript'])
def build():
    puts('----------------------------------------')
    puts(colored.green('Finished building the SharedSolar Gateway'))
    puts(colored.green('Please run paster serve development --reload'))


@task
@needs(['build'])
def post_bootstrap():
    pass
