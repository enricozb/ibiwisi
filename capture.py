import builtins
import LaunchServices
import numpy as np
import Quartz
import Quartz.CoreGraphics as CG

from Cocoa import NSURL
from PIL import Image

debug = False

def print(*args, **kwargs):
    if debug:
        builtins.print(*args, **kwargs)

class DummyWriter:
    name = 'dummy.jpeg'
    bytes_arr = []

    def write(content):
        DummyWriter.bytes_arr.append(content)

    def flush():
        pass

    def get_bytes():
        data = b''.join(DummyWriter.bytes_arr)
        DummyWriter.bytes_arr = []
        return data

def resize(image, w, h):
    context = CG.CGBitmapContextCreate(
            None, w, h,
            CG.CGImageGetBitsPerComponent(image),
            CG.CGImageGetBytesPerRow(image) // CG.CGImageGetWidth(image) * w,
            CG.CGImageGetColorSpace(image),
            CG.CGImageGetAlphaInfo(image))

    CG.CGContextSetInterpolationQuality(context, CG.kCGInterpolationHigh)

    CG.CGContextDrawImage(context, CG.CGContextGetClipBoundingBox(context), image);
    return CG.CGBitmapContextCreateImage(context);

from time import time

_, displays, count = CG.CGGetActiveDisplayList(1, None, None)

def get_bytes_quartz(image):
    s = time()
    dpi = 72 # FIXME: Should query this from somewhere, e.g for retina displays
    url = NSURL.fileURLWithPath_('capture.jpg')

    dest = Quartz.CGImageDestinationCreateWithURL(
        url,
        LaunchServices.kUTTypeJPEG, # file type
        1, # 1 image in file
        None
    )

    properties = {
        Quartz.kCGImagePropertyDPIWidth: dpi,
        Quartz.kCGImagePropertyDPIHeight: dpi,
    }

    Quartz.CGImageDestinationAddImage(dest, image, properties)
    Quartz.CGImageDestinationFinalize(dest)

    data = open('capture.jpg', 'rb').read()
    print(f'Time to get data (Quartz): {time() - s}')
    return data

def get_bytes_pil(image):
    # Grab raw pixel data (remove alpha channel)
    width = CG.CGImageGetWidth(image)
    height = CG.CGImageGetHeight(image)
    bytesperrow = CG.CGImageGetBytesPerRow(image)
    pixeldata = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
    image = np.frombuffer(pixeldata, dtype=np.uint8)
    image = image.reshape((height, bytesperrow//4, 4))
    image = image[:,:width,1:]

    # Use PIL & DummyWriter to get byte data
    s = time()
    image = Image.fromarray(image)
    print(f'Time to fromarray (PIL):   {time() - s}')

    s = time()
    image.save(DummyWriter)
    print(f'Time to image.save (PIL):  {time() - s}')

    s = time()
    data = DummyWriter.get_bytes()
    print(f'Time t0 get_bytes (PIL):   {time() - s}')
    return data

def capture():
    s = time()
    # Capture and resize
    image = CG.CGDisplayCreateImage(displays[0])
    image = resize(image, 1200, 750)    
    print(f'Time to capture:           {time() - s}')

    return get_bytes_quartz(image)
 
