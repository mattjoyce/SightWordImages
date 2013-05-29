"""Create a set of images of rendered text"""
import sys
import string
from PIL import Image, ImageDraw, ImageFont 
from  random import random
import colorsys
import optparse

def generate(im_width, im_height, text, img_scale, fontfile, 
             jpg_quality, hsv_color):
    """Create a new jpg file.
    Render the text, in the middle
    Adjust the font size to utilize the space
    """
        
    text = str(text).replace("\n", "").strip()
    new_image = Image.new("RGB", (im_width, im_height), (0, 0, 0))
    draw = ImageDraw.Draw(new_image)

    fontsize = 1
    font = ImageFont.truetype(fontfile, fontsize)
    text_width, text_height = font.getsize(text)
    
    while (text_width < img_scale*im_width and 
            text_height < img_scale * im_height)  :
        fontsize += 1
        font = ImageFont.truetype(fontfile, fontsize)
        text_width, text_height = font.getsize(text)
        
    font = ImageFont.truetype(fontfile, fontsize-1)
    if hsv_color[0]==-1:
        color = colorsys.hsv_to_rgb(random(), hsv_color[1], hsv_color[2])
    else:    
        color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
    color_rgb = tuple([int(256*x) for x in color])
    draw.text(((im_width-text_width) / 2, (im_height-text_height) / 2), 
                text, fill = (color_rgb), font=font)
    filename = text.translate(string.maketrans("",""), string.punctuation)+".jpg"
    new_image.save(filename, "jpeg",quality=jpg_quality)
    print filename

def main(argv=None):
    """ Read a text file, take each line and create a image file"""
    parser = optparse.OptionParser()
    parser.add_option('-y', '--height', dest='y', type='int', 
                        help="Vertical size of images in pixels (600)")
    parser.add_option('-x', '--width', dest='x', type='int',  
                        help="Horizontal size of images in pixels (800)")
    parser.add_option("-t", "--infile", dest="infile", metavar="FILE",
                        help="FILE containing text, one item per line (test.txt)")
    parser.add_option("-f", "--font", dest="font", metavar="FILE",
                        help="truetype font FILE (comic.ttf)")
    parser.add_option('-q', '--quality', dest='quality', type='int', 
                        help="JPEG quality, 0-100 (90)")
    parser.add_option('-c', '--hue', dest='hsv_hue', type='float', 
                        help="text HSV color hue 0-360 (random)")
    parser.add_option('-s', '--saturation', dest='hsv_saturation', type='float', 
                        help="text HSV color saturation 0.0-1.0 (0.5)")    
    parser.add_option('-v', '--value', dest='hsv_value', type='float', 
                        help="text HSV color value 0.0-1.0 (0.95)")
    parser.set_defaults(y=600, x=800, infile="test.txt", font="comic.ttf", quality=90, hsv_saturation=0.5, hsv_value=0.95, hsv_hue=-1)
    (options, args) = parser.parse_args()
    
    lines = open(options.infile).readlines()
    for line in lines:
        generate(options.x, options.y, line, 1, options.font, options.quality, [options.hsv_hue, options.hsv_saturation, options.hsv_value])

if __name__ == "__main__":
    sys.exit(main())
