from fabric.api import *
import datetime

env.app = 'app_name_here' # 9 character max
env.git = 'git@pomelodesign.com:path/to/repo.git'
env.media = 'wp-content/uploads'
env.dbpath = '%s/db' % (env.media)
env.dbfile = '%s/latest.sql.gz' % (env.dbpath)

now = datetime.datetime.now()
env.timestamp = now.strftime('%Y%m%dT%H%M%S')

# Development server
@task
def dev():
	# Optimized settings for webfaction
	env.user = 'dev_username_here'
	env.hosts = ['prod_domain_name_here']
	env.dir = '/path/to/website/%s' % (env.app)
	env.dbname = '%s' % (env.app) 
	env.dbuser = env.dbname # same as dbname
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