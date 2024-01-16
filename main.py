from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, vfx
import re
import glob

clips = []
name = ""

for video in glob.glob("./videos/*.mp4"):
    match = re.search(';(.*);', video)
    if (match is not None):
        name = match.group(1)
    else:
        name = "default"

    # Create video clip from file and apply resizing and FX
    returnedVideo = VideoFileClip(video, target_resolution=(1080, 1920)).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
    # Create the nameplate image from files with {name} as file name
    image = ImageClip("./nameplates/" + name + ".png").set_duration(3).set_pos(("left","top")).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
    image = image.resize(0.5)
    
    returnedVideo = CompositeVideoClip([returnedVideo, image])
    clips.append(returnedVideo)

# Concatenate all the video clips together
combined = concatenate_videoclips(clips)
length = len(glob.glob("./output/*"))
combined.write_videofile("./output/" + str(length) + ".mp4")