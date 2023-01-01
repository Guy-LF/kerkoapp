
from PIL import Image, ImageDraw, ImageFont
import platforms

def test_post():
    a = platforms.Twitter()
    media = a.api.media_upload("test.png")
    b=a.api.update_status(status="hello", media_ids=[media.media_id])
    return

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def main():

    fontname = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" #or -Bold.ttf  
    fontsize = 11   
    text = """
    Gross et al. (2015) have demonstrated that about a quarter\n of hits would typically be lost to keyword searchers\n"""
    
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"


    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    img.thumbnail((600,400))
    img.save("test.png")
