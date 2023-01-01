
from PIL import Image, ImageDraw, ImageFont
import platforms
import textwrap

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
    wrapper = textwrap.TextWrapper(width=100)
    return(wrapper.dedent(text))

def main(title="Not available", abstract=None, author="Not available", year="Not available"):

    fontname = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" #or -Bold.ttf  
    fontsize = 11 
    
    if not abstract:
        abstract = format_text(("Gross et al. (2015) have demonstrated that about a quarter of hits would typically be lost to keyword searchers" * 50))
    
    fulltext = format_text(text=f"First author: {author} year: {year}\n title: {title}\n {abstract}")
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"


    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(fulltext, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    #d.text((2, height/2), fulltext, fill=colorText, font=font)
    d.text((0, 0), fulltext, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    #size = 500,500
    #img.thumbnail(size,Image.ANTIALIAS)
    img.save("abstract.png")
