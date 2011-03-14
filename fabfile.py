from fabric.api import env, run, cd, sudo

location = '/usr/local/gateway-env/gateway'

env.hosts.extend(['178.79.140.99','173.203.94.233'])

def update_gateway():
    with cd(location):
        run('git pull origin master')
        run('../bin/python setup.py install')
        sudo('/etc/init.d/apache2 reload')
