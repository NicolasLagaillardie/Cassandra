#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:03:42 2018

@author: lag
"""

"""Utilisation de Cassandra à travers Python"""
from cassandra.cluster import Cluster

"""Pour la génération aléatoire de chaîne de caractères"""
from random import choice,randint
import string

cluster = Cluster()
session = cluster.connect()

#Sélectionne le keyspace demo
session.set_keyspace('demo')
    
#Ajout massif d'entrées
for i in range(200):

    idEleve = str(i)
    nom = "".join(choice(string.ascii_letters) for x in range(randint(5, 12)))
    prenom = "".join(choice(string.ascii_letters) for x in range(randint(5, 12)))
    nom = nom.upper()
    prenom = prenom.capitalize()
    mail = prenom.lower() + "." + nom.lower() + "@etu.emse.fr"
    telephone = "".join(choice(string.digits) for x in range(10))
    
    session.execute(
        """
        INSERT INTO eleves (idEleves, nom, prenom, mail, telephone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (idEleve, nom, prenom, mail, telephone)
    )
    
#Ajout d'une valeur connue
session.execute(
    """
    INSERT INTO eleves (idEleves, nom, prenom, mail, telephone)
    VALUES (%s, %s, %s, %s, %s)
    """,
    ("500", "Lag", "Nicolas", "Nicolas.LAGAILLARDIE@etu.emse.fr", "0612345678")
)

#Affichage de tous les noms, prénoms et mails
rows = session.execute('SELECT nom, prenom, mail FROM eleves')
for user_row in rows:
    print(user_row.nom, user_row.prenom, user_row.mail)
    
#Affichage de idEleves, cours et mail
rows = session.execute('SELECT * FROM eleves')
for row in rows:
    print(row[0], row[1], row[2])

# Affichage des entrées dont le prénom est Nicolas à l'aide d'un requête asynchrone
futures = []
query = "SELECT * FROM eleves WHERE prenom=%s  ALLOW FILTERING"
FN_to_fetch = ["Nicolas"]
for prenom in FN_to_fetch:
    futures.append(session.execute_async(query, [prenom]))
    
print()

# Attente puis affichage des résultats asynchrones
for future in futures:
    rows = future.result()
    for row in rows :
        for elt in row :
            print(elt, end="")
            print(" ", end="")
        print()