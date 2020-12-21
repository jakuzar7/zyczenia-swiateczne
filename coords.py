from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageShow
import csv


def makeFont(textFontPath='font/RoughRakoon.ttf', textSize=60):
    return ImageFont.truetype(textFontPath, size=textSize)


# stdFont = ImageFont.truetype(
#    'font/newStandardRegular/NewStandardRegular.otf', size=160)
# manualeFont = ImageFont.truetype(
#    'font/manuale/Manuale-Regular.ttf', size=60)
#rainbowFont = ImageFont.truetype('font/RainbowRegular.ttf', size=60)
rainbowFont = makeFont('font/RainbowRegular.ttf')


# box [x, y, w, h] left up corner XY, width, height
def addText(text, box, docImg, textFont, textColor=(0, 0, 0), textSpacing=24, downMarginPct=0.8):

    # drawing box
    textImg = Image.new('RGB', (box[2], box[3]), color=(255, 255, 255))
    ImgDrw = ImageDraw.Draw(textImg)
    # calculating text size
    TextSizeX, TextSizeY = ImgDrw.multiline_textsize(
        text, font=textFont, spacing=textSpacing)

    # adjust text size
    while True:
        if TextSizeX > box[2] or TextSizeY > box[3] * downMarginPct:
            # calculating new text size
            textFont = makeFont(textSize=int(textFont.size * .9))
            TextSizeX, TextSizeY = ImgDrw.multiline_textsize(
                text, font=textFont, spacing=textSpacing)
        else:
            textFont = makeFont(textSize=(textFont.size - 2))
            break

    # middle pos
    TextPosX = (box[2]-TextSizeX)/2
    # down border, with margin from below
    TextPosY = int((box[3]-TextSizeY - textFont.size/4) * downMarginPct)

    ImgDrw.text((TextPosX, TextPosY), text, fill=textColor,
                font=textFont, align='center', spacing=textSpacing)

    # paste box with text onto document
    docImg.paste(textImg, (box[0], box[1], box[0] + box[2], box[1]+box[3]))

    return docImg


#############
tekstMatma = 'Wesołych Świąt i dużo zdrówka!\n życzy IIIA'

tekstBox = Image.new('RGB', (1080, 540), color=(200, 200, 200))

tekstImg = addText(tekstMatma, [0, 0, 1080, 540],
                   tekstBox, rainbowFont, textColor=(0, 0, 0))

# tekstImg.show()

tekstImg.save('test.jpg')

finalImg = tekstImg.load()

# print(finalImg[1,0])


xCoords = []
yCoords = []
# searching through pixels
for x in range(0, 1080, 2):
    for y in range(0, 540, 2):
        if(finalImg[x, y] != (255, 255, 255)):
            xCoords.append(x - 720)
            yCoords.append(y - 3*540/4)
    pass

for i in range(len(xCoords)):
    xCoords[i] = str('{x:' + str(xCoords[i]))

for i in range(len(yCoords)):
    yCoords[i] = str('y:' + str(yCoords[i]) + '},')


# creating js files
for j in range(0, 12):
    fileName = str('coords/draw' + str(j) + '.js')
    f = open(fileName, 'w')
    f.write('var drawing' + str(j) + '= [')

    for i in range(int(j*len(xCoords)/12), int((j+1)/12 * len(xCoords))):
        f.write(xCoords[i] + ', ' + yCoords[i]+'\n')

    f.write('\n]')


'''
# creating CSV files
multipleFiles = True
    
if multipleFiles:
    for j in range(0, 12):
        fileName = str('coords/coordsCSVFile' + str(j) + '.csv')

        with open(fileName, mode='w') as fileName:
            coordsCSV = csv.writer(fileName, delimiter=',')
            for i in range(int(j*len(xCoords)/12), int((j+1)/12 * len(xCoords))):
                coordsCSV.writerow([xCoords[i], yCoords[i]])
else:
    fileName = str('coordsCSVFile.csv')
    with open(fileName, mode='w') as fileName:
        coordsCSV = csv.writer(fileName, delimiter=',')
        for i in range(len(xCoords)):
            coordsCSV.writerow([xCoords[i], yCoords[i]])
'''
