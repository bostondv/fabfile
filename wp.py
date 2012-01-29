from __future__ import with_statement
from fabric.api import *
import urllib
import os

# Find and replace function
def replace_all(data, dic):
	for i, j in dic.iteritems():
		data = data.replace(i, j)
	return data
	
# Create wp-config.php
@task
def config():
	salt = urllib.urlopen('https://api.wordpress.org/secret-key/1.1/salt/').read()

	reps = {
		'database_name_here': env.dbname,
		'username_here': env.dbuser, 
		'password_here': env.dbpass,
		'localhost': env.dbhost,
		'//salt': salt,
	}

	config_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/wp-config.php').read()
	config_file = open('%s/wp-config.php' % env.tmpdir,'w')
	output = replace_all(config_sample, reps)
	config_file.write(output)
	config_file.close()
	with cd(env.dir):
		put('%s/wp-config.php' % env.tmpdir, 'wp-config.php')

# Create .htaccess
@task
def htaccess():
	htaccess_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/htaccess.txt').read()
	htaccess_file = open('%s/htaccess-sample.txt' % env.tmpdir,'w')
	htaccess_file.write(htaccess_sample)
	htaccess_file.close()
	with cd(env.dir):
		put('%s/htaccess-sample.txt' % env.tmpdir, '.htaccess')

# Fix WordPress db URL paths when moving servers
@task
def fix_urls():
	pass