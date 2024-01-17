from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, vfx
import os
import re
import glob
import argparse
import datetime

clips = []
totalTime = 0
streamers = []
name = ""
missingNames = []

# Ask arguments to define the video resolution and the export codec (if not encoding with nvdia)
parser = argparse.ArgumentParser()
parser.add_argument('--width', default=1920)
parser.add_argument('--height', default=1080)
parser.add_argument('--codec', default="mpeg4")
parser.add_argument('--requiredNameplates', default=0)
args = parser.parse_args()

# Convert args to int since it's the number of pixels
width = int(args.width)
height = int(args.height)
requiredNameplates = int(args.requiredNameplates)

codec = args.codec

for video in glob.glob("./videos/*.mp4"):
    match = re.search(';(.*);', video)
    if (match is not None):
        name = match.group(1)
    else:
        name = "Contact us"

    # Create video clip from file and apply resizing and FX
    returnedVideo = VideoFileClip(video, target_resolution=(height, width)).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)

    # Create the nameplate image from files with {name} as file name if the file exists
    if os.path.isfile("./nameplates/" + name + ".png"):
        image = ImageClip("./nameplates/" + name + ".png").set_duration(4).set_pos(("left","top"))
        image = image.crossfadein(1.0)
        image = image.crossfadeout(1.0)
        image = image.resize(0.5)
        returnedVideo = CompositeVideoClip([returnedVideo, image])
    else:
        # If nameplates are required, store missing names in an array
        if requiredNameplates:
            missingNames.append(name)

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
    codec=codec
)
for streamer in streamers:
    print(streamer)