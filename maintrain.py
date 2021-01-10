import pygame
from pygame.locals import *
import numpy as np
from crossing import *
from streets import *
from car import *
from crash import *
from settings import *
from city import *
from RL import *

class game():
    def __init__(self):
        pygame.init()
#       self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.mode = 0
        self.city = City()
        if loadcity:
            self.city = self.city.load()
            self.mode = 2
        self.cars = []
        self.crashes = []
        self.shot = 0
        self.learner = QLearner()
        self.crashcounter = 0
        """
        0: create crossings
        1: create streets
        2: run game
        """

           
    def run2(self):
        """
        structure:
        1) update all objects, cars make their decision where to go next
        2) animate the movement of the cars
        3) when cars have reached their target, detect crashes and collect
           cars that are still there
        """ 

        # make decisions for cars
        for car in self.cars:
            car.action = self.learner.choose_action(car.state)
            car.update(act=car.action)
#           car.update()


        self.cars, self.crashes = self.city.update()
        self.crashcounter += len(self.crashes)
        
        for car in self.cars:
            # pass feedback to learner
            car.new_state = car.info()
            self.learner.learn(car.state, car.action ,car.feedback,car.new_state) 
            car.state = car.new_state
        
              
    def run(self):
        for i in range(1000):
            self.run2()



game().run()