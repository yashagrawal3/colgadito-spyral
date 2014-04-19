# -*- coding: utf-8 -*-

import spyral
import pygame

import sys
import os
import random
import logging
logging.debug(os.path.abspath('.'))

SIZE = (1000, 750)
BG_COLOR = (255, 255, 255)
FG_COLOR = (0, 0, 0)
GREY = (125, 125, 125)

archivo = open("frases.txt", "r")
# desciframos
frases = unicode(archivo.read().decode("utf-8")).splitlines()
# una frase al azar
frase = frases[random.randint(0, len(frases)-1)]
archivo.close()

class Colgadito(spyral.Sprite):
    def __init__(self, scene):
        super(Colgadito, self).__init__(scene)

        self.anchor = 'bottomright'
        self.y = SIZE[1] 
        self.x = SIZE[0]

        self.update(6)


    def update(self, intentos):
        if intentos>=6:
            self.image = spyral.Image(filename="images/Hangman-0.png")
        elif intentos==5:
            self.image = spyral.Image(filename="images/Hangman-1.png")
        elif intentos==4:
            self.image = spyral.Image(filename="images/Hangman-2.png")
        elif intentos==3:
            self.image = spyral.Image(filename="images/Hangman-3.png")
        elif intentos==2:
            self.image = spyral.Image(filename="images/Hangman-4.png")
        elif intentos==1:
            self.image = spyral.Image(filename="images/Hangman-5.png")
        elif intentos==0:
            self.image = spyral.Image(filename="images/Hangman-6.png")
        self.image.scale((512,512))


class Descartadas(spyral.Sprite):
    def __init__(self, scene):
        super(Descartadas, self).__init__(scene)

        font_path = "SFDigitalReadout-Medium.ttf"
        self.font = spyral.Font(font_path, 72, GREY)
        self.image = self.font.render(scene.erradas)
        self.text = ""

        self.anchor = 'midtop'

        self.x = SIZE[0]/2
        self.y = 300

    def update(self, scene):
        if self.text:
            self.set_text(self.text)
        else:
            self.image = self.font.render(scene.erradas)

    def set_text(self, text):
        self.image = self.font.render(text)
        self.text = text


class Tablero(spyral.Sprite):
    def __init__(self, scene):
        super(Tablero, self).__init__(scene)

        self.completo = False

        font_path = "SFDigitalReadout-Medium.ttf"
        self.font = spyral.Font(font_path, 50, FG_COLOR)
        self.image = self.font.render("")
        self.text = ""

        self.anchor = 'midtop'

        self.x = SIZE[0]/2
        self.y = 50

    def set_text(self, text):
        self.image = self.font.render(text)
        self.text = text

    def mostrar(self, frase, acertadas):
        total = 0
        estado = ""
        for letra in frase:
            if letra in acertadas:
                estado = estado + " " + letra
                total = total + 1
            else:
                estado = estado + " _"

        if total==len(frase):
            self.completo = True

        self.set_text(estado)
        

class Finale(spyral.Scene):
    def __init__(self, text, ganaste):
        spyral.Scene.__init__(self, SIZE)

        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)

        self.text = text 
        font_path = "SFDigitalReadout-Medium.ttf"
        font = spyral.Font(font_path, 72, FG_COLOR)

        self.finale = spyral.Sprite(self)
        self.finale.image = font.render(self.text)
        self.finale.anchor = 'midtop'
        self.finale.x = SIZE[0]/2
        self.finale.y = SIZE[1]/2

        #if ganaste:
        #    animation = spyral.Animation('y', spyral.easing.Sine(300), shift=450, duration=3, loop=True)
        #else:
        #    animation = spyral.Animation('x', spyral.easing.Sine(300), shift=600, duration=3, loop=True)
        #self.finale.animate(animation)

        spyral.event.register("input.keyboard.down.*", self.procesar_tecla)
        self.closing = False
        spyral.event.register("system.quit", sys.exit)

    def procesar_tecla(self):
        print "HOLA DESDE FINALE"
        if not self.closing:
            spyral.director.pop()
            self.closing = True


class Game(spyral.Scene):
    """
    A Scene represents a distinct state of your game. They could be menus,
    different subgames, or any other things which are mostly distinct.
    """
    def __init__(self):
        global SIZE
        pantalla = pygame.display.get_surface()
        SIZE = pantalla.get_size()

        spyral.Scene.__init__(self, SIZE)

        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)
        self.erradas = ""

        self.hangman = Colgadito(self)
        self.tablero = Tablero(self)
        self.descartadas = Descartadas(self)
        self.setup()

        pygame.mixer.init()
        self.bonus = pygame.mixer.Sound('sounds/BonusCube_0.ogg')
        self.fallo = pygame.mixer.Sound('sounds/Hurt_0.ogg')
        self.exito = pygame.mixer.Sound('sounds/chipquest.wav')
        self.pierde = pygame.mixer.Sound('sounds/punch.wav')
        self.aplauso = pygame.mixer.Sound('sounds/applause.wav')
        
        pygame.mixer.music.load('sounds/snare.wav')
        pygame.mixer.music.play(-1)

        spyral.event.register("input.keyboard.down.*", self.procesar_tecla)
        spyral.event.register("system.quit", sys.exit)

    def setup(self):
        frase = frases[random.randint(0, len(frases)-1)]
        self.intentos = 6
        self.erradas = ""
        self.acertadas = " "
        self.tablero.completo = False

        self.sinacentos = ''
        for letra in frase:
            if letra==u"á":
                letra = "a"
            if letra==u"é":
                letra = "e"
            if letra==u"í":
                letra = "i"
            if letra==u"ó":
                letra = "o"
            if letra==u"ú":
                letra = "u"
            self.sinacentos = self.sinacentos + letra

        self.hangman.update(self.intentos)
        self.tablero.mostrar(self.sinacentos, self.acertadas)
        self.descartadas.update(self)

    def procesar_tecla(self, key):
        print "Hola desde el juego"
        if not 0<key<255:
            return
        
        respuesta = chr(key)

        if respuesta in self.sinacentos:
            self.acertadas = self.acertadas + respuesta
            self.bonus.play()
        else:
            if self.intentos==0:
                self.perdiste()
            else:
                self.erradas = self.erradas + respuesta
                self.intentos = self.intentos - 1
                self.fallo.play()

        self.hangman.update(self.intentos)
        self.tablero.mostrar(self.sinacentos, self.acertadas)
        self.descartadas.update(self)

        if self.tablero.completo:
            self.ganaste()

    def ganaste(self):
        self.exito.play()
        self.aplauso.play()
        self.final(1)

    def perdiste(self):
        self.pierde.play()
        self.final(0)

    def final(self, ganaste):
        spyral.director.push(Finale(self.sinacentos, ganaste))
        self.setup()


if __name__ == "__main__":
    spyral.director.init(SIZE) # the director is the manager for your scenes
    spyral.director.run(scene=Game()) # This will run your game. It will not return.
