import spyral
import pygame
import time

class Mono(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        #self.scene = scene
        self.image = spyral.Image(filename="images/monkey_normal.png")
        self.grito = pygame.mixer.Sound("sounds/smile.wav")
        self.x = 100
        self.y = 300

    def sonreir(self):
        self.image = spyral.Image(filename="images/monkey_smile.png")
        self.scene.redraw()
        self.grito.play()
        #self.image = spyral.Image(filename="images/monkey_normal.png")
        
