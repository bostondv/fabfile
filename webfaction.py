from __future__ import with_statement
from fabric.api import *
import xmlrpclib
import sys

# Create webfaction domain
@task
def domain():
	create_domain(env.hosts[0], env.app)

# Create webfaction application
@task
def app():
	create_app(env.app)

# Create webfaction website
@task
def website():
	create_website(env.app, env.ip, env.hosts[0])

# Create webfaction db
@task
def db():
	create_db(env.dbname, env.dbpass)

# Create webfaction application
@task(default=True)
def create():
	execute(domain)
	execute(app)
	execute(website)
	execute(db)

def create_domain(host, app):
	server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
	session_id, account = server.login(env.user, env.password)
	try:
		if env.user == 'pomelo':
			response = server.create_domain(session_id, host, app)
		else:
			response = server.create_domain(session_id, host, 'www')
		print "Domain on webfaction created: %s" % response
		return response

	except xmlrpclib.Fault:
		print "Could not create domain on webfaction %s, domain name maybe already in use" % host
		sys.exit(1)

# Creates a static_php53 using webfaction API
def create_app(app):
	server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
	session_id, account = server.login(env.user, env.password)
	try:
		response = server.create_app(session_id, app, 'static_php53', False, '')
		print "App on webfaction created: %s" % response
		return response

	except xmlrpclib.Fault:
		print "Could not create app on webfaction %s, app name maybe already in use" % app
		sys.exit(1)

def create_website(app, ip, host, https=False):
	server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
	session_id, account = server.login(env.user, env.password)
	try:
		if env.user == 'pomelo':
			response = server.create_website(session_id, app, ip, https, ['%s.%s' % (app, host)], [app, '/'])
		else:
			response = server.create_website(session_id, app, ip, https, [host, 'www.%s' % (host)], [app, '/'])
		print "Website on webfaction created: %s" % response
		return response

	except xmlrpclib.Fault:
		print "Could not create website on webfaction %s, website name maybe already in use" % app
		sys.exit(1)	
		
def create_db(dbname, dbpass, dbtype='mysql'):
	server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
	session_id, account = server.login(env.user, env.password)
	try:
		response = server.create_db(session_id, dbname, dbtype, dbpass)
		print "Databases on webfaction created: %s" % response
		return response

	except xmlrpclib.Fault:
		print "Could not create database on webfaction %s, database name maybe already in use" % dbname
		sys.exit(1)
