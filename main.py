from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, vfx
import imageGenerate
import os
import re
import glob
import argparse
import datetime

clips = []
streamers = []
missingNames = []
transitionsArray = []
totalTime = 0
name = ""

# Ask arguments to define the video resolution and the export codec
parser = argparse.ArgumentParser()
parser.add_argument('--width', default=1920)
parser.add_argument('--height', default=1080)
parser.add_argument('--codec', default="mpeg4")
parser.add_argument('--requiredNameplates', default=0)
parser.add_argument('--font', default="LifeCraft_Font.ttf")
parser.add_argument('--fontSize', default=150)
parser.add_argument('--posX', default=520)
parser.add_argument('--posY', default=185)
parser.add_argument('--red', default=225)
parser.add_argument('--green', default=201)
parser.add_argument('--blue', default=67)
parser.add_argument('--transitions', default=0)
args = parser.parse_args()

# Convert args to int since it's the number of pixels
width = int(args.width)
height = int(args.height)
requiredNameplates = int(args.requiredNameplates)
fontSize = int(args.fontSize)
posX = int(args.posX)
posY = int(args.posY)
red = int(args.red)
green = int(args.green)
blue = int(args.blue)
transitions = int(args.transitions)

codec = args.codec
font = args.font
missingName = False

if transitions:
    firstTransition = VideoFileClip("./transition/Black_TwirlPart2V2.mov", has_mask=True, target_resolution=(height, width))
    firstTransition = firstTransition.set_start(0)
    secondTransition = VideoFileClip("./transition/Black_TwirlPart1V2.mov", has_mask=True, target_resolution=(height, width))
    firstTransition = firstTransition.fx( vfx.speedx, 1.5) 
    secondTransition = secondTransition.fx( vfx.speedx, 1.5)



for video in glob.glob("./videos/*.mp4"):
    missingName = False
    match = re.search(';(.*);', video)
    if (match is not None):
        name = match.group(1)
    else:
        name = "Contact us"
        missingName = True

    # Create video clip from file and apply resizing and FX
    returnedVideo = VideoFileClip(video, target_resolution=(height, width)).fx(vfx.fadein, 0.3).fx(vfx.fadeout, 0.3)
    if transitions:
        secondTransition = secondTransition.set_start(returnedVideo.duration - secondTransition.duration)
        transitionsArray = [firstTransition, secondTransition]

    # Create the nameplate image from files with {name} as file name if nameplates are required
    if requiredNameplates:
        if not missingName:
            imageGenerate.generate_image("./templates/", ("./fonts/" + font), fontSize, name, [posX,posY], [red, green, blue])
            image = ImageClip("./nameplates/" + name + ".png").set_duration(5).set_pos(("left","top"))
            image = image.crossfadein(1.0)
            image = image.crossfadeout(1.0)
            image = image.resize(0.5)
            returnedVideo = CompositeVideoClip([returnedVideo, image] + transitionsArray)
        else:
            missingNames.append(video)
    else:
        returnedVideo = CompositeVideoClip([returnedVideo] + transitionsArray)
    # Generate the timecode description
    timeCode = str(datetime.timedelta(seconds=totalTime))
    # Get only the 0:00:00 part and not the milliseconds
    time, separator, ms = timeCode.partition('.')
    streamers.append(time + " - " + name)
    totalTime += returnedVideo.duration
    clips.append(returnedVideo)

# If missingNames array is not empty, print all missing names then exit program before rendering video
if missingNames:
    for name in missingNames:
        print("Missing : " + name + ".png")
    exit()

# Concatenate all the video clips together
combined = concatenate_videoclips(clips)
length = len(glob.glob("./output/*"))
combined.write_videofile(
    "./output/" + str(length) + ".mp4",
    codec=codec,
    bitrate="7000k"
)
for streamer in streamers:
    print(streamer)