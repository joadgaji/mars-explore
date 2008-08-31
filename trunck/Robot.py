try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from pygame.locals import *
        import random
        import thread


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class Robot:
        def __init__(self, mapaxy):
                self.positionx = (mapaxy%12) *50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.speed = 5
                self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
        def move(self, mov):
                if mov == 1:
                        self.moveup()
                elif mov == 2:
                        self.movedown()
                elif mov == 3:
                        self.moveright()
                elif mov == 4:
                        self.moveleft()
                
                
                
        def moveup(self):
                self.pos = self.pos.move(0, -self.speed)
                #if self.pos.top < 0:
                 #       self.pos.top = 500
                        
        def movedown(self):
                self.pos = self.pos.move(0, self.speed)
                #if self.pos.top > 500:
                 #       self.pos.top = 0
                        
        def moveright(self):
                self.pos = self.pos.move(self.speed, 0)
                #if self.pos.right > 600:
                 #       self.pos.left = 0

        def moveleft(self):
                self.pos = self.pos.move(-self.speed, 0)
                #if self.pos.right < 0:
                 #       self.pos.left = 600
