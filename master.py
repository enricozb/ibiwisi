import mouse
import socket

from connection import Connection

import time

import pyglet

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Master:
    def __init__(self, port):
        self.connection = Connection(port)

        self.width, self.height = 200, 200
        self.window = pyglet.window.Window(self.width, self.height)
    
    def set_slave(self, addr):
        self.connection.set_sink(addr)
    
    def set_size(self, width, height):
        if self.width == width and self.height == height:
            return
        self.width, self.height = width, height
        self.window.set_size(width, height)

    def on_draw(self):
        # display slave screen
        # send mouse/keyboard events
        mssg = self.connection.recv()
        with open('k.jpg', 'wb') as out:
            out.write(mssg)
        img = pyglet.sprite.Sprite(img=pyglet.image.load('k.jpg'))
        img.scale = 0.3
        img.draw()
        self.connection.send('ready')
        
    def on_mouse_motion(self, x, y, dx, dy):
        window_x, window_y = self.window.get_location()
        mouse.set_position(window_x + self.width // 2, window_y + self.height // 2)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def run(self):
        self.window.event(self.on_mouse_motion)
        self.window.event(self.on_mouse_drag)
        self.window.event(self.on_mouse_press)
        self.window.event(self.on_mouse_release)
        self.window.event(self.on_draw)
        pyglet.app.run()
