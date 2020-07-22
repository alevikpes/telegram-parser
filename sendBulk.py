#!/usr/bin/env python3

import argparse
import sqlite3
import sys
import time

import telethon
from telethon import sync  # this module must be imported, although never used
from telethon.tl import functions, types


def sql_insert_group(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute(
        "insert into 'group' ("
        "'group_id', 'group_name', 'group_title', 'user_count'"
        ") values ("
        "?, ?, ?, ?)",
        entities)
    con.commit()

def sql_insert_user(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute(
        "insert into 'user' ("
        "'user_id', 'is_bot', 'name', 'username'"
        ") values ("
        "?, ?, ?, ?)",
        entities)
    con.commit()

def get_group_users(chat, db_con):
    print('Chat type: %s' % type(chat))
    #print(dir(chat))
    if isinstance(chat, types.Channel) or isinstance(chat, types.ChannelFull):
        print('%s | %s | %s' % (chat.id, chat.username, chat.title))
        # save group data
        sql_insert_group(
            db_con,
            (chat.id, chat.username, chat.title, chat.participants_count),
        )
        # get users list
        try:
            chat_users = client.get_participants(chat.username,
                                                 aggressive=True)
            time.sleep(3)
            return chat_users
        except Exception as e:
            if 'ChatAdminRequiredError' in str(e):
                e = 'Only admins can see the list of users in this group'

            print('Error while getting groups users:\n\t%s' % e)
            return
    elif isinstance(chat, types.ChatForbidden):
        print('%s | no username | %s' % (chat.id, chat.title))
        print('This is a private chat')
        return
    else:
        print('WARNING: Chat type is not supported: %s' % type(chat))
        return

def save_user_data(user, db_con):
    try:
        # save user data
        sql_insert_user(
            db_con,
            (user.id,
             user.bot,
             '%s %s' % (user.first_name, user.last_name),
             user.username),
        )
    except Exception as e:
        print('Error while saving user data:\n\t%s' % e)

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
                    help='Message',
                    type=str)
# parse the arguments
args = parser.parse_args()
# get the arguments value
message = args.message

# login and start
try:
    client = telethon.TelegramClient(SESSION_NAME, APP_API_ID, APP_API_HASH)
    client.start()
except Exception as e:
    print('Error while authenticating the user:\n\t%s' % e)
    sys.exit()

if client.is_user_authorized():
    print('User is authenticated')
    try:
        client.send_message('@TreeCapital1', message)
    except Exception as e:
        print(e)
        sys.exit(2)

