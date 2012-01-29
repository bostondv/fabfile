from fabric.api import *
import datetime
import os

env.app = 'app_name_here'
env.git = 'git@domain.com:path/to/repo.git'
env.mediadir = 'wp-content/uploads'
env.tmpdir = '~/tmp'
env.dbfile = '%s/%s-latest.sql.gz' % (env.tmpdir, env.app)
env.mediafile = '%s/%s-media.tar.gz' % (env.tmpdir, env.app)
now = datetime.datetime.now()
env.timestamp = now.strftime('%Y%m%dT%H%M%S')

# Development server
@task
def dev():
	env.user = 'dev_username_here'
	env.hosts = ['prod_domain_name_here']
	env.dir = '/path/to/website'
	env.dbname = 'dev_database_name_here' 
	env.dbuser = 'dev_database_username_here'
	env.dbpass = 'dev_database_password_here'
	env.dbhost = 'localhost'

# Production server
@task
def prod():
	env.user = 'prod_username_here'
	env.hosts = ['prod_domain_name_here']
	env.dir = '/path/to/website'
	env.dbname = 'prod_database_name_here'
	env.dbuser = 'prod_database_username_here'
	env.dbpass = 'prod_database_password_here'
	env.dbhost = 'localhost'
