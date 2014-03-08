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

'''
sleep is on scale of 0-5
    when it is less that 2, you are perceived to be awake
    you gain energy proportional to your sleepiness when your sleepiness is greater than 2
energy is on a scale of 0-10
    you cannot stay awake if your energy is less than 2.5
    you get delirious when your energy is less than 5
suspicion is on a scale of 0-10
    when it is above 7.5, there is an increasingly random chance that the prof will look
    when it gets above 9.5 (aka is about 10), the prof looks!
    
'''
class Student():

    def __init__(self):
        self.energy = 10
        self.sleep = 0
    
    def update(self):
        if self.sleep>2:
            self.energy+=0.005*self.sleep
        else:
            self.energy+=-0.005 
        if self.sleep<5:
            self.sleep+=0.05
            time.sleep(0.1)
    
    def stayAwake(self):
        if self.energy > 5:
            self.sleep += -0.15

class Prof():
    def __init__(self):
        self.suspicion = 0
        self.looking = False
    
    def update(self):
        if self.suspicion>9.7:
            self.looking = True
        if self.suspicion > 7.5:
            rand = random.randint(1, int(self.suspicion))
            if rand>9:
                self.looking = True
                
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
        self.play = True
    
    def update(self):
        #self.prof.teach()
        self.student.update()
        if self.student.sleep>2:
            self.prof.suspicion += self.student.sleep/100
        self.prof.update()
        if self.prof.looking == True:
            print "he saw :("
            self.play = False
        

class StayAwakePygameController:
    
    def __init__(self, model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key==pygame.K_SPACE:
            model.student.stayAwake()
    
        

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    
    model = StayAwakeModel()
    controller = StayAwakePygameController(model)
    running = True
    
    pygame.display.set_caption("Text adventures with Pygame")
    # pick a font you have and set its size
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    # apply it to text on a label
    label = myfont.render("lets display some stuff!", 1, Color(255,255,255))
    # put the label object on the screen at point x=100, y=100
    screen.blit(label, (100, 100))
    # show the whole thing
    pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                controller.handle_keyboard_event(event)
        model.update()
        white = Color(255,255,255)
        sleeplabel = myfont.render("sleep: "+str(model.student.sleep), 1, white)
        energylabel = myfont.render("energy: "+str(model.student.energy),1, white)
        suslabel = myfont.render("suspicion: "+str(model.prof.suspicion),1,white)
        screen.fill(pygame.Color(0,0,0))
        screen.blit(sleeplabel, (100,20))
        screen.blit(energylabel, (100,100))
        screen.blit(suslabel, (100,150))
        pygame.display.flip()
        if model.play == False:
            #do some sort of end game thing on the screen, maybe with an option to start over
            running = False #maybe don't end this here but I'm going to for now
        #print "sleep: "+str(model.student.sleep)+" , energy: "+str(model.student.energy)
        time.sleep(0.001)
        
    pygame.quit()
    #print model.student.sleep
    
    
    
        
        
    