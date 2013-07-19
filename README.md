dmpy
====

display manipulation tool use "xrandr" command wrapper in python

example:

List attached monitor information
list informations of all attached monitors
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         normal    1920x1200
HDMI-0         1920x1200   YES     1920,0      normal    1920x1200
DVI-0          1600x1200   NO
DVI-1          1920x1200   NO
python dm --List ==> only list online monitor name
python dm --LIST ==> only list off line monitor name
qe@v260:~/src/dmpy$ python dm.py --List
DisplayPort-1
HDMI-0
qe@v260:~/src/dmpy$ python dm.py --LIST
DVI-0
DVI-1
change to "Portrait"("1x2") layout, with the second below the first one
qe@v260:~/src/dmpy$ python dm.py --layout 1 -d 1
*************
cmd : -->
xrandr --output DisplayPort-1 --primary --mode 1920x1200 --rotate normal  --output HDMI-0 --mode 1920x1200 --rotate normal --below DisplayPort-1
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         normal    1920x1200
HDMI-0         1920x1200   YES     0,1200      normal    1920x1200
DVI-0          1600x1200   NO
DVI-1          1920x1200   NO
change the resolution of the 2 monitors as 1024x768 and 1600x1200, with the second monitor above the first one
qe@v260:~/src/dmpy$ python dm.py --layout 1 -d 3 -s 1024x768,1600x1200
*************
cmd : -->
xrandr --output DisplayPort-1 --primary --mode 1024x768 --rotate normal  --output HDMI-0 --mode 1600x1200 --rotate normal --above DisplayPort-1
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,1200      normal    1024x768
HDMI-0         1920x1200   YES     0,0         normal    1600x1200
DVI-0          1600x1200   NO
DVI-1          1920x1200   NO
change to default layout("2x1"), with the first monitor rotate to 90 degree, the second one rotate 270 degree
qe@v260:~/src/dmpy$ python dm.py -o 1,3
*************
cmd : -->
xrandr --output DisplayPort-1 --primary --mode 1920x1200 --rotate right  --output HDMI-0 --mode 1920x1200 --rotate left --right-of DisplayPort-1
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         right     1200x1920
HDMI-0         1920x1200   YES     1200,0      left      1200x1920
DVI-0          1600x1200   NO
DVI-1          1920x1200   NO
change the second monitor as primary, and both of the monitors rotate 180 degree and preferred resolutions
qe@v260:~/src/dmpy$ python dm.py -p 1 -o 2,2
*************
cmd : -->
xrandr --output DisplayPort-1 --mode 1920x1200 --rotate inverted  --output HDMI-0 --primary --mode 1920x1200 --rotate inverted --right-of DisplayPort-1
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         inverted  1920x1200
HDMI-0         1920x1200   YES     1920,0      inverted  1920x1200
DVI-0          1600x1200   NO
DVI-1          1920x1200   NO
make 3 monitors online and change to "1x3" mode, with same resolution -- maximum available of the 3
qe@v260:~/src/dmpy$ python dm.py --layout 1 -n 3 -d 1 -o 0,0,0
*************
cmd : -->
xrandr --noprimary --output DisplayPort-1 --pos 0x0 --mode 1600x1200 --rotate normal --output HDMI-0 --mode 1600x1200 --rotate normal --below DisplayPort-1  --output DVI-0 --mode 1600x1200 --rotate normal --below HDMI-0
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         normal    1600x1200
HDMI-0         1920x1200   YES     0,1200      normal    1600x1200
DVI-0          1600x1200   YES     0,2400      normal    1600x1200
DVI-1          1920x1200   NO
same as above, but change all of the three to 1024x768 and change the first as normal,
both of the second and third as rotate 90 degree
qe@v260:~/src/dmpy$ python dm.py --layout 1 -n 3 -d 1 -o 0,0,0 -s 1024x768 -o 0,1,1
*************
cmd : -->
xrandr --noprimary --output DisplayPort-1 --pos 0x0 --mode 1024x768 --rotate normal --output HDMI-0 --mode 1024x768 --rotate right --below DisplayPort-1  --output DVI-0 --mode 1024x768 --rotate right --below HDMI-0
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         normal    1024x768
HDMI-0         1920x1200   YES     0,768       right     768x1024
DVI-0          1600x1200   YES     0,1792      right     768x1024
DVI-1          1920x1200   NO
cube or "2x2" layout, no rotation(normal), with same resolution -- maximum available of the 4
qe@v260:~/src/dmpy$ python dm.py --layout 2 -n 4
*************
cmd : -->
xrandr --noprimary --output DisplayPort-1 --pos 0x0 --mode 1600x1200 --rotate normal --output HDMI-0 --mode 1600x1200 --rotate normal --right-of DisplayPort-1 --output DVI-0 --mode 1600x1200 --rotate normal --below DisplayPort-1  --output DVI-1 --mode 1600x1200 --rotate normal --right-of DVI-0
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         normal    1600x1200
HDMI-0         1920x1200   YES     1600,0      normal    1600x1200
DVI-0          1600x1200   YES     0,1200      normal    1600x1200
DVI-1          1920x1200   YES     1600,1200   normal    1600x1200
same as above, but rotate 180 degree
qe@v260:~/src/dmpy$ python dm.py --layout 2 -n 4 -o 2
*************
cmd : -->
xrandr --noprimary --output DisplayPort-1 --pos 0x0 --mode 1600x1200 --rotate inverted --output HDMI-0 --mode 1600x1200 --rotate inverted --right-of DisplayPort-1 --output DVI-0 --mode 1600x1200 --rotate inverted --below DisplayPort-1  --output DVI-1 --mode 1600x1200 --rotate inverted --right-of DVI-0
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         inverted  1600x1200
HDMI-0         1920x1200   YES     1600,0      inverted  1600x1200
DVI-0          1600x1200   YES     0,1200      inverted  1600x1200
DVI-1          1920x1200   YES     1600,1200   inverted  1600x1200
once we have make 4 monitors online, we don't need to specify it in "-n 4", also default layout is "landscape" mode, such as "2x1,3x1,4x1", and we can have different rotation for each of the 4 in
landscape or portrait mode

qe@v260:~/src/dmpy$ python dm.py -o 0,1,2,3
*************
cmd : -->
xrandr --noprimary --output DisplayPort-1 --pos 0x0 --mode 1600x1200 --rotate normal --output HDMI-0 --mode 1600x1200 --rotate right --right-of DisplayPort-1  --output DVI-0 --mode 1600x1200 --rotate inverted --right-of HDMI-0  --output DVI-1 --mode 1600x1200 --rotate left --right-of DVI-0
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         normal    1600x1200
HDMI-0         1920x1200   YES     1600,0      right     1200x1600
DVI-0          1600x1200   YES     2800,0      inverted  1600x1200
DVI-1          1920x1200   YES     4400,0      left      1200x1600
qe@v260:~/src/dmpy$ python dm.py --layout 1 -o 3,1,2,0 -d 1
*************
cmd : -->
xrandr --noprimary --output DisplayPort-1 --pos 0x0 --mode 1600x1200 --rotate left --output HDMI-0 --mode 1600x1200 --rotate right --below DisplayPort-1  --output DVI-0 --mode 1600x1200 --rotate inverted --below HDMI-0  --output DVI-1 --mode 1600x1200 --rotate normal --below DVI-0
*************
qe@v260:~/src/dmpy$ python dm.py -l
Name           preferred   online? position    rotation  current
DisplayPort-1  1920x1200   YES     0,0         left      1200x1600
HDMI-0         1920x1200   YES     0,1600      right     1200x1600
DVI-0          1600x1200   YES     0,3200      inverted  1600x1200
DVI-1          1920x1200   YES     0,4400      normal    1600x1200
finally, its help message as following
qe@v260:~/src/dmpy$ python dm.py -h
Usage: dm.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -l, --list            list all connected monitor informations
  --List                list all online monitors
  --LIST                list all inactive monitors
  -a, --all
  -p PRIMARY, --primary=PRIMARY
                        primary monitor index, default is the first
  --off=OFFLIST         de-active online monitor
  -n NUMBER, --number=NUMBER
                        active monitor number ...
  -o ROTATION, --rotation=ROTATION
                        0 : normal, do not rotate,
                        1 : right , counter clockwise 90 degree,
                        2 : inverted , counter clockwise 180 degree,
                        3 : left, counter clockwise 270 degree
  -s SIZE, --size=SIZE  supported resolution like 1920x1200, 1024x768 ...
  -d DIRECTION, --direction=DIRECTION
                        0 : right , next monitor connected to the right of the
                        previous one ,                            1 : below ,
                        next monitor connect below of the previous one,
                        2 : left , next monitor connect to the left of the
                        previous one,                            3 : top ,
                        next monitor connect on top of the previous one
  --layout=LAYOUT       0 or landscape: 2x1, 3x1, 4x1 ...
                        1 or portrait : 1x2, 1x3, 1x4 ...
                        2 or cube : 2x2, 3x3 ...
