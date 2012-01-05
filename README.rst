gateway README

Install
=======

Requirements::

  postgresql (and development headers)
  git
  setuptools
  numpy

#. Or in one command line on a debian/ubuntu system. 

  Install python::

   sudo apt-get install postgresql-9.1 git-core 

  Install numpy::

   sudo apt-get install python-numpy 

  Install geos::

   sudo apt-get install libgeos-dev

#. Check out the gateway.::

    git clone git://github.com/modilabs/gateway.git

  
#. Create a virtual env via the bootstrap command
This command should install all of the require dependencies.::
  
  python bootstrap.py


#. Activate the virtualenv::
 
    source bin/activate

#. Run the development server.::
 
  paster serve development.ini --reload


