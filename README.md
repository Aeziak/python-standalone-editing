# Python Standalone Editing

This is a tool to generate videos with name tags over it.

The hierarchy must looks like :	

- nameplates
  - xxxx.png
  - xxxx.png
  - ....
- output
- font
- templates
  - template1.png
  - template2.png
  - ......
  - templateX.png

- transition
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
requiredNameplates # The program will generate nameplates based on the templates in the folder ./templates if set to 1
font # The font name (with its extension) you want to use for the text on the templates
fontSize # The font size you want
posX # The X axis position of the text on your template image
posY # The Y axis position of the text on your template image
red # The red color for the text (0 to 255)
green # The green color for the text (0 to 255)
blue # The blue color for the text (0 to 255)
transitions # If you want to use the transition in ./transition folder set it to 1, if 0 you will have fadein and fadeout
```

