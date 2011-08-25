gateway README

Install
=======

Requirements:: 

  postgresql-8.4
  python-psycopg2
  python-matplotlib
  python-setuptools

#. Or in one command line on a debian/ubuntu system.:: 

  sudo apt-get install postgresql-8.4 python-psycopg2 
  python-setuptools python-virtualenv git-core

  sudo apt-get install geos libgeos proj libproj
  
#. Create a virtual env.:: 


#. Check out the gateway.::

  git clone git://github.com/modilabs/gateway.git



#. Activate the virtualenv:: 


#. Install the python requirements::

  python setup.py develop

#. Run the development server.::
 
  paster serve development.ini --reload

