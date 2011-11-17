from __future__ import with_statement
from fabric.api import *
import datetime

# Environments
from environments import *

# Submodules
import wp
import mysql as db
import git
import media

# Globals
env.app = 'project_name_here'

env.git = 'git@pomelodesign.com'
env.media = 'wp-content/uploads'
env.dbpath = '%s/db' % (env.media)
env.dbfile = '%s/latest.sql.gz' % (env.dbpath)

now = datetime.datetime.now()
env.timestamp = now.strftime('%Y%m%dT%H%M%S')

# Create tmp dirs
@task
def bootstrap():
	with cd(env.dir):
		run('mkdir -p %s' % (env.media))
		run('mkdir -p %s' % (env.dbpath))
	run('mkdir -p ~/tmp')
	local('mkdir -p ~/tmp')
	local('mkdir -p %s' % (env.media))
	run('db -p %s' % (env.dbpath))

# First run install - automatically triggered by 'deploy' if needed
@task
def setup():
	execute(bootstrap)
	execute(git.commit)
	execute(git.push)
	run('git clone %s:%s.git %s' % (env.git, env.app, env.dir))
	execute(wp.config)
	execute(wp.htaccess)
	execute(media.put)
	execute(db.put)

# Update local development from remote
@task
def get():
	execute(git.commit_remote)
	execute(git.push_remote)
	execute(git.pull)
	execute(media.get)
	execute(db.get)

# Deploy the website
@task
def put():
	with settings(warn_only=True):
		if run('test -d %s/.git' % (env.dir)).failed:
			if run('test -f %s/index.html' % (env.dir)).succeeded:
				run('rm %s/index.html' % (env.dir))
			execute(setup)
		else:
			execute(git.commit)
			execute(git.push)
			execute(git.pull_remote)