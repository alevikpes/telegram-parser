#!/usr/bin/env python3

import argparse
import sqlite3
import sys
import time

import telethon
from telethon import sync  # this module must be imported, although never used
from telethon.tl import functions, types

def get_users(db_conn):
	cursor = db_conn.cursor()
	sql = 'SELECT * FROM user WHERE username IS NOT NULL'

	try: 
		cursor.execute(sql)

		return cursor.fetchall()
	except Exception as e:
		print('Error while read user data:\n\t%s' % e)
		return

def delete_user(id, db_conn):
	cursor = db_conn.cursor()
	sql = 'DELETE FROM user WHERE id = ?'

	try:
		cursor.execute(sql, [(id)])
		db_conn.commit()
	except Exception as e:
		print('Error while delete user:\n\t%s' % e)

	return

# read environment variables
with open('.env', 'r') as f:
	for line in f:
		key, val = line.strip().split('=')
		globals()[key] = val

# read command line arguments
# create parser
parser = argparse.ArgumentParser()
# add arguments to the parser
parser.add_argument('-m',
					'--message',
					help='Text message which will be send to user.',
					required=1,
					type=str)
parser.add_argument('-d', 
					'--delete',
					help='Delete user from DB after send message',
					action='store_true')
parser.add_argument('-t', 
					'--timeout',
					help='Timeout between send messages',
					type=int)

# parse the arguments
args = parser.parse_args()
# get the arguments value
message = args.message
delete_flag = args.delete
timeout = args.timeout or 1

# login and start
try:
	client = telethon.TelegramClient(SESSION_NAME, APP_API_ID, APP_API_HASH)
	client.start()
except Exception as e:
	print('Error while authenticating the user:\n\t%s' % e)
	sys.exit()

if client.is_user_authorized():
	print('User is authenticated')
	connection = sqlite3.connect(DB_NAME, check_same_thread=True)

	user_names = get_users(connection)
	
	for user in user_names:
		try:
			client.send_message(user[4], message)
			print('Success send - {0}'.format(user[4]))

			if delete_flag:
				delete_user(user[0], connection)
				
			time.sleep(timeout)
		except Exception as e:
			print(e)

connection.close()