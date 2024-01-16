from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, vfx
import re
import glob

clips = []
name = ""

for video in glob.glob("./videos/*.mp4"):
    match = re.search(';(.*);', video)
    if (match is not None):
        name = match.group(1)
    if name == "" or (match is None):
        name = "default"
    returnedVideo = VideoFileClip(video).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
    image = ImageClip("./nameplates/" + name + ".png").set_duration(3).set_pos(("right","top")).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
    returnedVideo = CompositeVideoClip([returnedVideo, image])
    clips.append(returnedVideo)
    print(video)

combined = concatenate_videoclips(clips)
length = len(glob.glob("./output/*"))
combined.write_videofile("./output/" + str(length) + ".mp4")