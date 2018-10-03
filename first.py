#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:03:42 2018

@author: lag
"""



from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()

"""Create the keyspace before"""
session.set_keyspace('users')

"""Create the table before"""
rows = session.execute('SELECT firstname, lastname, age FROM users')
for user_row in rows:
    print(user_row.firstname, user_row.lastname, user_row.age)
    
rows = session.execute('SELECT firstname, lastname, age FROM users')
for row in rows:
    print(row[0], row[1], row[2])
    
session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Nicolas", "LAGAILLARDIE", 24, "contact@minbot.fr", "Sainte")
)

rows = session.execute('SELECT firstname, lastname, age FROM users')
for user_row in rows:
    print(user_row.firstname, user_row.lastname, user_row.age)
    