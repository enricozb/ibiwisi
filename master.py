import mouse
import socket

from connection import Connection

import time

import pyglet

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class DummyReader:
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data

class Master:
    def __init__(self, port):
        self.connection = Connection(port)

        self.width, self.height = 200, 200
        self.window = pyglet.window.Window(self.width, self.height)
        self.last = 0
    
    def set_slave(self, addr):
        self.connection.set_sink(addr)
    
    def set_size(self, width, height):
        if self.width == width and self.height == height:
            return
        self.width, self.height = width, height
        self.window.set_size(width, height)

    def on_draw(self, val):
        curr = time.time()
        print('fps:', 1 / (curr - self.last))
        self.last = curr

        reader = DummyReader(self.connection.recv())
        img = pyglet.sprite.Sprite(img=pyglet.image.load('dummy.jpg', file=reader))
        img.scale = self.width / img.width
        img.draw()
        self.connection.send('ready')

    def on_mouse_motion(self, x, y, dx, dy):
        return
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
        pyglet.clock.schedule_interval(self.on_draw, 1/120.0)
        pyglet.app.run()
