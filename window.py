from AppKit import NSScreen

def size():
    s = NSScreen.mainScreen().frame().size
    return s.width, s.height
