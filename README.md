dmpy
====

display manipulation tool use "xrandr" command wrapper in python

example:

1, python dm.py -o 2 --layout 2 -d 1 -s 1024x768
--> 4 monitor in "2x2" mode, with resolution as 1024x768 each, and
    inverted rotations each

2, python dm.py -l, output as  following:
Name        preferred      online?        position       rotation       current
DisplayPort-1  1920x1200      YES            0,0            inverted       1024x768
HDMI-0         1920x1200      YES            1024,0         inverted       1024x768
DVI-0          1600x1200      YES            0,768          inverted       1024x768
DVI-1          1920x1200      YES            1024,768       inverted       1024x768
--> display monitor informations

3, python dm.py -n 2 --layout 0 -d 0
--> only active 2 monitors and use landscape(default) layout -- "1x2", with the
    second monitor right-of the first one, both of the 2 monitors use its preferred resolution

4, python dm.py -n 2 --layout 0 -d 0 -s 1920x1200,1600x1200
--> same as above, except with first monitor in 1920x1200 resolution and the second in 1600x1200

5, python dm.py -n 2 --layout 0 -d 0 -s 1024x768
--> now the first monitor in 1024x768 resolution and the second in preferred resolution

6, python dm.py  -o 1,3
--> now the first monitor rotate 90 degree while the second monitor rotate 270 degree

6, python dm.py  -n 3 -o 0,0,2
--> now we make 3 monitor active and make the third on right rotate 180 degree
