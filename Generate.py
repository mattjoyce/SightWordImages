"""Create a set of images of rendered text"""
import sys
import string
from PIL import Image, ImageDraw, ImageFont 
from  random import random
import colorsys
import optparse

def generate(im_width, im_height, text, img_scale, fontfile, jpg_quality):
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
    color = colorsys.hsv_to_rgb(random(), 0.5, 0.95)
    color_rgb = tuple([int(256*x) for x in color])
    draw.text(((im_width-text_width) / 2, (im_height-text_height) / 2), 
                text, fill = (color_rgb), font=font)
    filename = text.translate(string.maketrans("",""), string.punctuation)
    new_image.save(filename+".jpg", "jpeg",quality=jpg_quality)

def main(argv=None):
    """ Read a text file, take each line and create a image file"""
    parser = optparse.OptionParser()
    parser.add_option('-y', '--height', dest='y', type='int', 
                        help="Vertical size of images in pixels, default=600", default='600' )
    parser.add_option('-x', '--width', dest='x', type='int',  
                        help="Horizontal size of images in pixels, default=800", default='800' )
    parser.add_option("-t", "--infile", dest="infile", default='test.txt',
                  help="FILE containing text, one item per line, default=test.txt", metavar="FILE")
    parser.add_option("-f", "--font", dest="font", default='comic.ttf',
                  help="truetype font FILE, default='comic.tff'", metavar="FILE")
    parser.add_option('-q', '--quality', dest='quality', type='int', 
                        help="JPEG quality, 0-100 (100-high), default=90", default='90' )
    (options, args) = parser.parse_args()
    
    lines = open(options.infile).readlines()
    for line in lines:
        generate(options.x, options.y, line, 1, options.font, options.quality)

if __name__ == "__main__":
    sys.exit(main())
