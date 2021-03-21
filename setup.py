#! /usr/bin/python3
"""Manager for the python package"""

from setuptools import setup

setup(
	name='timtools',
	version='0.29.2',
	packages=['timtools'],
	url='',
	license='',
	author='Tim Mees',
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
	include_package_data=True
)
