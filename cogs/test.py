# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 07:36:15 2020
@author: @Xalava
"""

import random
choix = ["casserole", "cuillere", "patate", "souris"]
solution = random.choice(choix)

solution = "casserole"
tentatives = 7
affichage = ""
lettres_trouvees = ""

for l in solution:
  affichage = affichage + "_ "

print(">> Bienvenue dans le pendu <<")

while tentatives > 0:
  print("\nMot à deviner : ", affichage)
  proposition = input("proposez une lettre : ")[0:1].lower()

  if proposition in solution:
      lettres_trouvees = lettres_trouvees + proposition
      print("-> Bien vu!")
  else:
    tentatives = tentatives - 1
    print("-> Nope\n")
    if tentatives==0:
        print(" ==========Y= ")
    if tentatives<=1:
        print(" ||/       |  ")
    if tentatives<=2:
        print(" ||        0  ")
    if tentatives<=3:
        print(" ||       /|\ ")
    if tentatives<=4:
        print(" ||       /|  ")
    if tentatives<=5:                    
        print("/||           ")
    if tentatives<=6:
        print("==============\n")

  affichage = ""
  for x in solution:
      if x in lettres_trouvees:
          affichage += x + " "
      else:
          affichage += "_ "

  if "_" not in affichage:
      print(">>> Gagné! <<<")
      break
     
print("\n    * Fin de la partie *    ")