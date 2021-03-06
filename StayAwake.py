# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:01:14 2014

@author: cauerswald
"""
import os, pygame
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

#functions to load images. Taken from the pygame website. Awwwww Yeaaah! Thnx Pygame!
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

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
            self.energy+=0.02*self.sleep #if sleep is greater than 2, you get energy!
        elif self.energy>-5: #only happens if self.sleep is less than  or = to 2n"            
            self.energy+=-0.1 #if sleep is not greater than 2, you lose energy!
        if self.sleep<5 and self.energy <=0:
            self.sleep+=0.02 #if sleep is less than 5, you naturally fall asleep, unless you have enough energy
        time.sleep(0.1) #add a pause so that you don't just fall right asleep. this may not be the best way to do this/place to do this, but it works for now...

    def stayAwake(self):
        if self.energy > 0:
            self.sleep += -0.2 #if you have enough energy, you wake up!
            time.sleep(0.1)
    
    def goToSleep(self):
        self.sleep +=0.2
        time.sleep(0.1)
        

class Prof(): #Professor class
    def __init__(self):
        self.suspicion = 0
        self.looking = False
        self.level = 1
    
    def update(self):
        #print "suspicion: " + str(self.suspicion)
        if self.suspicion>9:
            self.looking = True #if suspicion goes up to about 10, the prof catches you. be careful!
        elif self.suspicion > 7.5:
            rand = random.randint(1, 200-int(self.suspicion))  # if suspicion is above 7.5, the prof might catch you. the higher above, the more likely you'll be caught          
            if rand<10:
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
    
    def __init__(self, windowwidth, windowheight, start_time):
        self.student = Student()
        self.prof = Prof()
        self.play = True #should be TRUE
        self.coffee = Coffee(windowwidth +10, windowheight/2)
        self.time = start_time
        self.waited =0
        self.coffeebonus = False
    
    def update(self, time):
        if self.play:
            if (self.prof.looking and self.student.sleep>=2) or self.student.energy<=-5:
                print "he saw :("
                self.play = False
            self.waited += (time - self.time )/1000.0 #add the delta time to waited
            #print self.waited
            self.time = time
            if int(self.waited) == random.randint(5,10): #if the time that has passed is some random number between 5 and 20 seconds, send a coffee
                self.coffee.coffeeGo(-1)
                self.waited =0 #reset waited to 0 once the coffee has gone by
            if int(self.waited)>10:
                self.waited =0
            #print "vx: "+str(self.coffee.vx)+"\n"+ "xpos: " +str(self.coffee.xpos) + "\n"
            self.coffee.coffeeMove() #move the coffee, this could just go 0
            self.student.update()
            if self.student.sleep>2 and self.prof.suspicion<10:
                self.prof.suspicion += self.student.sleep/30
            elif self.student.sleep<=2 and self.prof.suspicion >0:
                self.prof.suspicion +=-0.01*self.prof.level
            self.prof.update()
            if self.coffeebonus:
                self.addCoffeeBonus()  
    
    def addCoffeeBonus(self):
        if self.waited<0.2 and self.student.energy<=3:
            self.student.energy += 2
        elif self.waited<0.2 and self.student.energy>3:
            self.student.energy +=5.0-self.student.energy
        elif self.waited>2:
            self.student.sleep -=1
            self.waited =0
            self.coffeebonus = False


class StayAwakePygameController:
    
    def __init__(self, model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN or not self.model.play:
            return 
        if event.key==pygame.K_DOWN:
            model.student.stayAwake()
        elif event.key == pygame.K_UP:
            model.student.goToSleep()
        elif event.key == pygame.K_SPACE:
            if self.model.coffee.vx!=0:
                self.model.waited = 0
                self.model.coffeebonus = True
                self.model.coffee.vx = 0
                self.model.coffee.xpos = self.model.coffee.xinit
                

    
class StayAwakeView:# The view for the game. This gets the images of the game!
    """A view of brick breaker rendered"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        #making the background image yo
        background = pygame.image.load("background.jpg")
        backgroundRect = background.get_rect()
        size = (width, height) = background.get_size()
        screen = pygame.display.set_mode(size)
        screen.blit(background, backgroundRect)         

        pygame.display.update()
    
    def energybar(self):
        energy = model.student.energy * 50
        pygame.draw.rect(screen, pygame.Color(0,0, 0), pygame.Rect(850,300 - 250,30,250-energy))
        pygame.draw.rect(screen, pygame.Color(255,0, 0), pygame.Rect(850,300 - energy,30,255+energy))
        energylabel = myfont.render("ENERGY",1,pygame.Color(255,0,0))
        screen.blit(energylabel, (824, 560))
        pygame.display.update()  
        
    def suspbar(self):
        sus = model.prof.suspicion * 20
        pygame.draw.rect(screen, pygame.Color(0,0, 0), pygame.Rect(200+sus,60,200-sus,20))
        pygame.draw.rect(screen, pygame.Color(0,0, 255), pygame.Rect(200,60,sus,20))
        suslabel = myfont.render("SUSPICION",1,pygame.Color(0,0,255))
        screen.blit(suslabel, (80, 60))
        pygame.display.update()

        
class Teacher_Sprite(pygame.sprite.Sprite):#sprite for the teacher. Teacher will turn head
    """Makes a teacher sprite who looks around."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('teacher55.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 600, 30
        
class Head_Sprite(pygame.sprite.Sprite):#sprite for the teacher. Teacher will turn head
    """Makes a teacher sprite who looks around."""
    def __init__(self, model):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.model = model

    def draw(self):
        state = model.student.sleep
        if int(state) == 0:
            self.image, self.rect = load_image('head1.jpg', 0)
        elif int(state) == 1:          
            self.image, self.rect = load_image('head1.jpg', 0)
        elif int(state) == 2:            
            self.image, self.rect = load_image('head2.jpg', 0)
        elif int(state) == 3:            
            self.image, self.rect = load_image('head3.jpg', 0) 
        elif int(state) == 4:           
            self.image, self.rect = load_image('head4.jpg', 0)
        elif int(state) == 5:
            self.image, self.rect = load_image('head4.jpg', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 60,250
              
        
        
if __name__ == '__main__':
    pygame.init()
    size = (900, 700)
    screen = pygame.display.set_mode(size)
    startback = pygame.image.load("start.jpg")
    startbackRect = startback.get_rect()
    #size = (width, height) = startback.get_size()
    screen = pygame.display.set_mode(size)
    screen.blit(startback, startbackRect)
    pygame.display.update()
    time.sleep(2)
    start_time = pygame.time.get_ticks()
    
    #MVC BELOW!!!!!!!!!!!!!!!
    model = StayAwakeModel(size[0], size[1], start_time)
    controller = StayAwakePygameController(model)
    view = StayAwakeView(model, screen) #<== View    
    running = True
    #Yeahhhhhhh!!!!!!!!!!!!!!
    
    #Sprite(s)!!!!!!!!!!!!!!!
    teacher = Teacher_Sprite()
    head = Head_Sprite(model)
    allsprites = pygame.sprite.RenderPlain((head,teacher))
    #Yeaaaaaaaaaaaaaaahhh!!!!
    
    
    pygame.display.set_caption("Stay Awake!")
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
        gametime=pygame.time.get_ticks()
        model.update(gametime)
        white = Color(255,255,255)
        black = Color(0,0,0)
        timelabel = myfont.render("Time Elapsed: "+str((pygame.time.get_ticks()-start_time)/1000),1,black)
        screen.subsurface(pygame.Rect(70, 100, 300, 100)).fill(white)
        screen.subsurface(pygame.Rect(70, 100, 300, 100)).blit(timelabel, (10, 20))
#        if model.coffee.vx!=0:
#            loselabel = myfont.render("COFFEE BONUS",1,black)
#            screen.blit(loselabel, (100, 200))
        pygame.display.flip()
        if model.play == False:
            #do some sort of end game thing on the screen, maybe with an option to start over
            print "the game is off....:("
            lose = pygame.image.load("lose.jpg")
            loseRect = lose.get_rect()
            size = (width, height) = lose.get_size()
            screen = pygame.display.set_mode(size)
            screen.blit(lose, loseRect)
            pygame.display.update()
            time.sleep(5)
            running = False #maybe don't end this here but I'm going to for now
        else:
            head.draw()
            view.energybar()       
            view.suspbar()
            allsprites.update()
            allsprites.draw(screen)        
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
    
    
    
        
        
    