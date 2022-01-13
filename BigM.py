# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:33:18 2021

@author: yonau
"""

import numpy as np
class Maximisation:
    """Classe de Maximisation
    implémente la méthode de Big M 
    dans le cas d'une maximisation à contraintes 
    d'égalité, inégalités supérieures et inférieures
    """
    def __init__(self):
        """Constructeur : initialisation des variables"""
        self.nb_variables=0
        self.nb_contraintes=0
        self.M=1000  #une valeur très grande 
        self.liste_M=[]
        self.ligneprise=[] 
        self.lignepasprise=[]
        self.liste_quotient=[]
        self.ligne_pivot=1
        self.colonne_pivot=0
        self.pivot=1
        
    def saisie(self):
        """On demande à l'utilisateur 
        d'entrer les coefficients """
        while True:
            try:
                self.nb_variables=int(input("Combien y a t-il de variables ?: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
        while True:
            try:
                self.nb_contraintes=int(input("Combien y a t-il de contraintes en tout (<=,>=, = inclus) ?: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
        while True:
            try:
                self.nb_superieur=int(input("Combien y a t-il de variables de type >= ?: ")) #ajout de variable d'ecart et de variable artificielle 
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
        while True:
            try:
                self.nb_inferieur=int(input("Combien y a t-il de contraintes de type <= ?: ")) #ajout de variable d'écart 
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
        while True:
            try:
                self.nb_egal=int(input("Combien y a t-il de contraintes de type = ?: ")) #ajout de variable artificielle 
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
        #nb de lignes: self.nb_contrainte + 1 
        #nb de colonnes: 2 * nb >= + nb = + nb <= +2
        self.table=np.zeros((self.nb_contraintes + 1, self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2)) #nb lignes, nb colonnes 
        self.somme=np.zeros((1, self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2)) #nb lignes, nb colonnes 
        self.lignepasprise=[x for x in range(1,self.nb_contraintes+1)]
        self.construction_tableau()
        #print(self.table)
        
    def construction_tableau(self):
        """On construit alors le tableau avec
        le coefficients ainsi que la forme canonique """
        self.somme=np.zeros((1, self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2)) #nb lignes, nb colonnes 
        self.lignepasprise=[x for x in range(1,self.nb_contraintes+1)]
        
        for j in range(self.nb_variables):
            while True:
                try:
                    self.table[0,j]=-int(input("Coeff de la {0} e variable dans Z: ".format(j+1))) #premiere ligne Z
                    break
                except ValueError:
                    print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
            self.table[0,-2]= 1 #+Z coefficient unitaire 
            
        #valeurs des coefficients d'abord 
        
        print("On affichera les coefficients d'abord pour les inegalites de type >= et ensuite pour les <= puis les =")
        for i in range(1,self.nb_contraintes+1): # lignes 
            for j in range(self.nb_variables): #colonnes
                while True:
                    try:
                        self.table[i,j]=int(input("Coeff de la {0} e variable dans la {1} e contrainte: ".format(j+1, i))) 
                        break
                    except ValueError:
                        print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
                #la saisie de l'utilisateur doit s'arreter aux nb de veriables entrées avant 
                #les autres coefficients restent egaux a 0
            self.table[i,-1]=int(input("Valeur de b dans la {0} e contrainte: ".format(i))) #Valeur de b dans les contraintes 
       
         #les zeros de Z 
        for j in range(self.nb_variables,self.nb_variables+self.nb_superieur+ self.nb_inferieur):
            self.table[0,j]=0
            
         #les M dans Z seront modelises par des infinis ~self.M=1000

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
                
        print(self.table)
        self.preliminaires()
        
    def preliminaires(self):
        j=self.nb_variables+self.nb_superieur+self.nb_inferieur
        for k in range(self.nb_superieur+self.nb_egal):
            for i in range(1,self.nb_contraintes+1):
                if self.table[i,j+k]==1:
                    self.liste_M.append(i)
                    i+=1
                    
        for i in self.liste_M:
            for j in range(self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2):
                self.somme[0,j]+=self.table[i,j]
                
        for j in range(self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal+2):
            self.table[0,j]=self.table[0,j]-self.M*self.somme[0,j]
            
        print('preliminaires: \n',self.table)
        self.traitement()
        
    def traitement(self):
        """On traite les coefficients, on effectue 
        les calculs et on fait le changement des lignes"""
        #i=0 premiere ligne 
        #on regarde sil y a un coef <0 
        #on prend le + petit de la premiere ligne Z
        while self.poursuivre():
            self.table_variables=self.table[:,:(self.nb_variables + 2*self.nb_superieur + self.nb_inferieur + self.nb_egal)] #tout sauf la colonne de Z et b
            self.petit=min(self.table_variables[0]) #valeur minimale sur la premiere ligne 
                #print("petit:",self.petit)
            self.colonne_pivot=np.argmin(self.table_variables[0]) 
        
            self.liste_quotient=[]
            for i in self.lignepasprise:
                if self.table[i,self.colonne_pivot] !=0:
                    #initialisation du quotient 
                    self.liste_quotient.append(self.table[i,-1]/self.table[i,self.colonne_pivot])
                    self.quotient=min(self.liste_quotient)
            for i in range(1,self.nb_contraintes+1):
                if self.table[i,self.colonne_pivot] !=0 and self.table[i,-1]/self.table[i,self.colonne_pivot]==self.quotient:
                    self.ligne_pivot=i
            if self.ligne_pivot in self.lignepasprise:
                self.lignepasprise.remove(self.ligne_pivot)
            
            self.pivot=self.table[self.ligne_pivot,self.colonne_pivot]
            
            self.table=self.transformation()
            
        #pas de valeur négative => optimisation terminee 
        print("Optimisation finie") 
        print(self.table)
        print("pivot={0}".format(self.pivot))
        print("ligne pivot={0}".format(self.ligne_pivot))
        print("colonne pivot={0}".format(self.colonne_pivot))
        self.Z=self.table[0,self.nb_variables+2*self.nb_superieur+self.nb_inferieur+self.nb_egal+1]
        print('Solution Optimale : Z={0}'.format(self.Z))
        
    def poursuivre(self):
        """poursuivre est une fonction qui parcourt la premiere ligne du tableau
        et qui determine si une optimisation est encore possible
        ie s'il existe un coef <0 a la premiere ligne"""
        self.alors=False
        for j in range(self.nb_variables + 2*self.nb_superieur+self.nb_inferieur+self.nb_egal+2): #colonnes
            if self.table[0,j]<0:
                self.alors=True
        return(self.alors)
        
    def transformation(self):
        for i in range(self.nb_contraintes+1):
            if i!=self.ligne_pivot:
                self.l=self.table[i,self.colonne_pivot]
                for j in range(self.nb_variables+2*self.nb_superieur+self.nb_inferieur+self.nb_egal+2):
                    self.table[i,j]=self.table[i,j]-(self.l/self.pivot)*self.table[self.ligne_pivot,j]
                    # print(self.table)
        for j in range(self.nb_variables+2*self.nb_superieur+self.nb_inferieur+self.nb_egal+2):
            self.table[self.ligne_pivot,j]=self.table[self.ligne_pivot,j]/self.pivot 
        return(self.table)


coucou=Maximisation()
coucou.saisie()