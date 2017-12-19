import Quartz
import LaunchServices
import Quartz.CoreGraphics as CG

from Cocoa import NSURL

import time

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

def capture(path):
    _, displays, count = CG.CGGetActiveDisplayList(1, None, None)

    dpi = 72 # FIXME: Should query this from somewhere, e.g for retina displays
    url = NSURL.fileURLWithPath_(path)

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

    # Add the image to the destination, characterizing the image with
    # the properties dictionary.
    image = CG.CGDisplayCreateImage(displays[0])

    image = resize(image, 1200, 750)    

    Quartz.CGImageDestinationAddImage(dest, image, properties)

    # When all the images (only 1 in this example) are added to the destination, 
    # finalize the CGImageDestination object. 
    Quartz.CGImageDestinationFinalize(dest)
