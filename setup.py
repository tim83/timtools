#! /usr/bin/python3
"""Manager for the python package"""

from setuptools import setup

setup(
	name='timtools',
	version='0.26',
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
		"oath2client",
	],
)
