#-------------------------------------------------------------------------------
# Name:        movingball
# Purpose:      Dominique's lab 8, the ball program I love so much...
#
# Author:      Munnu
#
# Created:     28/03/2013
# Copyright:   (c) Munnu 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from graphics import*
import random

W = 300
H = 300
sBoxOriginX = 50
sBoxOriginY = 50
sBoxW = 100 # you have to include origin + width therefore 100-50 = 50 sBoxW
sBoxH = 100

ballList = []
colorOfBall = []

#--------------------------------------------
def simul(ballList):
#    for ball in ballList:
#        r1 = ball.getRadius()

    #print "This is dx, dy", dx, dy # what is dx, is it the slope or the rate at which the ball moves?
        for step in range(2000):
            for i in range(len(ballList)):
                r1 = ballList[i][0].getRadius()
                x1 = ballList[i][0].getCenter().getX()
                y1 = ballList[i][0].getCenter().getY()

                if y1 < r1 or y1 > H-r1:
                    ballList[i][2] = -ballList[i][2]

                if x1 < r1 or x1 > W-r1:
                    ballList[i][1] = -ballList[i][1]

                # for pitstop
                # if (smallboxStartX + radius <= x <= smallboxWidth - radius)
                # and (smallboxStartY + radius <= y <= smallboxWHeight - radius)
                # dy = 0, dy = 0
                if (sBoxOriginX + r1 <= x1 <= sBoxW - r1) and \
                (sBoxOriginY + r1 <= y1 <= sBoxH - r1):
                    ballList[i][2] = 0
                    ballList[i][1] = 0

                ballList[i][0].move(ballList[i][1], ballList[i][2])

def drawSquare(win):
    square = Rectangle(Point(sBoxOriginX, sBoxOriginY), Point(sBoxW, sBoxH))
    square.draw(win)
    square.setFill("white")


#---------------------------------------------
def waitForClick(win, message):
    """ waitForClick: stops the GUI and displays a message.
    Returns when the user clicks the window. The message is erased."""

    # wait for user to click mouse to start
    startMsg = Text(Point(win.getWidth()/2, win.getHeight()/2), message)
    startMsg.draw(win)  # display message
    win.getMouse()      # wait
    startMsg.undraw()   # erase

#-----------------------------------------------
def main():
    win = GraphWin("moving ball", W, H)

    ballColor = ['azure', 'magenta', 'brown', 'coral', 'goldenrod']
    #--- define a ball position and velocity ---#
    ballAmount = int(raw_input("How many balls do you want?"))
    drawSquare(win)
    for i in range(ballAmount):
        #ballColor = raw_input("What color ball?") <= old, before array impl
        c = Circle(Point(W/2, H/2), 15)
        c.setFill(ballColor[i%5])
        c.draw(win)
        # randrange == the start pos speed of the balls (dx,dy), -3 alters the
        # start direction. If a ball's rand num is <= 0, we get opposite sign dx
        ballList.append([c, 5 - random.randrange(10), 5 - random.randrange(10)])


    waitForClick(win, "Click to Start")
    simul(ballList)
#    simul(ballList, 3-random.randrange(6), 3-random.randrange(6)) #ask

    waitForClick(win, "Click to End")
    win.close()

main()