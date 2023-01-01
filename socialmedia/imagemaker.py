
from PIL import Image, ImageDraw, ImageFont

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def main():

    fontname = "Arial.ttf"
    fontsize = 11   
    text = """
    Gross et al. (2015) have demonstrated that about a quarter of hits would typically be lost to keyword searchers if contemporary academic library catalogs dropped their controlled subject headings. This article re- ports on an investigation of the search value that subject descriptors and identifiers assigned by professional indexers add to a bibliographic database, namely the Australian Education Index (AEI). First, a similar methodology to that developed by Gross et al. (2015) was applied, with keyword searches representing a range of educational topics run on the AEI database with and without its subject indexing. The results indicated that AEI users would also lose, on average, about a quarter of hits per query. Second, an alternative research design was applied in which an experienced literature searcher was asked to find resources on a set of educational topics on an AEI database stripped of its subject indexing and then asked to search for additional resources on the same topics after the subject indexing had been reinserted. In this study, the proportion of additional resources that would have been lost had it not been for the subject indexing was again found to be about a quarter of the total resources found for each topic, on average.    
    """
    
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"

    #font = ImageFont.load_default().font
    #font = ImageFont.truetype(fontname, fontsize)
    font = ImageFont.truetype(font=None, size=fontsize, index=0, encoding='', layout_engine=None)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    
    img.save("test.png")
