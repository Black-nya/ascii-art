from PIL import Image, ImageFont, ImageDraw
import argparse
import numpy as np
import time,sys,traceback
from pygame import mixer

class Var:
    def __init__(self, font = None, symbols = " .-^*x#", sample_rate = 0.3, bg_color = "black", brightness = 1):

        self.print = sys.stdout.write # Parameter must be a str object

        # Defines all the symbols in ascending order that will form the final ascii
        self.symbols = np.array(list(symbols))

        # Normalize to [0, max_symbol_index)
        self.normalize = np.rint(np.arange(256) / 255 * (self.symbols.size - 1)).astype(int)

        # Compute letter aspect ratio
        if font:
            self.font = ImageFont.truetype(font) # numpy.str_ is acceptable
        else:
            self.font = ImageFont.load_default() # numpy.str_ is not acceptable
            
        width, height = self.font.getbbox("x")[2], self.font.getbbox("x")[3]
        self.aspect_ratio =  width/height 
        self.letter_size = (width, height)

        self.sample_rate = sample_rate
        self.bg_color = "black"
        self.brightness = 1

def simple_brighter(color, factor):
    r, g, b = color
    r = min(255, int(r*factor))
    g = min(255, int(g*factor))
    b = min(255, int(b*factor))
    return r, g, b

def ascii_art(file, var, test = False, save = False, output = False):

    if test:
        t = time.time()
    
    im = Image.open(file)

    new_im_size = np.array(
        [im.size[0] * var.sample_rate, im.size[1] * var.sample_rate * var.aspect_ratio]
    ).astype(int)
    
    # Downsample the image
    im = im.resize(new_im_size)
    
    # Keep a copy of image for color sampling
    im_color = np.array(im)

    # Convert to gray scale image
    im = im.convert("L")
    
    # Convert to numpy array
    im = np.array(im)

    # Generate the ascii art
    im = var.normalize[im]
    
    ascii = var.symbols[im]

    # Save as a image
    if save:
        im_out_size = new_im_size * var.letter_size
        im_out = Image.new("RGB", tuple(im_out_size), var.bg_color)
        draw = ImageDraw.Draw(im_out)

        # Draw text
        y = 0
        for i, line in enumerate(ascii):
            for j, ch in enumerate(line):
                color = simple_brighter(im_color[i, j], var.brightness)  # sample color from original image
                draw.text((var.letter_size[0] * j, y), ch[0], fill=color, font=var.font)
            y += var.letter_size[1]  # increase y by letter height

        # Save image file
        im_out.save("ascii_"+file + "_ascii.png")
        
    if output:
        lines = "\n".join(("".join(r) for r in ascii))
        var.print(lines)

        if test:
            return time.time() - t
    
def bad_apple(var, frame_rate = 25, volume = 0.5, save = False, output = False):
    interval = 0

    if output:
        mixer.init()
        mixer.music.load("Bad_Apple.mp3")
        mixer.music.set_volume(volume)
        
        t = ascii_art("out/0001.jpg", var, test = True, save = save, output = output)
        interval = 1/frame_rate - t
        mixer.music.play()

    for i in range(1, 5481):
        
        ascii_art("out/%04d.jpg"%i, var, save = save, output = output)
        
        if interval > 0 :    
            time.sleep(interval)

def main():
    var = Var()
    bad_apple(var)
           
if __name__ == '__main__':
    
    try:
        pass
        
    except SystemExit:
        pass
    
    except:
        traceback.print_exc()
        input()
