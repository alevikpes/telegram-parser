#!/usr/bin/env python3

import sqlite3


# read environment variables
with open('.env', 'r') as f:
    for line in f:
        key, val = line.strip().split('=')
        globals()[key] = val

# connect sqlite
connection = sqlite3.connect(DB_NAME, check_same_thread=True)
cursor = connection.cursor()
# create tables
cursor.execute(
    "CREATE TABLE IF NOT EXISTS 'group' ("
    "'id' INTEGER PRIMARY KEY,"
    "'group_id' TEXT,"
    "'group_name' TEXT,"
    "'group_title' TEXT,"
    "'user_count' INTEGER)"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS 'user' ("
    "id INTEGER PRIMARY KEY,"
    "user_id TEXT,"
    "is_bot BOOLEAN,"
    "name TEXT,"
    "username TEXT)"
)
# commit
connection.commit()
connection.close()
