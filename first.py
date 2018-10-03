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
    
session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Nicolas", "LAGAILLARDIE", 24, "contact@minbot.fr", "Sainte")
)

session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Chloe", "GOURRAT", 22, "chloeG@minbot.fr", "Sainte")
)

session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city, notes, notestxt)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    ("Chloe", "POURIDGE", 25, "chloeP@minbot.fr", "Sainte", [15,16], ["15"])
)

session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Chloe", "SAFRAN", 22, "chloeS@minbot.fr", "Sainte")
)

session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Aubin", "RABOUAN", 23, "aubin@minbot.fr", "Sainte")
)

session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Paul", "BREUGNOT", 23, "PBR@minbot.fr", "Sainte")
)

session.execute(
    """
    INSERT INTO users (firstname, lastname, age, email, city)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("Paul", "BONNET", 23, "PBE@minbot.fr", "Sainte")
)

"""Create the table before"""
rows = session.execute('SELECT firstname, lastname, age FROM users')
for user_row in rows:
    print(user_row.firstname, user_row.lastname, user_row.age)
    
rows = session.execute('SELECT firstname, lastname, age FROM users')
for row in rows:
    print(row[0], row[1], row[2])

rows = session.execute('SELECT firstname, lastname, age FROM users')
for user_row in rows:
    print(user_row.firstname, user_row.lastname, user_row.age)

# build a list of futures
futures = []
query = "SELECT * FROM users WHERE firstname=%s  ALLOW FILTERING"
FN_to_fetch = ["Chloe"]
for firstname in FN_to_fetch:
    futures.append(session.execute_async(query, [firstname]))
    
print()

# wait for them to complete and use the results
for future in futures:
    rows = future.result()
    for row in rows :
        for elt in row :
            print(elt, end="")
            print(" ", end="")
        print()
        
