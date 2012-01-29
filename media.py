from __future__ import with_statement
from fabric.api import *

# Media local --> remote
@task
def push():
	local('tar czf %s %s' % (env.mediafile, env.mediadir))
	put(env.mediafile, env.mediafile)
	with cd(env.dir):
		run('tar xzfm %s' % env.mediafile)

# Media remote --> local
@task
def pull():
	with cd(env.dir):
		run('tar czf %s %s' % (env.mediafile, env.mediadir))
		get(env.mediafile, env.mediafile)
		local('tar xzfm %s' % env.mediafile)