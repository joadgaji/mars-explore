try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        import time
        from pygame.locals import *
        import random
        import threading
        from Robot import Robot


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class RobotExplorador(Robot):
    def __init__(self, mapaxy, capacidad, fontrob, nave, nombre):
        self.positionx = (mapaxy%12) *50
        self.positiony = (mapaxy/12) *50
        self.mapaxy = mapaxy
        self.speed = 5
        self.movimiento = 5

        self.nave = nave
        
        self.movanterior = 0
        self.movactual = 0

        self.nombre = nombre
        self.buzon = []
        self.galletas = 0
        
        self.frame = 10
        self.seguir = True
        self.capacidad = capacidad
        self.cargadas = 0
        self.obstaculo = False
        self.rand = 0
        self.capas = []

        self.fontrob = fontrob
        self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
        self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
        self.pos = self.image.get_rect().move(self.positionx, self.positiony)
        self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))

    def dispararcapas(self, capas, mapa, mutex, mensajes, mensajeKQML, cargadores, *args):
            while self.seguir:
                for event in pygame.event.get():
                    if event.type in (QUIT, KEYDOWN):
                        exit()
                mutex.acquire()
                self.capas = capas
                mutex.release()
                for a in self.capas:
                    if a == 1:
                        if self.evitarobs(mapa, mutex, self.nave):
                            break
                    if a == 3:
                        if self.negociacion(mapa, mutex, mensajes, mensajeKQML, cargadores):
                            break
                    if a == 5:
                        if self.explorar(mapa, mutex):
                            break

    def negociacion(self, mapa, mutex, mensajes, mensajeKQML, cargadores):
        cargue = False
        h = self.hayAlgo(mapa,mutex, "esmeralda", "buscar")
        if h != -1:
            cargue = True
            mutex.acquire()
            if mapa.has_key(h):
                self.mandaMensaje(mensajes, h, mensajeKQML, mutex, "informar")
            mutex.release()
            time.sleep(1)
            mutex.acquire()
            for i in mensajes:
                    agente, pos = i
                    if agente == self.nombre:
                            mensajes.remove(i)
            tamano = len(self.buzon)
            self.evaluarBuzon(tamano, h, cargadores,mensajeKQML)
            mutex.release()
            self.obstaculo = True
        return False

    def evaluarBuzon(self, tamano, h, cargadores, mensajeKQML):
        if tamano == 0:
            return
        if tamano == 1:
            self.aceptarMensaje(self.buzon[0], h, cargadores, mensajeKQML)
        if tamano > 1:
            self.aceptarMensaje(self.evaluaMensajes(), h, cargadores, mensajeKQML)

    def evaluaMensajes(self):
        movx = abs(self.mapaxy%12 - self.buzon[0][0]%12)
        movy = abs(self.mapaxy/12 - self.buzon[0][0]/12)
        winner = [movx+movy,self.buzon[0][1], self.buzon[0][2]]
        for i in self.buzon[1:]:
            mov = abs(self.mapaxy%12 - i[0]%12) + abs(self.mapaxy/12 - i[0]/12)
            if mov < winner[0]:
                winner = [mov, i[1], i[2]]
            if mov == winner[0]:
                if i[1] > winner[1]:
                    winner = [mov, i[1], i[2]]
        return winner

    def aceptarMensaje(self, winner, h, cargadores, mensajeKQML):
        referencia = int(winner[2].strip("cargador"))
        cargador = cargadores[referencia]
        cargador.buzon += [h]
        cargador.galletas += 1
        self.galletas += 1
        self.buzon = []
        mensajeKQML.append([self.nombre, h, "Contratado", winner[2], 1]) 
##        print "(Contratado-KQML"
##        print ":sender", self.nombre
##        print ":receiver", winner[2]
##        print ":language KQML"
##        print ":ontology marte-sinamigos"
##        print ":content Se acepta contrato con esmeraldas en: (", h%12 + 1, ",",  h/12 +1,")"
##        print "         y recompensa de: ", noGalletas,")"
##        print ""

    def mandaMensaje(self, mensajes, posesme, mensajeKQML, mutex, tipomsj):
        longMens = len(mensajes)
        mensajes.append((self.nombre, posesme))
        mensajeKQML.append([self.nombre, posesme, tipomsj, "broadcast", 0])

##        print "(" + tipomsj + "-KQML"
##        print ":sender", self.nombre
##        print ":receiver broadcast"
##        print ":language KQML"
##        print ":ontology marte-sinamigos"
##        print ":content hay esmeraldas en: (", posesme%12 + 1, ",",  posesme/12 +1,"))"
##        print ""

        def explorar(self, mapa, mutex):
           rand = random.randint(1,4)
           self.move(mapa, mutex, rand)
           return True

        def move(self, mapa, mutex, movactual):
                rand = movactual
                posmapnew = 0
                
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

                self.movanterior = rand
                mutex.acquire()        
                if posmapnew >= 0  and posmapnew < 120:
                        if not(mapa.has_key(posmapnew)):
                                mapa[posmapnew] = self
                                del mapa[self.mapaxy]
                                self.mapaxy = posmapnew
                        else:
                                rand = 5
                                self.obstaculo = True
                else:
                        rand = 5
                        self.obstaculo = True
                mutex.release()
                self.movimiento = rand
                for i in range(self.frame):
                        self.movimientos()
                        pygame.time.delay(25)

                return rand
