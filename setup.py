import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'zope.interface==3.8.0',
    'repoze.errorlog',
    'GitPython',
    'psycopg2',
    'twilio',
    'shapely',
    'WebTest',
    'pyramid_mailer',
    'fa.jquery',
    'distribute',
    'pyramid_formalchemy',
    'pyramid_handlers',
    'python-dateutil',
    'simplejson',
    'pyramid==1.2',
    'pyramid_beaker',
    'formalchemy',
    'SQLAlchemy==0.6.8',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'WebError',
    'pytz',
]

if sys.version_info[:3] < (2, 5, 0):
    requires.append('pysqlite')

setup(name='gateway',
      version='0.0',
      description='gateway',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="gateway",
      entry_points="""\
      [paste.app_factory]
      main = gateway:main
      """
      )
