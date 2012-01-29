from __future__ import with_statement
from fabric.api import *

# Dump database
@task
def dump():
	with settings(warn_only=True):
		if local('test -d %s' % env.tmpdir).failed:
			local('mkdir -p %s' % env.tmpdir)
	local('mysqldump --opt -u %s -p%s -h localhost %s | gzip -9 > %s' % (env.local_dbuser, env.local_dbpass, env.app, env.dbfile))
	local('cp %s %s/%s-%s-local.sql.gz' % (env.dbfile, env.tmpdir, env.dbname, env.timestamp))

# Dump remote database
@task
def dump_remote():
	with cd(env.dir):
		with settings(warn_only=True):
			if run('test -d %s' % env.tmpdir).failed:
				run('mkdir -p %s' % env.tmpdir)
		run('mysqldump --opt -u %s -p%s -h %s %s | gzip -9 > %s' % (env.dbuser, env.dbpass, env.dbhost, env.dbname, env.dbfile))
		run('cp %s %s/%s-%s-remote.sql.gz' % (env.dbfile, env.tmpdir, env.dbname, env.timestamp))

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
def push():
	execute(dump_remote)
	execute(dump)
	put(env.dbfile, env.dbfile)
	execute(mysql_remote)

# Database remote --> local
@task
def pull():
	execute(dump_remote)
	execute(dump)
	get(env.dbfile, env.dbfile)
	execute(mysql)
