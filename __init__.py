from __future__ import with_statement
from fabric.api import *

# Environments
from environments import *

# Submodules
import wp
import mysql as db
import git
import media

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
	execute(media.push)
	execute(db.push)

# Update local development from remote
@task
def pull():
	execute(git.commit_remote)
	execute(git.push_remote)
	execute(git.pull)
	execute(media.pull)
	execute(db.pull)

# Deploy the website
@task
def push():
	with settings(warn_only=True):
		if run('test -d %s/.git' % (env.dir)).failed:
			if run('test -f %s/index.html' % (env.dir)).succeeded:
				run('rm %s/index.html' % (env.dir))
			execute(setup)
		else:
			execute(git.commit)
			execute(git.push)
			execute(git.pull_remote)