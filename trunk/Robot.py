try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from pygame.locals import *
        import random
        import threading


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class Robot:
        def __init__(self, mapaxy, capacidad, surface):
                self.positionx = (mapaxy%12) *50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.speed = 5
                self.movimiento = 5
                self.frame = 10
                self.seguir = True
                self.capacidad = capacidad
                self.surface = surface
                self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (surface.get_size()[1]/ 2))

        def move(self, mapa, mutex, *args):
                while self.seguir:
                        for event in pygame.event.get():
                                if event.type in (QUIT, KEYDOWN):
                                        exit()

                        rand = random.randint(1,4)
                        posmapnew = 0
                        mutex.acquire()
                        if rand == 1:
                                posmapnew = self.mapaxy - 12
                        if rand == 2:
                                posmapnew = self.mapaxy + 12
                        if rand == 3:
                                posmapnew = self.mapaxy + 1
                                if ( posmapnew % 12 ) == 0:
                                        posmapnew  = self.mapaxy
                        if rand == 4:
                                posmapnew = self.mapaxy - 1
                                if ( posmapnew % 12 ) == 11:
                                        posmapnew = self.mapaxy
                                
                        if posmapnew >= 0  and posmapnew < 120:
                                if not(mapa.has_key(posmapnew)):
                                        mapa[posmapnew] = self
                                        del mapa[self.mapaxy]
                                        self.mapaxy = posmapnew
                                else:
                                        rand = 5
                        else:
                                rand = 5
                        mutex.release()
                        self.movimiento = rand
                        for i in range(self.frame):
                                self.movimientos()
                                pygame.time.delay(20)

        def movimientos(self):
                if self.movimiento == 1:
                        self.moveup()
                elif self.movimiento == 2:
                        self.movedown()
                elif self.movimiento == 3:
                        self.moveright()
                elif self.movimiento == 4:
                        self.moveleft()
                
        def postext(self, surface):
                return ((self.mapaxy%12) *50 +25 - height, (self.mapaxy/12) *50 + 25 - width)
        
                
        def moveup(self):
                self.pos = self.pos.move(0, -self.speed)
                self.postext = self.postext.move(0, -self.speed)
                #if self.pos.top < 0:
                 #       self.pos.top = 500
                        
        def movedown(self):
                self.pos = self.pos.move(0, self.speed)
                self.postext = self.postext.move(0, self.speed)
                #if self.pos.top > 500:
                 #       self.pos.top = 0
                        
        def moveright(self):
                self.pos = self.pos.move(self.speed, 0)
                self.postext = self.postext.move(self.speed, 0)
                #if self.pos.right > 600:
                 #       self.pos.left = 0

        def moveleft(self):
                self.pos = self.pos.move(-self.speed, 0)
                self.postext = self.postext.move(-self.speed, 0)
                #if self.pos.right < 0:
                 #       self.pos.left = 600
