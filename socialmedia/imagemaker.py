
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
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
    dedented_text = textwrap.dedent(text=text)
    return(wrapper.fill(text=dedented_text))

def add_watermark(img, watermark_path='lf_logo.png', scale = 1.1, opacity=.8, brightness=0.8):
    width, height = img.size
 
    #resize watermark file to 50% of base file
    watermark = Image.open(watermark_path)
    if watermark.mode != 'RGBA':
        watermark.convert('RGBA')
    watermark.thumbnail((width*scale, height*scale))
    
    #make watermark transparent and b/w
    alpha_channel = watermark.split()[3]
    alpha_channel = ImageEnhance.Brightness(alpha_channel).enhance(opacity)
    watermark = ImageEnhance.Brightness(watermark).enhance(brightness)
    watermark = ImageEnhance.Contrast(watermark).enhance(1.9)
    watermark.putalpha(alpha_channel)
    
    #position watermark
    water_width, water_height = watermark.size
    watermark_position = (int((width - water_width)/2) , int((height - water_height)/2))
    
    merge_img = Image.new('RGBA', (width, height), (0,0,0,0))
    merge_img.paste(img, (0,0))
    
    merge_img.paste(watermark, watermark_position, mask=watermark)
    return(merge_img)
    
def main(title="Not available", abstract=None, author="Not available", year="Not available"):

    fontname = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" #or -Bold.ttf  
    fontsize = 11 
    
    if not abstract:
        abstract = "Not available"
    
    fulltext = (f"First author: {author}      Year: {year}\n Title: {format_text(text=title)}\n\n {format_text(text=abstract)}")
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"


    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(fulltext, font)
    img = Image.new('RGBA', (width+4, height+4), colorBackground)
    img = add_watermark(img)
    d = ImageDraw.Draw(img)
    #d.text((2, height/2), fulltext, fill=colorText, font=font)
    d.text((0, 0), fulltext, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)

    img.save("abstract.png")
