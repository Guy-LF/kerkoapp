
from PIL import Image, ImageDraw, ImageFont
import platforms
import re

def test_post():
    a = platforms.Twitter()
    media = a.api.media_upload("test.png")
    b=a.api.update_status(status="hello", media_ids=[media.media_id])
    return

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def format_text(text=None):
    if not text:
        text = "0123456789"*100 # test string
    return(re.sub("(.{64})", "\\1\n", text, 0, re.DOTALL))

def main(title=None, text=None, author=None, year=None):

    fontname = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" #or -Bold.ttf  
    fontsize = 11 
    
    if not text:
        text = format_text(("Gross et al. (2015) have demonstrated that about a quarter of hits would typically be lost to keyword searchers" * 10))
    
    full_text = f"{author} {year}\n title: {title}\n {text}"
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"


    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, height/2), fulltext, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    img.thumbnail((600,400))
    img.save("test.png")
