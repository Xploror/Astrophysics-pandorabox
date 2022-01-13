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

G = 6.67*10**(-4)
G_dash = 6.67*10**(-11)
planets = []
l_rad = 1.5
PI = math.pi

class Black_hole():
    def __init__(self, mass, posx, posy):
        self.m = mass
        self.P = np.array([posx,posy], dtype=float)
        self.R = (3*mass/(4*math.pi*0.5))**(1/3)
        
class Planet():
    def __init__(self, mass, posx, posy, Vel):
        self.m = mass
        self.P = np.array([posx,posy], dtype=float)
        self.R = (3*mass/(4*math.pi))**(1/3)
        self.V = Vel
        
    def Motion(self, b_h):
        r = math.sqrt((self.P[0]-b_h.P[0])**2 + (self.P[1]-b_h.P[1])**2)
        r_vec = np.array([(self.P[0]-b_h.P[0])/r, (self.P[1]-b_h.P[1])/r], dtype=float)
        F_vec = -G*self.m*b_h.m*r_vec/r**2
        dV = (F_vec/self.m)
        
        self.V += dV
        #print(self.V[0])
        
    def lagrange(self, b_h):
        r = math.sqrt((self.P[0]-b_h.P[0])**2 + (self.P[1]-b_h.P[1])**2)
        r_vec = np.array([(self.P[0]-b_h.P[0])/r, (self.P[1]-b_h.P[1])/r], dtype=float)
        R = r*(self.m/(3*b_h.m))   # Since R/r = (m/3*M)^(1/3)
        self.L1x = b_h.P[0] + (r-R)*r_vec[0]
        self.L1y = b_h.P[1] + (r-R)*r_vec[1]
        self.L2x = b_h.P[0] + (r+R)*r_vec[0]
        self.L2y = b_h.P[1] + (r+R)*r_vec[1]
        self.L3x = b_h.P[0] - (r-R)*r_vec[0]
        self.L3y = b_h.P[1] - (r-R)*r_vec[1]
        rot_mat_L4 = np.array([[math.cos(60*PI/180), -math.sin(60*PI/180)], [math.sin(60*PI/180), math.cos(60*PI/180)]], dtype=float)
        rot_mat_L5 = np.array([[math.cos(-60*PI/180), -math.sin(-60*PI/180)], [math.sin(-60*PI/180), math.cos(-60*PI/180)]], dtype=float)
        L4_vec = np.matmul(rot_mat_L4,r_vec)
        L5_vec = np.matmul(rot_mat_L5,r_vec)
        self.L4x = b_h.P[0] + r*L4_vec[0]
        self.L4y = b_h.P[1] + r*L4_vec[1]
        self.L5x = b_h.P[0] + r*L5_vec[0]
        self.L5y = b_h.P[1] + r*L5_vec[1]
        
    def LRL_Vector(self, b_h):
        p_vec = self.m*self.V
        r = math.sqrt((self.P[0]-b_h.P[0])**2 + (self.P[1]-b_h.P[1])**2)
        r_unit_vec = np.array([(self.P[0]-b_h.P[0])/r, (self.P[1]-b_h.P[1])/r], dtype=float)
        r_vec = r*r_unit_vec
        LRL = np.array([np.cross(r_vec,p_vec)*p_vec[1], -np.cross(r_vec,p_vec)*p_vec[0]], dtype=float) - G*b_h.m*self.m**2*r_unit_vec
        LRL_mag = math.sqrt(LRL[0]**2 + LRL[1]**2)
        LRL_vec = LRL/LRL_mag*80
        canvas.create_line(self.P[0], self.P[1], self.P[0]+LRL_vec[0], self.P[1]+LRL_vec[1], arrow=tk.LAST, width=5, fill='blue')
        print(LRL_vec)
        
if __name__ == "__main__":
    OBJECTS = 1
    MASSIVE_BODY = 1
    
    m_b = Black_hole(1000, random.randrange(450,550), random.randrange(450,550))
    
    for i in range(OBJECTS):
        planets.append(Planet(random.randrange(100,300), random.randrange(500, 650), random.randrange(500, 650), [random.uniform(-0.15,0.15), random.uniform(-0.3,0.3)]))
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
            obj.Motion(m_b)
            obj.P += obj.V*dt  
            obj.lagrange(m_b)
            obj.LRL_Vector(m_b)
            canvas.create_oval(obj.P[0]-obj.R, obj.P[1]-obj.R, obj.P[0]+obj.R, obj.P[1]+obj.R, fill='orange')
            canvas.create_oval(obj.L1x-l_rad, obj.L1y-l_rad, obj.L1x+l_rad, obj.L1y+l_rad, fill='white')
            canvas.create_oval(obj.L2x-l_rad, obj.L2y-l_rad, obj.L2x+l_rad, obj.L2y+l_rad, fill='white')
            canvas.create_oval(obj.L3x-l_rad, obj.L3y-l_rad, obj.L3x+l_rad, obj.L3y+l_rad, fill='white')
            canvas.create_oval(obj.L4x-l_rad, obj.L4y-l_rad, obj.L4x+l_rad, obj.L4y+l_rad, fill='white')
            canvas.create_oval(obj.L5x-l_rad, obj.L5y-l_rad, obj.L5x+l_rad, obj.L5y+l_rad, fill='white')
            
        canvas.update()
        
        T += dt
        if T > 100000:
            flag = False
       
    canva.destroy() 
        