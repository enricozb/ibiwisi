from Quartz.CoreGraphics import (CGEventCreateMouseEvent,
                                 kCGEventMouseMoved,
                                 kCGMouseButtonLeft,
                                 CGEventPost,
                                 kCGHIDEventTap)

def set_position(x, y):
    event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event)

def position():
    pass

