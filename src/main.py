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
parser.add_argument('-g',
                    '--groupname',
                    help='Specify target group name',
                    type=str)
parser.add_argument('-u',
                    '--username',
                    help='Specify target user name',
                    type=str)
# parse the arguments
args = parser.parse_args()
# get the arguments value
target_group = args.groupname
target_user = args.username
# remove `@` if specified
if target_group and target_group.startswith('@'):
    target_group = target_group.split('@')[1]

if target_user and target_user.startswith('@'):
    target_user = target_user.split('@')[1]

# login and start
try:
    client = telethon.TelegramClient(SESSION_NAME, APP_API_ID, APP_API_HASH)
    client.start()
except Exception as e:
    print('Error while authenticating the user:\n\t%s' % e)
    sys.exit()

chats = []
if client.is_user_authorized():
    print('User is authenticated')
    if target_group:
        try:
            chat_obj = client(functions.channels.GetChannelsRequest(
                id=[target_group]
            ))  # returns Chats obj with minimal number of data
            # chat_obj = client(functions.channels.GetFullChannelRequest(
            #     channel=target_group
            # ))  # returns ChatFull obj with much data
            print(chat_obj.stringify())
            group = chat_obj.chats[0]
        except Exception as e:
            print(e)
            sys.exit(2)

        chats = [group]
    else:
        # get all chats of the currently logged in user
        last_date = None
        chunk_size = 500
        # TODO some channels may have FullChannel attr, with a
        # `participant_count` attribute, which can be used instead
        # of the following method
        result = client(functions.messages.GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=types.InputPeerEmpty(),
            limit=chunk_size,
            hash=0,
        ))
        chats = result.chats

print('number of chats: %d' % len(chats))

# connect database
connection = sqlite3.connect(DB_NAME, check_same_thread=True)

# get groups participants
for chat in chats:
    chat_users = get_group_users(chat, connection)
    if chat_users:
        users_in_chat = len(chat_users)
        print('\tnumber of users: %d' % users_in_chat)
        for user in chat_users:
            save_user_data(user, connection)

    print('============================================')

connection.close()
