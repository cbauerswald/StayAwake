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
energy is on a scale of -5 - 5
    you cannot stay awake if your energy is less than 2.5
    you get delirious when your energy is less than 5
suspicion is on a scale of 0-10
    when it is above 7.5, there is an increasingly random chance that the prof will look
    when it gets above 9.5 (aka is about 10), the prof looks!
    
'''
class Student():

    def __init__(self):
        self.energy = 0
        self.sleep = 0
    
    def update(self):
        if self.sleep <=0:
            self.sleep =0.0 #you never want sleep to go below 0 because thats just dumb
        elif self.sleep>=5.0:
            self.sleep=5.0
        if self.sleep>2 and self.energy<5:
            self.energy+=0.005*self.sleep #if sleep is greater than 2, you get energy!
        elif self.energy>-5: #only happens if self.sleep is less than  or = to 2n"            
            self.energy+=-0.01 #if sleep is not greater than 2, you lose energy!
        if self.sleep<5 and self.energy <=0:
            self.sleep+=0.01 #if sleep is less than 5, you naturally fall asleep, unless you have enough energy
        time.sleep(0.1) #add a pause so that you don't just fall right asleep. this may not be the best way to do this/place to do this, but it works for now...

    def stayAwake(self):
        if self.energy > 0:
            self.sleep += -0.05 #if you have enough energy, you wake up!
            time.sleep(0.1)
    
    def goToSleep(self):
        self.sleep +=0.05
        time.sleep(0.1)
        

class Prof():
    def __init__(self):
        self.suspicion = 0
        self.looking = False
        self.level = 1
    
    def update(self):
        if self.suspicion>9.7:
            pass
            self.looking = True #if suspicion goes up to about 10, the prof catches you. be careful!
        if self.suspicion > 7.5:
            rand = random.randint(1, 200-int(self.suspicion))  # if suspicion is above 7.5, the prof might catch you. the higher above, the more likely you'll be caught
            if rand<1:
                pass
                self.looking = True      
        
class Coffee:
    def __init__(self, xinit, yinit):
        self.xinit = xinit
        self.xpos= xinit
        self.ypos = yinit
        self.vx =0
    
    def coffeeGo(self, vx):
        self.vx = vx
    
    def coffeeMove(self):
        self.xpos +=self.vx
        if self.xpos<=0:
            self.xpos = self.xinit
            self.vx =0
    

                
class StayAwakeModel():
    
    def __init__(self, windowwidth, windowheight):
        self.student = Student()
        self.prof = Prof()
        self.play = True
        self.coffee = Coffee(windowwidth +10, windowheight/2)
        self.time = 0
        self.waited =0
        self.coffeebonus = False
    
    def update(self, time):
        self.waited += (time - self.time )/1000 #add the delta time to waited
        self.time = time
        if int(self.waited) == random.randint(5,20): #if the time that has passed is some random number between 5 and 20 seconds, send a coffee
            self.coffee.coffeeGo(-1)
            self.waited =0 #reset waited to 0 once the coffee has gone by
        self.coffee.coffeeMove() #move the coffee, this could just go 0
        self.student.update()
        if self.student.sleep>2 and self.prof.suspicion<10:
            self.prof.suspicion += self.student.sleep/100
        elif self.student.sleep<=2 and self.prof.suspicion >0:
            self.prof.suspicion +=-0.01*self.prof.level
        self.prof.update()
        if self.prof.looking == True and self.student.sleep<2 or self.student.energy<=-5:
            print "he saw :("
            self.play = False
        if self.coffeeBonus:
            self.addCoffeeBonus()  
    
    def addCoffeeBonus(time):
        #if time<
        self.student.energy += 2

class StayAwakePygameController:
    
    def __init__(self, model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key==pygame.K_DOWN:
            model.student.stayAwake()
        elif event.key == pygame.K_UP:
            model.student.goToSleep()
        elif event.key == pygame.K_SPACE:
            if self.model.coffee.vx!=0:
                self.model.coffeebonus = True
    
        

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
        if model.play== False:
            loselabel = myfont.render("YOU LOST",1,white)
            screen.blit(loselabel, (100, 200))
        screen.blit(sleeplabel, (100,20))
        screen.blit(energylabel, (100,100))
        screen.blit(suslabel, (100,150))
        pygame.display.flip()
        #if model.play == False:
            #do some sort of end game thing on the screen, maybe with an option to start over
         #   running = False #maybe don't end this here but I'm going to for now
        #print "sleep: "+str(model.student.sleep)+" , energy: "+str(model.student.energy)
        time.sleep(0.001)
        
    pygame.quit()
    #print model.student.sleep

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
    
    
    
        
        
    