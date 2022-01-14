# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 23:11:50 2022

@author: surya
"""

import numpy as np
from tkinter import *
import tkinter as tk
import math
import random

canva = Tk()
canva.wm_title('Simulation')
canvas = Canvas(canva, width=1000, height=1000, bg='black')
canvas.grid(row=0, column=0)

G = 3*10**(-1)
G_dash = 6.67*10**(-11)
planets = []
l_rad = 1.5
PI = math.pi

class Black_hole():
    def __init__(self, mass, posx, posy):
        self.m = mass
        self.P = np.array([posx,posy], dtype=float)
        self.R = (3*mass/(4*math.pi*1))**(1/3)
        
class Planet():
    def __init__(self, mass, posx, posy, Vel):
        self.m = mass
        self.P = np.array([posx,posy], dtype=float)
        self.R = (3*mass/(4*math.pi*1))**(1/3)
        self.V = Vel
        
    def Motion(self, b_h, dt):
        r = math.sqrt((self.P[0]-b_h.P[0])**2 + (self.P[1]-b_h.P[1])**2)
        r_vec = np.array([(self.P[0]-b_h.P[0])/r, (self.P[1]-b_h.P[1])/r], dtype=float)
        F_vec = -G*self.m*b_h.m*r_vec/r**2
        dV = (F_vec/self.m)*dt
        
        self.V += dV
        #print(self.V[0])
        
    def LRL_Vector(self, b_h):
        p_vec = self.m*self.V
        r = math.sqrt((self.P[0]-b_h.P[0])**2 + (self.P[1]-b_h.P[1])**2)
        r_unit_vec = np.array([(self.P[0]-b_h.P[0])/r, (self.P[1]-b_h.P[1])/r], dtype=float)
        r_vec = r*r_unit_vec
        #LRL = np.array([np.cross(r_vec,p_vec)*p_vec[1], -np.cross(r_vec,p_vec)*p_vec[0]], dtype=float) 
        MKR = - G*b_h.m*self.m**2*r_unit_vec
        MKR_mag = math.sqrt(MKR[0]**2 + MKR[1]**2)
        MKR_vec = MKR/MKR_mag*50
        PL = np.array([np.cross(r_vec,p_vec)*p_vec[1], -np.cross(r_vec,p_vec)*p_vec[0]], dtype=float)
        PL_mag = math.sqrt(PL[0]**2 + PL[1]**2)
        PL_vec = PL/PL_mag*50
        LRL = PL + MKR
        LRL_mag = math.sqrt(LRL[0]**2 + LRL[1]**2)
        LRL_vec = LRL/LRL_mag*80
        canvas.create_line(self.P[0], self.P[1], self.P[0]+MKR_vec[0], self.P[1]+MKR_vec[1], arrow=tk.LAST, width=5, fill='blue')
        canvas.create_line(self.P[0], self.P[1], self.P[0]+PL_vec[0], self.P[1]+PL_vec[1], arrow=tk.LAST, width=5, fill='green')
        canvas.create_line(self.P[0], self.P[1], self.P[0]+LRL_vec[0], self.P[1]+LRL_vec[1], arrow=tk.LAST, width=5, fill='red')
        print(LRL_mag)
        
if __name__ == "__main__":
    OBJECTS = 1
    MASSIVE_BODY = 1
    
    m_b = Black_hole(1000, random.randrange(450,550), random.randrange(450,550))
    
    for i in range(OBJECTS):
        planets.append(Planet(random.randrange(10,30), random.randrange(500, 650), random.randrange(500, 650), [random.uniform(-1.3,1.3), random.uniform(-1.3,1.3)]))
        print(planets[i].R)     ##500-800

    T = 0
    flag = True
    x = planets[0].P[0]
    y = planets[0].P[1]
    dt = 0.1
    
    while flag:
        canvas.delete('all')
        
        canvas.create_oval(m_b.P[0]-m_b.R, m_b.P[1]-m_b.R, m_b.P[0]+m_b.R, m_b.P[1]+m_b.R, fill='red')
        
        for obj in planets:
            obj.Motion(m_b, dt)
            obj.LRL_Vector(m_b) 
            obj.P += obj.V*dt  
            canvas.create_oval(obj.P[0]-obj.R, obj.P[1]-obj.R, obj.P[0]+obj.R, obj.P[1]+obj.R, fill='orange')

        canvas.update()
        
        T += dt
        if T > 100000:
            flag = False
       
    canva.destroy() 
        