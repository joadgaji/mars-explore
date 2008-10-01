#!/usr/bin/env python
background_image_filename = 'mars2.gif'
mouse_image_filename = 'robot2.png'
roca_image = "roca.png"
piedra_image = 'esmeralda.png'

import pygame
from pygame.locals import *
from sys import exit

#Esta es una version de pruebas
pygame.init()

screen = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption("Hello, World!")
background = pygame.image.load(background_image_filename).convert()
mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()
roca = pygame.image.load(roca_image).convert_alpha()
piedra = pygame.image.load(piedra_image).convert_alpha()
robot_class = robot
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
    screen.blit(background, (0,0))
    screen.blit(roca, (100,300))
    screen.blit(piedra, (300,250))
    x, y = pygame.mouse.get_pos()
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2
    screen.blit(mouse_cursor, (x, y))
    pygame.display.update()

class robot():
    x = 0
    y = 0
    def __init__(self):
        robot_image = pygame.image.load(mouse_image_filename).convert_alpha()
        screen.blit(robot_image, (x, y))
    def refrescar(self):
        screen.blit(robot_image, (x, y))
    def set_posicion(self, x1 , y1):
        self.x = x1
        self.y = y1
