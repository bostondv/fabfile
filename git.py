from __future__ import with_statement
from fabric.api import *

# Commit local repo
@task
def commit():
	local('git add .')
	local('git commit -a')

# Push local repo
@task
def push():
	local('git push')

# Pull local repo
@task
def pull():
	local('git pull')

# Commit remote repo
@task
def commit_remote():
	with cd(env.dir):
		run('git add .')
		run('git commit -am "Update from remote server"')

# Push remote repo
@task
def push_remote():
	with cd(env.dir):
		run('git push')

# Pull remote repo
@task
def pull_remote():
	with cd(env.dir):
		run('git pull')