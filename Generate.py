from PIL import Image, ImageDraw, ImageFont, ImageColor 
import string
from  random import random
import colorsys

def Generate(W,H,msg,img_fraction,fontname,color):
	msg=msg.replace("\n","")
	im =Image.new("RGB",(W,H),(0,0,0))
	draw = ImageDraw.Draw(im)

	fontsize=1
	font = ImageFont.truetype(fontname,fontsize)
	while font.getsize(msg)[1] < img_fraction*im.size[1] and font.getsize(msg)[0] < img_fraction*im.size[0]  :
		fontsize += 1
		font = ImageFont.truetype(fontname, fontsize)
	w, h = font.getsize(msg)
	color=colorsys.hsv_to_rgb(random(),0.5, 0.95)
	color_rgb=tuple([int(256*x) for x in color])
	print color
	print color_rgb
	draw.text(((W-w)/2,(H-h)/2), msg, fill=(color_rgb), font=font)
	fsp=msg.translate(string.maketrans("",""), string.punctuation)
	im.save(fsp+".jpg", "jpeg")

	
	
lines=open("FrysPhrases.txt").readlines()
for line in lines:
	Generate(480,234,line,0.9,"comic.ttf",'white')
