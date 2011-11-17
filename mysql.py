from __future__ import with_statement
from fabric.api import *

# Dump database
@task
def dump():
	with settings(warn_only=True):
		if local('test -d %s' % (env.dbpath)).failed:
			local('mkdir -p %s'% (env.dbpath))
	local('mysqldump --opt -u %s -p%s -h localhost %s | gzip -9 > %s' % (env.local_dbuser, env.local_dbpass, env.app, env.dbfile))
	local('cp %s %s/%s-%s-local.sql.gz' % (env.dbfile, env.dbpath, env.app, env.timestamp))

# Dump remote database
@task
def dump_remote():
	with cd(env.dir):
		with settings(warn_only=True):
			if run('test -d %s' % (env.dbpath)).failed:
				run('mkdir -p %s'% (env.dbpath))
		run('mysqldump --opt -u %s -p%s -h %s %s | gzip -9 > %s' % (env.dbuser, env.dbpass, env.dbhost, env.dbname, env.dbfile))
		run('cp %s %s/%s-%s-remote.sql.gz' % (env.dbfile, env.dbpath, env.app, env.timestamp))

# Import database
@task
def mysql():
	local('gunzip < %s | mysql -u %s -p%s -h localhost %s' % (env.dbfile, env.local_dbuser, env.local_dbpass, env.app))

# Import database remote
@task
def mysql_remote():
	with cd(env.dir):
		run('gunzip < %s | mysql -u %s -p%s -h %s %s' % (env.dbfile, env.dbuser, env.dbpass, env.dbhost, env.dbname))

# Database local --> remote
@task
def put():
	execute(dump_remote)
	execute(dump)
	local('tar czf ~/tmp/db.tgz %s' % (env.dbpath))
	put('~/tmp/db.tgz', '~/tmp/db.tgz')
	with cd(env.dir):
		run('tar xzf ~/tmp/db.tgz')
	execute(mysql_remote)

# Database remote --> local
@task
def get():
	execute(dump_remote)
	execute(dump)
	with cd(env.dir):
		run('tar czf ~/tmp/db.tgz %s' % (env.dbpath))
		get('~/tmp/db.tgz', '~/tmp/db.tgz')
		local('tar xzf ~/tmp/db.tgz')
	execute(mysql)
