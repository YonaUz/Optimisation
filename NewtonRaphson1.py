# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 23:03:33 2022

@author: yonau
"""

class Newton_Raphson1:
    """La méthode de Newton Raphson1 permet de trouver la 
    solution de l'équation f(x)=0 
    INPUT a: borne inférieure de l'intervalle
    INPUT b: borne supérieure de l'intervalle 
    INPUT epsilon: valeur de epsilon
    OUTPUT n: nombre d'itérations nécessaires
    OUTPUT: x*: solution optimale """
    def __init__(self):
        self.fonction=0
        self.intervalle_min=0
        self.intervalle_max=0
    
    def saisie(self):
        while True:
            try:
                self.a=float(input("borne inférieure de l'intervalle: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
                
        while True:
            try:
                self.b=float(input("borne supérieure de l'intervalle: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
                
        while True:
            try:
                self.epsilon=float(input("Valeur de ε: "))
                break
            except ValueError:
                print("Ooups ! Ceci n'est pas un nombre réessayez svp. Merci bien")
                
        self.processus()
        
    def f(self,x):
        return(x**4-5*x**3+9*x+3)
    
    def f_prime(self,x,dx=1e-6):
        return((self.f(x+dx)-self.f(x-dx))/(2*dx))
    
    def processus(self):
        self.x0=(self.a+self.b)/2
        self.x=[self.x0]
        self.n=0 #nb d'iterations
        while abs(self.f(self.x[self.n]))>self.epsilon:
            #print(self.x)
            self.x.append(self.x[self.n]-(self.f(self.x[self.n])/self.f_prime(self.x[self.n])))
            self.n+=1
        print('Résultat obtenu au bout de n={0} itérations'.format(self.n))
        print('La solution optimale est : x*={0}'.format(self.x[self.n]))
        


coucou=Newton_Raphson1()
coucou.saisie()
