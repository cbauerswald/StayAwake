# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:01:14 2014

@author: cauerswald
"""

import pygame
from pygame.locals import *
import random
import math
import time
import random


class Student():

    def __init__(self):
        self.energy = 10
        self.sleep = False
    
    def update(self):
        if self.sleep:
            self.energy+=0.5

class Prof():
    
    def __init__(self):
        self.teaching = False
    
    def teach(self):
        self.teaching = bool(random.getrandbits(1))

class StayAwakeModel():
    
    '''
    create player
    create prof
    when the upkey is being pressed, be more awake
    when the downkey is being pressed, be more asleep
    the more asleep you are, the more energy you get
    only at a certain amount of energy can you hear what the prof says
    There are NO levels of asleep, either you ARE or ARE NOT (i.e. boolean)
    THROUGHOUT THE WHOLE GAME: you can see how close you are to being caught by the prof
    --> so you have to balance between:
        getting enough energy to be able to answer the profs questions AND
        being awake enough that the prof does not see you 
    GAME PLAY:
        the higher the profmeter, the more you need to be awake and working
        if your energy is too low, your success working declines
        when you work poorly, the prof pays more attention to you
    '''
    
    def __init__(self):
        self.student = Student()
        self.prof = Prof()
    
    def update(self):
        self.prof.teach()
        #print self.prof.teaching
        self.student.update()
        print self.student.sleep
        #if self.student.energy<5:
            
        

class StayAwakePygameController:
    
    def __init__(self, model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key==pygame.K_SPACE:
            model.student.sleep = True
        else:
            model.student.sleep = False
    
        

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    
    model = StayAwakeModel()
    controller = StayAwakePygameController(model)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                controller.handle_keyboard_event(event)
        model.update()
        time.sleep(0.001)
        
    pygame.quit()
    
    
    
        
        
    