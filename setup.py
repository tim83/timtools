#! /usr/bin/python3
"""Manager for the python package"""

from setuptools import setup

setup(
	name='timtools',
	version='0.27.1',
	packages=['timtools'],
	url='',
	license='',
	author='***REMOVED*** Mees',
	author_email='tim@mees.vip',
	description='',
	install_requires=[
		"validators",
		"python-telegram-bot",
		"pandas",
		"google-api-core",
		"google-auth-httplib2",
		"google-auth-oauthlib",
	],
	data_files=[('', 'timtools/client_secret.json')]
)
