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
    
    def update(self):
        if self.suspicion>9.7:
            pass
            #self.looking = True #if suspicion goes up to about 10, the prof catches you. be careful!
        if self.suspicion > 7.5:
            rand = random.randint(1, 200-int(self.suspicion))  # if suspicion is above 7.5, the prof might catch you. the higher above, the more likely you'll be caught
            if rand<1:
                pass
                #self.looking = True
                
class StayAwakeModel():
    
    def __init__(self):
        self.student = Student()
        self.prof = Prof()
        self.play = True
    
    def update(self):
        #self.prof.teach()
        self.student.update()
        if self.student.sleep>2 and self.prof.suspicion<10:
            #print "up susp"
            self.prof.suspicion += self.student.sleep/100
        elif self.student.sleep<=2 and self.prof.suspicion >0:
            self.prof.suspicion += 0.01
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
        if event.key==pygame.K_DOWN:
            model.student.stayAwake()
        elif event.key == pygame.K_UP:
            model.student.goToSleep()
    
class StayAwakeView:# The view for the game. This gets the images of the game!
    """A view of brick breaker rendered"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        #initializes the game with this Image!
        ball = pygame.image.load("background2.jpg")
        ballrect = ball.get_rect()
        screen.blit(ball, ballrect)              

        
    def draw(self): #state is the sleepiness of the student
        #imports the image file of the student. There are 4 images for the student, one for each level of sleepiness.        
        state = self.model.student.sleep        
        if int(state) == 1: #Most awake:
            ball = pygame.image.load("background2.jpg")
            ballrect = ball.get_rect()
            screen.blit(ball, ballrect)
        elif int(state) == 2:
            ball = pygame.image.load("background2.jpg")
            ballrect = ball.get_rect()
            screen.blit(ball, ballrect)
        elif int(state) == 3:
            ball = pygame.image.load("background3.jpg")
            ballrect = ball.get_rect()
            screen.blit(ball, ballrect)
        elif int(state) == 4:
            ball = pygame.image.load("background4.jpg")
            ballrect = ball.get_rect()
            screen.blit(ball, ballrect)
        elif int(state) == 5: #Asleep!
            ball = pygame.image.load("background5.jpg")            
            ballrect = ball.get_rect()
            screen.blit(ball, ballrect)
        pygame.display.update()
        
if __name__ == '__main__':
    pygame.init()
    size = (900, 700)
    screen = pygame.display.set_mode(size)
    
    #MVC BELOW!!!!!!!!!!!!!!!
    model = StayAwakeModel()
    controller = StayAwakePygameController(model)
    view = StayAwakeView(model, screen) #<== View    
    running = True
    #Yeahhhhhhh!!!!!!!!!!!!!!
    
    
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
        black = Color(0,0,0)
        sleeplabel = myfont.render("sleep: "+str(model.student.sleep), 1, black)
        energylabel = myfont.render("energy: "+str(model.student.energy),1, black)
        suslabel = myfont.render("suspicion: "+str(model.prof.suspicion),1,black)
        #screen.fill(pygame.Color(255,255,255))
        if model.play== False:
            loselabel = myfont.render("YOU LOST",1,white)
            screen.blit(loselabel, (100, 200))
        screen.blit(sleeplabel, (100,20))
        screen.blit(energylabel, (100,100))
        screen.blit(suslabel, (100,150))
        screen.blit(suslabel, (100,150))
        pygame.display.flip()
        #if model.play == False:
            #do some sort of end game thing on the screen, maybe with an option to start over
         #   running = False #maybe don't end this here but I'm going to for now
        #print "sleep: "+str(model.student.sleep)+" , energy: "+str(model.student.energy)
        time.sleep(0.001)
        view.draw()
        
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
    
    
    
        
        
    