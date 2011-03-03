gateway README

Install
=======

Requirements:: 

  postgresql-8.4
  python-psycopg2
  python-matplotlib
  python-setuptools

#. Or in one command line on a debian/ubuntu system.:: 

   sudo apt-get install postgresql-8.4 python-psycop python-matplotlib
   python-setuptools python-virtualenv git-core

#. Create a virtual env.:: 

   virtualenv gateway-env
   cd gateway-env

#. Check out the gateway.::

   git clone git://github.com/modilabs/gateway.git

#. Activate the virtualenv:: 

   source bin/activate

#. Install the python requirements::

   python setup.py develop

#. Run the development server.::
 
   paster serve development.ini --reload

