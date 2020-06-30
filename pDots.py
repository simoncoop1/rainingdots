from curses import wrapper
import inspect
import locale
from random import randrange
import time
from time import sleep
import math
import argparse

locale.setlocale(locale.LC_ALL, '')

def main(stdscr):
    # Clear screen
    stdscr.clear()
    #stdscr.addstr(0, 0, 'this is a string {},{}'.format(stdscr.getmaxyx()[0],stdscr.getmaxyx()[1]))
    #stdscr.addstr(2, 0, u'\u2585'.encode('UTF-8'))

    ##choose column for dot
    ##2205m height
    ##time interval 30fps 0.03

    tupple1 = (0,randrange(stdscr.getmaxyx()[1]),0)
    dots = (tupple1,)
    timeac = 0
    now1=time.time()
    startt = now1
    interval=0.033
    acc = 9.8 #m/s^2
    whgt=2205

    while(True):
        time2=time.time()
        sleepm = interval-(time2-now1)
        #stdscr.addstr(0,0,'sleeping {}'.format(sleepm))
        sleep(sleepm)
        now1=time.time()

        for T in dots:
            T=((timeac-T[2])*(timeac-T[2])*acc,T[1],T[2])

        timeac=timeac+interval

        ##create new dot?
        if((int(timeac))%3 == 0):
            dots= dots + ((0,randrange(stdscr.getmaxyx()[1]),timeac),)

        stdscr.clear()
        
        for T in dots:           
            thex=stdscr.getmaxyx()[0]*(((timeac-T[2])*(timeac-T[2])*acc)/whgt)
            if(thex>stdscr.getmaxyx()[0]):
                thex=stdscr.getmaxyx()[0]-1

            try:
                stdscr.addstr(int(thex), T[1], u'\u2585'.encode('UTF-8'))
            except:
                print("caught it")

        stdscr.refresh()
        
    stdscr.getkey()

def effect(stdscr):
    # Clear screen
    stdscr.clear()

    timeac = 0
    now1=time.time()
    startt = now1
    interval=0.033


    startrect=(0,0)

    ##coords to draw
    points = [(0,0)]

    startrect=(0,0)
    
    while((startrect[0]<=(stdscr.getmaxyx()[0]/2)) & (startrect[1]<=(stdscr.getmaxyx()[1]/2))):
        
        points.append(startrect)
        while(points[-1][1]+1 < stdscr.getmaxyx()[1]-1-startrect[1]):
            points.append((points[-1][0],points[-1][1]+1))
        
        while(points[-1][0]+1 < stdscr.getmaxyx()[0]-startrect[0]):
            points.append((points[-1][0]+1,points[-1][1]))

        while(points[-1][1]-1 >= startrect[1]):
            points.append((points[-1][0],points[-1][1]-1))

        while(points[-1][0]-1 > startrect[0]):
            points.append((points[-1][0]-1,points[-1][1]))

        startrect=(startrect[0]+1,startrect[1]+1)             

    pointsC = 0

    #raise NameError(str(points) + str(pointsC))
    
    while(True):
        time2=time.time()
        sleepm = interval-(time2-now1)
        #stdscr.addstr(0,0,'sleeping {}'.format(sleepm))
        sleep(sleepm)
        now1=time.time()

        timeac=timeac+interval

        stdscr.clear()

        stdscr.addstr(points[pointsC][0], points[pointsC][1], u'\u2585'.encode('UTF-8'))
        #stdscr.addstr(0, 20, u'\u2585'.encode('UTF-8'))
        pointsC+=1
        if(len(points)<=pointsC):
            pointsC=0

        stdscr.refresh()
        
    stdscr.getkey()

def bounce(stdscr):
    # Clear screen
    stdscr.clear()

    timeac = 0
    now1=time.time()
    startt = now1
    interval=0.033

    #workout the points to draw
    #want about 4 bounces
    # each bounce takes pi wich is 3.14, so terminal width 80 is a bounce 80/3.14 = 25.47, so a modifier on x of 4/25.47 = 0.16
    #we want a height 80% of terminal of 24 which is 19.2, so y value multiplier of 19.2
    #1 second should be about 5 x axis pixels, therefore time 5x converts time to x-axis value. x is in seconds
    points = []
    xval=0
    xvalmodifier =  0.16
    while xval < 80:

        toadd = math.sin(xval*xvalmodifier)*19.2
        #need to mirror in xaxis
        
        if toadd < 0:
            toadd = toadd*-1
    
        toadd = 23 - toadd

        points.append((xval,toadd))
        xval+=1
               
    pointsC = 0
    
    while(True):
        time2=time.time()
        sleepm = interval-(time2-now1)
        #stdscr.addstr(0,0,'sleeping {}'.format(sleepm))
        sleep(sleepm)
        now1=time.time()

        timeac=timeac+interval

        stdscr.clear()

        stdscr.addstr(int(points[pointsC][1]),int(points[pointsC][0]), u'\u2585'.encode('UTF-8'))

        pointsC+=1
        if(len(points)<=pointsC):
            pointsC=0

        stdscr.refresh()
        
    stdscr.getkey()
    

#parse arguments
parser = argparse.ArgumentParser(description='Rainging Dots effect in terminal')
parser.add_argument('--effect', dest='effect', action='store_true',
               help='should play option effect instead')
parser.add_argument('--bounce', dest='bounce', action='store_true',
               help='should play option effect instead')
args = parser.parse_args()
 
if(args.effect): 
    wrapper(effect)
elif(args.bounce):
    wrapper(bounce)
else:
    wrapper(main)
