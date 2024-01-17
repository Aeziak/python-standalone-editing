# Python Standalone Editing

This is a tool to generate videos with name tags over it.

The hierarchy must looks like :	

- nameplates
  - xxxx.png
  - xxxx.png
  - ....
- output
- video
  - All the videos that you want to be in your clip as mp4 (may support other video types later)

- main.py

To execute the program you have to use :

```
python .\main.py --width 1080 --height 1920 --codec h264_nvenc --requiredNameplates 1
```

You can replace the parameters by your needs.

All the optional parameters are :

```
width # The width of the output video. Default value is 1920
height # The height of the output video. Default value is 1080
codec # Codec used to encode video. Default value is mpeg4
requiredNameplates # Does the program stops if nameplate image is missing (will output the missing name). Default value is 0
```

