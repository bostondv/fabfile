from fabric.api import *

# Development server
@task
def dev():
	env.user = 'dev_username_here'
	env.hosts = ['dev_domain_name_here']
	env.dir = '/home/pomelo/webenv.apps/%s' % (env.app)
	env.dbname = 'dev_database_name_here'
	env.dbuser = 'dev_database_username_here'
	env.dbpass = 'dev_database_password_here'
	env.dbhost = 'localhost'

# Production server
@task
def prod():
	env.user = 'prod_username_here'
	env.hosts = ['prod_domain_name_here']
	env.dir = '/path/to/website/%s' % (env.app)
	env.dbname = 'prod_database_name_here'
	env.dbuser = 'prod_database_username_here'
	env.dbpass = 'prod_database_password_here'
	env.dbhost = 'localhost'