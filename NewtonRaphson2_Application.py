# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 19:41:20 2022

@author: yonau
"""

import math 

class Newton_Raphson2:
    """La méthode de Newton Raphson1 permet de trouver la 
    solution de l'équation f'(x)=0 
    donc de trouver un optimum à f INPUT a: borne inférieure de l'intervalle
    INPUT b: borne supérieure de l'intervalle 
    INPUT epsilon: valeur de epsilon
    OUTPUT n: nombre d'itérations nécessaires
    OUTPUT: x*: solution optimale """
    def __init__(self):
        self.fonction=0
        self.intervalle_min=0
        self.intervalle_max=0
    
    def saisie(self):
        self.a=0.2
        self.b=0
        self.epsilon=0.01
                
        self.processus()
        
    def f(self,x):
        #faut il demander à l'utilisateur d'entrer la fonction ? mais comment faire our la rendre f(x) ? avec arg...
        #return(x**4-5*x**3+9*x+3)
        return(0.65-0.75/(1+x**2)-0.65*x*math.atan(1/x))
    
    def f_prime(self,x,dx=1e-6): #taux d'accroissement et fonction continue
        return((self.f(x+dx)-self.f(x-dx))/(2*dx))
    
    def f_seconde(self,x,dx=1e-6):
        return((self.f(x+dx)+self.f(x-dx)-2*self.f(x))/(dx**2))
    
    
    def processus(self):
        self.x0=(self.a+self.b)/2
        self.x=[self.x0]
        self.n=0 #nb d'iterations
        while abs(self.f_prime(self.x[self.n]))>self.epsilon:
            #print(self.x)
            self.x.append(self.x[self.n]-(self.f_prime(self.x[self.n])/self.f_seconde(self.x[self.n])))
            self.n+=1
        print('Résultat obtenu au bout de n={0} itérations'.format(self.n))
        print('La solution optimale est : x*={0}'.format(self.x[self.n]))
        


coucou=Newton_Raphson2()
coucou.saisie()
