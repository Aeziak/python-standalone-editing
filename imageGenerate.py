from PIL import Image, ImageFont, ImageDraw
import os, random

def generate_image(templatePath, fontPath, fontSize, streamerName, pos, rgb):
    
    my_image = Image.open(templatePath + random.choice(os.listdir(templatePath)))

    if len(streamerName) >= 11:
        fontSize = fontSize - 30
        pos[1] = pos[1] + 20

    font = ImageFont.truetype(fontPath, fontSize)

    image_editable = ImageDraw.Draw(my_image)

    image_editable.text((pos[0],pos[1]), streamerName, (rgb[0], rgb[1], rgb[2]), font=font)

    my_image.save("./nameplates/" + streamerName + ".png")
