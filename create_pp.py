import os
import cv2

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from urllib.request import Request, urlopen

from io import BytesIO



def get_pic(url, username):
    # print(str(url))
    url = str(url)
    size = (256,256)
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # print(type(webpage))
    img = Image.open(BytesIO(webpage)).convert("RGBA")
    # img = Image.open(username+".png").convert("RGBA")
    img = img.resize(size)

    new_image = Image.new("RGBA", img.size, "WHITE") # Create a white rgba background
    new_image.paste(img, (0, 0))
    new_image.resize(size)
    
    

    n = Image.new('RGB', (256, 40))
    draw = ImageDraw.Draw(n)
    # font = ImageFont.truetype(<font-file>, <font-size>)


    # font = ImageFont.load_default()
    

    font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
    font = ImageFont.truetype(font_path, size=32)

    # font = ImageFont.truetype("arial.ttf",32)
    # draw.text((x, y),"Sample Text",(r,g,b))
    
    
    
    draw.text((1, -1), username, font=font, fill="black")
    draw.text((1, -1), username, font=font, fill="black")
    draw.text((-1, 1), username, font=font, fill="black")
    draw.text((-1, 1), username, font=font, fill="black")
    draw.text((0, 0),username,(254,254,254),font=font)

    new_image.paste(n, (0,256-40))

    new_image.save('./pp/'+username+'.png')
    
    return 0