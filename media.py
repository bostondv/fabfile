from __future__ import with_statement
from fabric.api import *

# Media local --> remote
@task
def push():
	local('tar czf ~/tmp/media.tgz %s' % (media_path))
	put('~/tmp/media.tgz', '~/tmp/media.tgz')
	with cd(env.dir):
		run('tar xzf ~/tmp/media.tgz')

# Media remote --> local
@task
def pull():
	with cd(env.dir):
		run('tar czf ~/tmp/media.tgz %s' % (media_path))
		get('~/tmp/media.tgz', '~/tmp/media.tgz')
		local('tar xzf ~/tmp/media.tgz')