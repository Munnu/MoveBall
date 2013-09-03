#-------------------------------------------------------------------------------
# Name:        moveball 2
# Purpose:     This was an old homework assignment from 2010. I redone it in the
#               Past few days for fun. There was a lab that accompanied (was
#               similar to) the homework. There is a little glitch
#               if the balls overlap each other whether in the initial drawing
#               or due to dx, dy increments.
#
#               The program loads some balls of varying colors.
#               The program waits for the user to click to start, the balls
#               bounce off the edge of the screen, each other, and a black box.
#               There are 4 boxes on the screen loaded at random positions.
#               Three of them stop the ball's movement if the ball is inside
#               of the bounds of the box. The last one (black box) acts as
#               an obstacle. The program ends at the end of loop or if all balls
#               are in a white box.
#
# Author:      Munnu/Monique Blake
#
# Created:     27/08/2013
# Copyright:   (c) Munnu 2013
# Licence:     None
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from graphics import *
from math import *
import random

W = 300
H = 300
ballList = []
squareList = []

#----------------------------------------------------------------
def simul(win, ballList):
    for step in range( 200 ):
        for i in range(len(ballList)):
            c, dx, dy = ballList[i]
            x = c.getCenter().getX()
            y = c.getCenter().getY()
            r = c.getRadius()

            if (x  <= 0 + r ) or (x >= W - r):
                dx = -dx
            if (y <= 0 + r) or(y >= H - r):
                dy = -dy

            # stop the ball's movement
            if isInSquare(x, y, r):
                dx = 0
                dy = 0

            # make it bounce off the black box's bounds
            if hitBlackBox(x, y, r):
                dx = -dx
                dy = -dy

            (boolVal, ball1, ball2) = hasCollided(ballList) # create a tuple
            if boolVal == True:
                # change the dx and dy of each ball that satisfies condition
                # then reverse the dx, dy of collided balls
                c1, dx1, dy1 = ball1
                c2, dx2, dy2 = ball2

                # replace old ballList values with current ballList values
                for list in ballList:
                    if ball1[0] in list:
                        list.pop(1)
                        list.insert(1, dx1)
                        list.pop(2)
                        list.insert(2, dy1)
                    if ball2[0] in list:
                        list.pop(1)
                        list.insert(1, dx2)
                        list.pop(2)
                        list.insert(2, dy2)
                c1.move(dx1, dy1)
                c2.move(dx2, dy2)

            else:
                c.move(dx, dy)
                ballList[ i ] = [ c, dx, dy ] # update ball values

            if allInBoxes(ballList):
                end(win)

def allInBoxes(ballList):
    counter = 0
    for i in range(len(ballList)):
        c, dx, dy = ballList[i]
        if (dy == dx == 0):
            counter += 1
    if counter == len(ballList):
        return True
    return False

def hasCollided(ballList):
    newBallList = []
    for i in range(len(ballList)-1):
        for j in range(i+1, len(ballList)):
            c1 = ballList[i][0]
            c2 = ballList[j][0]
            # get the dx1-2, dy1-2 vals
            dx1 = ballList[i][1]
            dy1 = ballList[i][2]
            dx2 = ballList[j][1]
            dy2 = ballList[j][2]
            # get radius of i and j balls
            r1 = c1.getRadius()
            r2 = c2.getRadius()
            # now get the points
            P1 = Point(c1.getCenter().getX(), c1.getCenter().getY())
            P2 = Point(c2.getCenter().getX(), c2.getCenter().getY())
            #print "(", P1.getX(), ",",P1.getY(),")", "(" , P2.getX() , ",",P2.getY(),")", "This is P1, P2"
            dist = distance(P1, P2)
            if (dist <= (r1 + r2)):
                if isSameSign(dx1, dx2): # push away one ball if sign's same
                    dx1 = -dx1
                elif isSameSign(dy1, dy2):
                    dy1 = -dy1
                else: # assume opposing sign, intend to push away each ball
                    dx1 = -dx1
                    dy1 = -dy1
                    dx2 = -dx2
                    dy2 = -dy2
                while (dist <= (r1 + r2)):
                    c1.move(dx1, dy1)
                    c2.move(dx2, dy2)
                    P1 = Point(c1.getCenter().getX(), c1.getCenter().getY())
                    P2 = Point(c2.getCenter().getX(), c2.getCenter().getY())
                    dist = distance(P1, P2) # call again, get updated points

                newBallList.append([c1, dx1, dy1])
                newBallList.append([c2, dx2, dy2])
                return True, newBallList[0], newBallList[1]
    return False, 0, 0

def distance(P1, P2):
    return sqrt( pow( P1.getX() - P2.getX(), 2 ) + pow( P1.getY() - P2.getY(), 2 ))

def isSameSign(a, b):
    # check if both signs are same
    if ((a < 0) and (b < 0)) or ((a > 0) and (b > 0)):
        return True

# Complete but incomplete concept (not implemented):
# This function is to assist the while loop in the collision check
# to ensure the balls don't knock each other out of the screen.
# I was going to integrate this in the while loop above and
# find the ball that is not closest to the bounds and push
# that one in the opposite direction, then bounce the other one.
# I've been working on this program for a few days, I think it's better
# to do something else now, so I'll leave this incomplete.
def isInBounds(c1, c2):
    boundsList = []
    boundsList.append(c1)
    boundsList.append(c2)
    for i in range(len(boundsList)):
        r = boundsList[i].getRadius()
        x = boundsList[i].getCenter().getX()
        y = boundsList[i].getCenter().getY()
        if ((x  <= 0 + r ) or (x >= W - r)) or ((y <= 0 + r) or(y >= H - r)):
            return False
        return True

def isInSquare(x, y, r):
    for i in range(len(squareList)-1): # exclude black box
        sP1 = squareList[i].getP1() # (bOriginX, bOriginY)
        sP2 = squareList[i].getP2() # (bW, bH)

        if (sP2.getX() - r >= x >= sP1.getX() + r) and (sP2.getY() - r >= y >= sP1.getY() + r):
            return True

# Another complete but incomplete concept.
# I was going to do make the code push out
# any balls that are already inside/go inside the black box.
# It's pretty much like the while loop, but I think it's better
# to move on. On to another project!
def hitBlackBox(x, y, r):
    # get last box
    blackBox = squareList[-1]
    sP1 = blackBox.getP1() # (bOriginX, bOriginY) | square P1
    sP2 = blackBox.getP2() # (bW, bH) | square P2
    if (sP2.getX() + r >= x >= sP1.getX() - r) and (sP2.getY() + r >= y  >= sP1.getY() - r):
        return True

def drawSquare(win):
    for i in range(4): # create 3 white boxes with random coords
        bOriginX = random.randrange(0, W-50, 51)
        bOriginY = random.randrange(0, H-100, 51)
        bW = bOriginX + 50 # you have to include origin + width therefore 100-50 = 50 sBoxW
        bH = bOriginY + 50
        square = Rectangle(Point(bOriginX, bOriginY), Point(bW, bH))
        square.draw(win)
        square.setFill("white")
        squareList.append(square)
    squareList[-1].setFill("black") # Fill last square drawn with black

# this commented portion can work too, remove the previous line, set loop range(3)
##    blackSquare = Rectangle(Point(H-50,W-50), Point((W-50)+50, (H-50)+ 50))
##    blackSquare.draw(win)
##    blackSquare.setFill("black")
##    squareList.append(blackSquare)

# -------------------------------------------
def end(win):
    waitForClick( win, "Click to End" )
    win.close()


#----------------------------------------------------------------
def waitForClick( win, message ):
    """ waitForClick: stops the GUI and displays a message.
    Returns when the user clicks the window. The message is erased."""

    # wait for user to click mouse to start
    startMsg = Text( Point( win.getWidth()/2, win.getHeight()/2 ), message )
    startMsg.draw( win )    # display message
    win.getMouse()          # wait
    startMsg.undraw()       # erase

#----------------------------------------------------------------
def main():
    win = GraphWin( "moving ball", W, H )
    #--- define a ball position and velocity ---
    drawSquare(win)
    ballColor = ["red", "blue", "pink", "purple", "green"]
    for i in range(5):
        c = Circle( Point( random.randrange( 16, W-15, 20 ), random.randrange( H/3, 2*H/3, 20 ) ), 15 )
        c.setFill(ballColor[i%len(ballColor)])
        c.draw(win)
        ballList.append([c, 5 - random.randrange(10), 5 - random.randrange(10)])

    for i in range(len(ballList)): # loop: no ball should be 0 dx and 0 dy
        if ballList[i][1] == ballList[i][2] == 0:
            ballList[i][1] == 1

    waitForClick( win, "Click to Start" )

    simul(win, ballList)
    end(win)

main()