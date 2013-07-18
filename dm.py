import sys
import re
import time
import subprocess
import optparse
import math

class ConnectedMonitor():
    def __init__(self, display):
        self.name        = display[0]
        self.presolution = display[1]
        self.online      = display[2]
        if self.online:
            self.cresolution = display[3]
            self.rotation   = display[4]
            self.position   = display[5]

class DisplayTools():

    #class XRandrException(Exception):
        #pass

    def __init__(self):
        self.refresh()
        self.dirTable = {'right':'--right-of', 'left':'--left-of', 'below':'--below', 'above':'--above'}

    def refresh(self):
        ret = self.__getInfo()
        self.connected = [ ConnectedMonitor(x) for x in ret ]
        self.online = [ x for x in self.connected if x.online ]
        self.offline = [ x for x in self.connected if not x.online ]

    def __getInfo(self):
        # must support xrandr command
        cmd = "xrandr -q"
        outs, err = subprocess.Popen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True).communicate()
        if err:
            #raise self.XRandrException('Test Environment Error: we must support xrandr command!')
            raise 'Test Environment Error: we must support xrandr command!'

        ret = []
        mp = re.compile('''
                    (?P<name>^\S+?)             # name
                    \s
                    connected
                    \s
                    ((?P<cresolution>\d+x\d+)   # current resolution
                    \+
                    (?P<pos>\d+\+\d+))?         # position
                    \s??
                    (?P<rotate>\S+)?            # rotation
                    \s?
                    (?:\(.+?$)
                    \s+?
                    (?P<presolution>\d+x\d+)    # preferred resolution
                    \s+?
                    \S+?
                    (?:\s|\*?)
                    \+$
                    ''',
                    re.S | re.M | re.X)
        for m in mp.finditer(outs):
            if m.group('cresolution') == None:
                ret.append([m.group('name'), m.group('presolution'), False])
                continue
            position = m.group('pos').replace('+', ',')
            if m.group('rotate') != None:
                rotate = m.group('rotate')
                ret.append([m.group('name'), m.group('presolution'), True, m.group('cresolution'), rotate, position])
            else:
                ret.append([m.group('name'), m.group('presolution'), True, m.group('cresolution'), 'normal', position])
        return ret


    def listMonitorInfo(self):
        print '%-12s%-15s%-15s%-15s%-15s%-15s' % ('Name', 'preferred', 'online?', \
                                        'position', 'rotation', 'current')
        for x in self.connected:
            if x.online:
                info = '%-15s%-15s%-15s%-15s%-15s%-15s' % \
                        (x.name, x.presolution, 'YES', x.position, x.rotation, x.cresolution)
            else:
                info = '%-15s%-15s%-15s' % (x.name, x.presolution, 'NO')
            print info

    def listOnlineMonitors(self):
        for x in self.online:
            print x.name

    def listOfflineMonitors(self):
        if not len(self.offline):
            for x in self.offline:
                print x.name
        else:
            print 'all connected monitors are active'

    def toggleMonitor(self, name=None, off=False):
        if off:
            cmd = 'xrandr --output %s --off' % name
        else:
            cmd = 'xrandr --output %s --auto' % name
        subprocess.call(cmd, shell=True)
        time.sleep(5)


    def setlayout(self, opts):
        cmd = ''
        if opts.layout in ('cube', '2'):
            cmd = self.getCubeCmd(opts)
        else:
            cmd = self.getCmd(opts)
        print '*************'
        print 'cmd : --> \n%s' % cmd
        print '*************'
        err = subprocess.call(cmd, shell=True)
        time.sleep(10)
        if err:
            print 'error in execute cmd : %s' % cmd
            return False
        return True


    def __chunks(self, l, n):
        return [l[i:i+n] for i in xrange(0, len(l), n)]

    def getCubeCmd(self, opts):
        cubeRange = [x*x for x in xrange(2, 7)] # 4 ~ 36 monitors total,
        nconnected = len(self.connected)           # 2 ~ 6 per row and column
        if nconnected not in cubeRange:
            msg = '%s monitors are not support the cube layout ' % nconnected
            e = Exception(msg)
            raise e

        dlen = int(math.sqrt(nconnected))
        d2 = self.__chunks(self.connected, dlen)
        v1 = self.connected[::dlen]
        cmd = ''
        pre = ''
        for i, monitor in enumerate(v1):
            if i > 0:
                cmd += ' --output %s --mode %s --rotate %s %s %s ' % \
                        (monitor.name, opts.size, opts.rotation, '--below', pre.name)
            else:
                cmd = 'xrandr --noprimary --output %s --pos 0x0 --mode %s --rotate %s' % \
                        ( monitor.name, opts.size, opts.rotation)
            prev = monitor
            for j, m in enumerate(d2[i][1:]):
                cmd += ' --output %s --mode %s --rotate %s %s %s' % \
                        (m.name, opts.size, opts.rotation, '--right-of', prev.name)
                prev = m
            pre = monitor
        return cmd


    def getCmd(self, opts):

        cmd = ''
        if opts.layout in ('landscape', '0') and opts.direction not in ('right', 'left'):
            msg = '%s direction not supported in Landscape mode' % opts.direction
            e = Exception(msg)
            raise e
        elif opts.layout in ('Portrait', '1') and opts.direction not in ('below', 'above'):
            msg = '%s direction not supported in Portrait mode' % opts.direction
            e = Exception(msg)
            raise e

        if opts.number in (3, 4):   # only rectangle supported
            pre = ''
            direction = self.dirTable[opts.direction]
            for i, monitor in enumerate(self.online):
                if i > 0:
                    cmd += ' --output %s --mode %s --rotate %s %s %s ' % \
                            (monitor.name, opts.size, opts.lrotation[i], direction, pre.name)
                else:
                    cmd = 'xrandr --noprimary --output %s --pos 0x0 --mode %s --rotate %s' % \
                            ( monitor.name, opts.size, opts.lrotation[i])
                pre = monitor
        elif opts.number == 2:      # can have different resolution and rotation
            if len(self.online) != 2:
                msg = 'fatal error in this script'
                e = Exception(msg)
                raise e
            m0, m1 = self.online
            s0 = opts.lsize[0]
            s1 = opts.lsize[1]
            r0 = opts.lrotation[0]
            r1 = opts.lrotation[1]

            direction = self.dirTable[opts.direction]
            print direction
            if opts.primary == 0:
                cmd = 'xrandr --output %s --primary --mode %s --rotate %s ' % \
                    ( m0.name, s0, r0)
                cmd += ' --output %s --mode %s --rotate %s %s %s ' % \
                    ( m1.name, s1, r1, direction, m0.name)
            else:
                cmd = 'xrandr --output %s --mode %s --rotate %s ' % \
                    ( m0.name, s0, r0)
                cmd += ' --output %s --primary --mode %s --rotate %s %s %s ' % \
                    ( m1.name, s1, r1, direction, m0.name)
        return cmd


def getOptions():
    parser = optparse.OptionParser(version='1.0')
    parser.add_option('-l', '--list',
                      dest='listconnected',
                      action='store_true',
                      help='list all connected monitor informations',
                      default=False)
    parser.add_option('--List',
                      dest='listonline',
                      action='store_true',
                      help='list all online monitors',
                      default=False)
    parser.add_option('--LIST',
                      dest='listoffline',
                      action='store_true',
                      help='list all inactive monitors',
                      default=False)
    parser.add_option('-a', '--all',
                      dest='activeall',
                      action='store_true',
                      default=False)
    parser.add_option('-p', '--primary',
                      dest='primary',
                      type=int,
                      help='primary monitor index, default is the first',
                      default=0)
    parser.add_option('--off',
                      action='append',
                      help='de-active online monitor',
                      default=[],
                      dest='offlist')
    parser.add_option('-n', '--number',
                      dest='number',
                      type=int,
                      help='active monitor number ...',
                      action='store')
    parser.add_option('-o', '--rotation',
                      dest='rotation',
                      help='0 : normal, do not rotate,\
                            1 : right , counter clockwise 90 degree,\
                            2 : inverted , counter clockwise 180 degree,\
                            3 : left, counter clockwise 270 degree',
                      default='0')
    parser.add_option('-s', '--size',
                      dest='size',
                      help='supported resolution like 1920x1200, 1024x768 ...',
                      default='best',
                      action='store')
    parser.add_option('-d', '--direction',
                      dest='direction',
                      help='0 : right , next monitor connected to the right of the previous one ,\
                            1 : below , next monitor connect below of the previous one,\
                            2 : left , next monitor connect to the left of the previous one,\
                            3 : top , next monitor connect on top of the previous one',
                      default='0')
    parser.add_option('--layout',
                      dest='layout',
                      type='choice',
                      choices=['0', 'landscape', '1', 'portrait', '2', 'cube'],
                      help='0 or landscape: 2x1, 3x1, 4x1 ...\
                            1 or portrait : 1x2, 1x3, 1x4 ...\
                            2 or cube : 2x2, 3x3 ...',
                      default='landscape'),
    opts, args = parser.parse_args()
    return (opts, args)

def main():
    opts, args = getOptions()
    dm = DisplayTools()

    # main logic
    if opts.listconnected:
        dm.listMonitorInfo()
        return
    if opts.listonline:
        dm.listOnlineMonitors()
        return
    if opts.listoffline:
        dm.listOfflineMonitors()
        return
    if opts.activeall:
        dm.toggleMonitor(off=False)
        return
    if len(opts.offlist):
        dm.toggleMonitor(opts.listoffline, off=True)
        return

    print 'begin toggling ....'
    # make sure we have the right number of active monitor
    ntotal = len(dm.connected)
    nonline = len(dm.online)
    if opts.number and opts.number != nonline:  # from command line
        if opts.number > ntotal:
            msg = 'you have connected %s monitors totally, but ask for %s ' \
                    % (ntotal, opts.number)
            e = Exception(msg)
            raise e
        diff = []
        if nonline < opts.number:
            diff = dm.offline[:opts.number - nonline]
            map((lambda t: dm.toggleMonitor(t.name, off=False)), diff)
        elif nonline > opts.number:
            diff = dm.online[opts.number - nonline :]
            map((lambda t: dm.toggleMonitor(t.name, off=True)), diff)
        else:
            pass
        # refresh all informations after change
        dm.refresh()
    else:
        opts.number = nonline


    print 'begin handling size and rotation ....'
    # same resolutions and rotations for 3 or 4 monitors
    # can have different resolutions and rotations for 2 monitors
    if opts.size == 'best':
        if opts.number in (3, 4):
            opts.size = min([x.presolution for x in dm.online])
        elif opts.number == 2:
            opts.lsize = [x.presolution for x in dm.online]
    else:
        opts.lsize = re.split(',', opts.size)
        opts.size = opts.lsize[0]
        if opts.number == 2 and len(opts.lsize) == 1:
            opts.lsize.append(dm.online[1].presolution)

    str4 = [str(i) for i in xrange(4)]
    rotateTable = {'0':'normal', '1':'right', '2':'inverted', '3':'left'}
    if ',' in opts.rotation :
        opts.lrotation = re.split(',', opts.rotation)
    else:
        opts.lrotation = [opts.rotation]
    opts.lrotation = [rotateTable[x] for x in opts.lrotation]
    # use default rotation if not specified
    if len(opts.lrotation) < opts.number:
        diff = dm.online[len(opts.lrotation) - opts.number:]
        for m in diff:
            opts.lrotation.append(m.rotation)

    opts.rotation = opts.lrotation[0]

    directionTable = {'0':'right', '1':'below', '2':'left', '3':'above'}
    if opts.direction in str4:
        opts.direction = directionTable[opts.direction]
    else:
        print 'invalid direction for layout, 0,1,2,3 are valid value'
        sys.exit(-1)

    print 'begin configuration ....'
    dm.setlayout(opts)

if __name__ == '__main__':
    main()

