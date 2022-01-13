# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 13:10:46 2022

@author: yonau
"""

import numpy as np
class Maximisation:
    """Classe de Maximisation"""
    def __init__(self):
        self.nb_variables=0
        self.nb_contraintes=0
        self.a=0
        self.b=0
        self.c=0

    def saisie(self):
        self.nb_variables=3
        self.nb_contraintes=3
        self.table=np.zeros((self.nb_contraintes + 1,self.nb_variables + self.nb_contraintes+2)) #nb lignes, nb colonnes 
        self.contraintes=np.zeros((1,self.nb_contraintes)) #tableau à valeurs nulles de taille 1*nb de contraites 
                                                            #permettra l'indentation des variables 
        self.ligneprise=[]                                                    
        self.construction_tableau() 
        
    def construction_tableau(self):
        self.table[0,0]=-4
        self.table[0,1]=1
        self.table[0,2]=-2
        self.table[0,self.nb_variables + self.nb_contraintes]= 1 #+Z coefficient unitaire 
        print(self.table)
        self.table[1,0]=2
        self.table[1,1]=1 
        self.table[1,2]=2
        self.table[2,0]=1
        self.table[2,1]=-4
        self.table[2,2]=2
        self.table[3,0]=5
        self.table[3,1]=-2
        self.table[3,2]=-2
        
        self.table[0,-1]=0
        self.table[1,-1]=6
        self.table[2,-1]=0
        self.table[3,-1]=4
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
                if self.table[i,self.colonne_pivot]!=0 : #si pas de div par zero on continue 
                    if i not in self.ligneprise:
                        if ((self.table[i,self.nb_variables + self.nb_contraintes+1]/self.table[i,self.colonne_pivot])<self.quotient): #on compare les quotients 
                            self.quotient=self.table[i,self.nb_variables + self.nb_contraintes+1]/self.table[i,self.colonne_pivot] #on note le quotient 
                            self.ligne_pivot=i
            self.ligneprise.insert(len(self.ligneprise),self.ligne_pivot) 
            self.pivot=self.table[self.ligne_pivot,self.colonne_pivot]
            self.table=self.transformation()
            print("pivot={0}".format(self.pivot))
            print("ligne pivot={0}".format(self.ligne_pivot))
            print("colonne pivot={0}".format(self.colonne_pivot)) 
        #pas de valeur négative => optimisation terminee 
        print("Optimisation finie") 
        print(self.table)
        print('Solution Optimale: Z =', self.table[0,-1])
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,0]==1:
                self.a=self.table[i,-1]
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,1]==1:
                self.b=self.table[i,-1]
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,2]==1:
                self.c=self.table[i,-1]
        print("a = {0}, b= {1}, c={2}".format(self.a,self.b,self.c))
        
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