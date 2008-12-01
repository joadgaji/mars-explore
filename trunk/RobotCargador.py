try:
        import sys
        import random
        import math
        import os
        import getopt
        import time
        import pygame
        from pygame.locals import *
        import random
        import threading
        from Robot import Robot
        from RobotMensaje import *

except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class RobotCargador(Robot, RobotMensaje):
    def __init__(self, mapaxy, capacidad, fontrob, nave, nombre):
        self.positionx = (mapaxy%12) *50
        self.positiony = (mapaxy/12) *50
        self.mapaxy = mapaxy
        self.speed = 5
        self.movimiento = 5

        self.nave = nave
        
        self.movanterior = 0
        self.movactual = 0
        
        self.frame = 10
        self.seguir = True
        self.capacidad = capacidad
        self.cargadas = 0
        self.obstaculo = False
        self.rand = 0
        self.capas = []

        self.nombre = nombre
        self.buzon = []
        self.galletas = 0
        
        self.dejarmoronas = False
        self.nummorona = 1
        self.valuemorona = 0
        
        self.fontrob = fontrob
        self.surface = self.fontrob.render(str(self.cargadas), True, (255,255,255))
        self.image = pygame.image.load('Resources/robotcargador.png').convert_alpha()
        self.pos = self.image.get_rect().move(self.positionx, self.positiony)
        self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))

    def dispararcapas(self, capas, mapa, mutex, mensajes, mensajeKQML, robots, *args):
        while self.seguir:
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    exit()
            mutex.acquire()
            self.capas = capas
            mutex.release()

            for a in self.capas:
                if a == 1:
                    if self.evitarobs(mapa,mutex, self.nave):
                        break
                if a == 2:
                    if self.regresoAPos(mapa,mutex, self.nave):
                        break
                if a == 3:
                    if self.contrato(mapa, mutex, mensajes, mensajeKQML, robots):
                       
                        break
                if a == 4:
                    
                    if self.cargaesme(mapa, mutex, ""):
                        
                        break
                if a == 5:
                    if self.explorar(mapa, mutex):
                        break
       


    def contrato(self, mapa, mutex, mensajes, mensajeKQML, robots):
        entreCapa = False
        mutex.acquire()
        entreCapa = self.mandarContrato(mutex, mensajes, robots)
        
        mutex.release()

        if not(entreCapa):
            
            return False
        time.sleep(1)
        
        mutex.acquire()
        entreCapa = self.aceptarContrato(mapa, mutex)
        mutex.acquire()
        self.buzon = []
        mutex.release()
        return entreCapa

    def aceptarContrato(self, mapa, mutex):
        tamano = len(self.buzon)
        if tamano == 0:
                mutex.release()
                return False
        if tamano != 0:
            posesme = self.buzon[0]
            mutex.release()
            self.irAEsme(mapa, mutex, posesme)
            return True

    def mandarContrato(self, mutex, mensajes, robots):
        if len(mensajes):
            for i in mensajes:
                agente, posesme = i
                mov = abs(posesme%12 - self.positionx / 50) + abs(posesme/12 - self.positiony / 50)
            
                if mov < 15:
                    
                    noAgente = int(agente.strip("robot"))
                    robots[noAgente].buzon += [[self.mapaxy, self.capacidad, self.nombre]]
            return True
        else:
            return False



