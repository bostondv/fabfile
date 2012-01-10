from __future__ import with_statement
from fabric.api import *

# Commit local repo
@task
def commit():
	# TODO check if anything to commit
	with settings(warn_only=True):
		local('git add .')
		local('git commit -a')

# Push local repo
@task
def push():
	with settings(warn_only=True):
		local('git push origin master')

# Pull local repo
@task
def pull():
	with settings(warn_only=True):
		local('git pull origin master')

# Commit remote repo
@task
def commit_remote():
	# TODO check if anything to commit first
	with settings(warn_only=True):
		with cd(env.dir):
			run('git add .')
			run('git commit -am "Update from remote server"')

# Push remote repo
@task
def push_remote():
	with settings(warn_only=True):
		with cd(env.dir):
			run('git push origin master')

# Pull remote repo
@task
def pull_remote():
	with settings(warn_only=True):
		with cd(env.dir):
			run('git pull origin master')