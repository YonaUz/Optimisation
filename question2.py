# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 11:29:35 2022

@author: yonau
"""

import numpy as np
class Maximisation:
    """Classe de Maximisation"""
    def __init__(self):
        """Constructeur : initialisation des variables"""
        self.nb_variables=0
        self.nb_contraintes=0
        self.M=1000  #une valeur très grande 
        self.liste_M=[]
        self.ligneprise=[] 

    def saisie(self):
        """On demande à l'utilisateur 
        d'entrer les coefficients """
        self.nb_variables=2
        self.nb_contraintes=3
        self.nb_superieur=3
        self.nb_inferieur=0
        self.nb_egal=0
        #nb de lignes: self.nb_contrainte + 1 
        #nb de colonnes: 2 * nb >= + nb = + nb <= +2
        self.table=np.zeros((self.nb_contraintes + 1, self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2)) #nb lignes, nb colonnes 
        self.somme=np.zeros((1, self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2)) #nb lignes, nb colonnes 
        self.construction_tableau()
        
    def construction_tableau(self):
        """On construit alors le tableau avec
        le coefficients ainsi que la forme canonique """
        self.table[0,0]=20000
        self.table[0,1]=25000
        self.table[0,-2]= 1 #+Z coefficient unitaire 
            
        #valeurs des coefficients d'abord 

        self.table[1,0]=400
        self.table[2,0]=300
        self.table[3,0]=200
        self.table[1,1]=300
        self.table[2,1]=400
        self.table[3,1]=500
        self.table[0,-1]=0 #-Z+Z=0
        self.table[1,-1]=25000 #Valeur de b dans les contraintes 
        self.table[2,-1]=27000
        self.table[3,-1]=30000
     
        #les zeros de Z 
        for j in range(self.nb_variables,self.nb_variables+self.nb_superieur+ self.nb_inferieur):
            self.table[0,j]=0
            
         #les M dans Z seront modelises par des infinis 

        for j in range(self.nb_variables+self.nb_superieur+ self.nb_inferieur,self.nb_variables+2*self.nb_superieur+ self.nb_inferieur+self.nb_egal):
             self.table[0,j]=self.M
         
        #forme canonique
            
        #pour les inegalités superieures >= d'abord: -1 
        #surplus variables
        
        i=1
        j=self.nb_variables
        for k in range(self.nb_superieur): #on fait ca uniquement pour le nb de contraintes 
            self.table[i,j]=-1 #forme canonique de depart 
            i+=1 
            j+=1
        
        #pour les inégalités inférieures <= : +1 
        #slack variables
        i=1
        j=self.nb_variables+self.nb_superieur
        for k in range(self.nb_inferieur): #on fait ca uniquement pour le nb de contraintes 
            self.table[i,j]=1 #forme canonique de depart 
            i+=1 
            j+=1
        
        #pour les inégalités superieures >= : +1 
        #artificial variables                
        i=1+self.nb_inferieur 
        j=self.nb_variables+self.nb_superieur+self.nb_inferieur
        for k in range(self.nb_superieur): #on fait ca uniquement pour le nb de contraintes 
            self.table[i,j]=1 #forme canonique de depart 
            i+=1 
            j+=1
        
        #pour les contraintes d'egalité = : +1
        #artificial variables
        i=1+self.nb_superieur+self.nb_inferieur
        j=self.nb_variables+2*self.nb_superieur+self.nb_inferieur
        for k in range(self.nb_egal): #on fait ca uniquement pour le nb de contraintes 
            self.table[i,j]=1 #forme canonique de depart 
            i+=1 
            j+=1
            
        print('construction: \n \n',self.table)
        self.preliminaires()
        
    def preliminaires(self):
        j=self.nb_variables+self.nb_superieur+self.nb_inferieur
        for k in range(self.nb_superieur):
            for i in range(1,self.nb_contraintes+1):
                if self.table[i,j+k]==1:
                    self.liste_M.append(i)
                    i+=1
        print(self.liste_M)
        for i in self.liste_M:
            for j in range(self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2):
                self.somme[0,j]+=self.table[i,j]

        print(self.somme)
        for j in range(self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2):
            self.table[0,j]=self.table[0,j]-self.M*self.somme[0,j]
        print('preliminaires: \n \n',self.table)
        
        self.traitement()
        
    def traitement(self):
        """On définit la colonne pivot, la ligne pivot 
        et le pivot ensuite on effectue les calculs"""
        
        #i=0 premiere ligne 
        #on regarde sil y a un coef <0 
        #on prend le + petit de la premiere ligne Z
        while self.poursuivre():
            self.table_variables=self.table[:,:(self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal)] #tout sauf la colonne de Z et b
            self.petit=min(self.table_variables[0]) #valeur minimale sur la premiere ligne 
            self.colonne_pivot=np.argmin(self.table_variables[0]) 
            i=1
            if self.table[i,self.colonne_pivot] !=0:
                #initialisation du quotient 
                self.quotient=self.table[1,-1]/self.table[i,self.colonne_pivot]
                self.ligne_pivot=1
            
            for i in range(2,self.nb_contraintes+1): #on parcourt les lignes
                if self.table[i,self.colonne_pivot]!=0 : #si pas de div par zero on continue 
                    if i not in self.ligneprise:
                        if ((self.table[i,-1]/self.table[i,self.colonne_pivot])<self.quotient): #on compare les quotients 
                            self.quotient=self.table[i, -1]/self.table[i,self.colonne_pivot] #on note le quotient 
                            self.ligne_pivot=i
            self.ligneprise.insert(len(self.ligneprise),self.ligne_pivot) 
            self.pivot=self.table[self.ligne_pivot,self.colonne_pivot]
            
            self.table=self.transformation()
        
        #boucle poursuivre terminee:
        #pas de valeur négative => optimisation terminee 
        print("\n Optimisation finie: \n") 
        print(self.table)
        
        # self.Z=self.table[0,self.nb_variables+2*self.nb_superieur+self.nb_inferieur+self.nb_egal+1]
        # print('Solution Optimale : Z={0}'.format(self.Z))
        
        self.Z=self.table[0,-1]

        #on regarde a quelle ligne correspond le 1 de la forme canonique 
        #pour trouver les coefficients de la solution (a,b,c)
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,0]==1:
                self.a=self.table[i,-1]
        for i in range(1,self.nb_contraintes+1):
            if self.table[i,1]==1:
                self.b=self.table[i,-1]
        print("Variable 1: a={0}, \nVariable 2: b={1}".format(round(self.a,2),round(self.b,2)))
        print('Solution Optimale : Z={0}'.format(round(-self.Z,2)))
        
    def poursuivre(self):
        """poursuivre est une fonction qui parcourt la premiere ligne du tableau
        et qui determine si une optimisation est encore possible
        ie s'il existe un coef <0 a la premiere ligne"""
        
        self.alors=False
        for j in range(self.nb_variables + 2*self.nb_superieur+self.nb_inferieur+self.nb_egal): #colonnes
            if self.table[0,j]<0:
                self.alors=True
        return(self.alors)
        
    def transformation(self):
        """On traite les coefficients, on effectue 
        les calculs et on fait le changement des lignes"""
        
        for i in range(self.nb_contraintes+1):
            if i!=self.ligne_pivot:
                self.l=self.table[i,self.colonne_pivot]
                for j in range(self.nb_variables+2*self.nb_superieur+self.nb_inferieur+self.nb_egal+2):
                    self.table[i,j]=self.table[i,j]-(self.l/self.pivot)*self.table[self.ligne_pivot,j]
        for j in range(self.nb_variables+2*self.nb_superieur+self.nb_inferieur+self.nb_egal+2):
            self.table[self.ligne_pivot,j]=self.table[self.ligne_pivot,j]/self.pivot 
        print('Transformation: \n',self.table)
        return(self.table)
    

coucou=Maximisation()
coucou.saisie() 
