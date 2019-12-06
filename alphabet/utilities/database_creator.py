'''
Python script which will create a new database 
'''
import MySQLdb
from utilities.credentials import MYSQL_USER, MYSQL_PASSWORD
from django.db import connections
from django.core import management

# function the create settings for dynamic database on settings
def database_dict(domain_name):
	database_settings = {}
	database_settings['ENGINE'] = 'django.db.backends.mysql'
	database_settings['NAME'] = domain_name
	database_settings['USER'] = 'root'
	database_settings['PASSWORD'] = 'root'
	return database_settings

# function to create database on mysql programmatically
def create_database(domain_name):
	try:
		db = MySQLdb.connect('localhost', MYSQL_USER,MYSQL_PASSWORD)
		cursor = db.cursor()
		cursor.execute("create database IF NOT EXISTS %s" % (domain_name))
		db.close()
	except Exception as e:
		print (e)
	

# automating the process of database migration
def migrate_new_database(company_name):
	try:
		management.call_command('migrate', database=company_name) 
		management.call_command('makemigrations')
	except Exception as e:
		print (e)