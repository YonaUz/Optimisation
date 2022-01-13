# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:33:18 2021

@author: yonau
"""

import numpy as np
class Maximisation:
    """Classe de Maximisation 
    implémente le code de simplex dans 
    le cas de maximisation avec contrainte d'égalité
    """
    def __init__(self):
        self.nb_variables=0
        self.nb_contraintes=0
        #POUR + DE VARIABLES FAIRE UN TABLEAU ICI C4EST UN EXEMPLE
        self.a=0
        self.b=0
        self.c=0

    def saisie(self):
        while True:
            try:
                self.nb_variables=int(input("Combien y a t-il de variables ?: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Mercie bien")
        while True:
            try:
                self.nb_contraintes=int(input("Combien y a t-il de contraintes ?: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Mercie bien")
        self.table=np.zeros((self.nb_contraintes + 1,self.nb_variables + self.nb_contraintes+2)) #nb lignes, nb colonnes 
        self.contraintes=np.zeros((1,self.nb_contraintes)) #tableau à valeurs nulles de taille 1*nb de contraites 
                                                            #permettra l'indentation des variables 
        self.ligneprise=[]                                                    
        self.construction_tableau() 
        print(self.table)
        
    def construction_tableau(self):
        for j in range(self.nb_variables):
            while True:
                try:
                    self.table[0,j]=-int(input("Coeff de la {0} e variable dans Z: ".format(j+1))) #premiere ligne Z
                    break
                except ValueError:
                    print("Ooups ! Ceci n'est pas un nombre réessayez svp. Mercie bien")
            self.table[0,self.nb_variables + self.nb_contraintes]= 1 #+Z coefficient unitaire 
        print(self.table)
        for i in range(1,self.nb_contraintes+1): # lignes 
            for j in range(self.nb_variables): #colonnes
                while True:
                    try:
                        self.table[i,j]=int(input("Coeff de la {0} e variable dans la {1} e contrainte: ".format(j+1, i))) 
                        break
                    except ValueError:
                        print("Ooups ! Ceci n'est pas un nombre réessayez svp. Mercie bien")
                #la saisie de l'utilisateur doit s'arreter aux nb de veriables entrées avant 
                #le resste reste egal a 0
            self.table[i,self.nb_variables + self.nb_contraintes+1]=int(input("Valeur de b dans la {0} e contrainte: ".format(i))) #Valeur de b dans les contraintes 
        #forme canonique
        i=1
        j=self.nb_variables
        for k in range(self.nb_contraintes): #on fait ca uniquement pour le nb de contraintes 
            self.table[i,j]=1 #forme canonique de depart 
            i+=1 
            j+=1
        print('Construction \n',self.table)
        self.traitement()
        
    def traitement(self):
        #i=0 premiere ligne 
        #on regarde sil y a un coef <0 
        #on prend le + petit de la premiere ligne Z
        while self.poursuivre():
            self.petit=min(self.table[0]) #valeur minimale sur la premiere ligne 
            for j in range(self.nb_contraintes+self.nb_variables): #on cherche la colonne correspondante 
                if self.table[0,j]==self.petit:
                    #j+=1 #tant qu on la trouve pas on incrémente 
                    self.colonne_pivot=j
            i=1
            if self.table[i,self.colonne_pivot] !=0:
                self.quotient=self.table[1,self.nb_variables + self.nb_contraintes+1]/self.table[i,self.colonne_pivot]
                self.ligne_pivot=1
            for i in range(2,self.nb_contraintes+1): #on parcourt les lignes
                    if i not in self.ligneprise:
                        if ((self.table[i,self.nb_variables + self.nb_contraintes+1]/self.table[i,self.colonne_pivot])<self.quotient): #on compare les quotients 
                            self.quotient=self.table[i,self.nb_variables + self.nb_contraintes+1]/self.table[i,self.colonne_pivot] #on note le quotient 
                            self.ligne_pivot=i
            self.ligneprise.insert(len(self.ligneprise),self.ligne_pivot) 
            self.pivot=self.table[self.ligne_pivot,self.colonne_pivot]
            self.table=self.transformation()
            print(self.table)
            print("pivot={0}".format(self.pivot))
            print("ligne pivot={0}".format(self.ligne_pivot))
            print("colonne pivot={0}".format(self.colonne_pivot)) 
        #pas de valeur négative => optimisation terminee 
        print("Optimisation finie") 
        print(self.table)
        
        #on regarde a quelle ligne correspond le 1 de la forme canonique 
        #pour trouver les coefficients de la solution (a,b,c)
        #ATTENTION ICI CEST QUE POUR 3 VARIABLES EXEMPLE
        #FAIRE UN TABLEAU OU UNE LISTE POUR !!!!
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,0]==1:
                self.a=self.table[i,-1]
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,1]==1:
                self.b=self.table[i,-1]
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,2]==1:
                self.c=self.table[i,-1]
                
        print('Solution Optimale: Z =', self.table[0,-1])
        print("Variable 1: a={0}, \nVariable 2: b={1}, \nVariable 3: c={2}".format(round(self.a,2),round(self.b,2),round(self.c,2)))
        
        
    def poursuivre(self):
        """poursuivre est une fonction qui parcourt la premiere ligne du tableau
        et qui determine si une optimisation est encore possible
        ie s'il existe un coef <0 a la premiere ligne"""
        self.alors=False
        for j in range(self.nb_variables + self.nb_contraintes): #colonnes
            if self.table[0,j]<0:
                self.alors=True
        return(self.alors)
        
    def transformation(self):
        for i in range(self.nb_contraintes+1):
            if i!=self.ligne_pivot:
                self.l=self.table[i,self.colonne_pivot]
                for j in range(self.nb_contraintes+self.nb_variables+2):
                    self.table[i,j]=self.table[i,j]-(self.l/self.pivot)*self.table[self.ligne_pivot,j]
        for j in range(self.nb_contraintes+self.nb_variables+2):
            self.table[self.ligne_pivot,j]=self.table[self.ligne_pivot,j]/self.pivot 
        return(self.table)
        

    
coucou=Maximisation()
coucou.saisie()