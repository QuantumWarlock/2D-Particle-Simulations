# -*- coding: utf-8 -*-
"""
Created: Apr 2020

@author: Ryan Clement (RRCC)
         scisoft@outlook.com
"""

### IMPORTS
import random
import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import AutoMinorLocator
from matplotlib import cm


### SET COLOR MAP
rainbow = cm.get_cmap('gist_rainbow')


### CLASSES
class GC:
    """
    GC: Ghost Circle Class
        Notes:
        1) Circles don't interact with each other (Ghosts).
        2) Circles do interact with the walls of the box (Ghosts are trapped
           and bounce of walls).
    """

    # Class Variables
    numInstances = 0         # #         Number of instanciations of this class.
    dt     = 0.01            # seconds   Time-Step
    boxU   = 10.0            # meters    Top of Box (Up)
    boxD   = 0.0             # meters    Bottom of Box (Down)
    boxL   = 0.0             # meters    Left Side of Box (Left)
    boxR   = 10.0            # meters    Right Side of Box (Right)
    # mass   = 1.0             # units    Future: Mass of Circle (Do ghosts have mass?)
    figW   = 8               # inches    Width of Figure (Plot)
    figH   = 8               # inches    Height of Figure (Plot)

    def __init__(self,x=0,y=0,vx=0,vy=0,r=0.1):
        """ Ghost Circle Constructor """
        GC.numInstances += 1
        self.x  = x
        self.y  = y
        self.vx = vx
        self.vy = vy
        self.r  = r
        self.t  = 0.0
        self.graphic = plt.Circle((x,y), radius=r,
                                  fill=False, color=rainbow(self.x/GC.boxR),
                                  linewidth=3)


    def move(self):
        """ Move particles """
        pass

    def __del__(self):
        """ Destructor """
        GC.numInstances -= 1

    def updateGraphic(self):
        """ Update graphic after a move. """
        self.graphic = plt.Circle((self.x,self.y), radius=self.r,
                                  fill=False, color=rainbow(self.x/GC.boxR),
                                  linewidth=3)
# END: GC
### END: CLASSES


### FUNCTIONS
# correctIC
def correctIC(gcList):
    """ Look for overlapping circles after initial conditions/set-up
        as random number generator doesn't know any better (if random
        positions are chosen). IMPORTANT: As this check is only
        pair-wise it will not work for a large number of particles
        as multiple circles will simultaneously overlap.
    """
    for i in np.arange(GC.numInstances-1):
        for j in np.arange(i+1,GC.numInstances):
            drx = gcList[i].x - gcList[j].x
            dry = gcList[i].y - gcList[j].y
            dr = m.hypot(drx,dry)
            d = gcList[i].r + gcList[j].r
            if( dr < d ):
                offset = (d - dr)/2.0
                dx = offset*drx/dr
                dy = offset*dry/dr
                gcList[i].x += dx
                gcList[i].y += dy
                gcList[j].x -= dx
                gcList[j].y -= dy
# END: correctIC
### END: FUNCTIONS


if __name__ == '__main__':
    numCircles = 10             # Number of circles along an axis. Total number of
                                # circles is numCircles**2
    dW = GC.boxR/(numCircles+1)
    dH = GC.boxU/(numCircles+1)
    rC = m.hypot(dW, dH)/10.0
    gcList = []
    for i in np.arange(numCircles):
        for j in np.arange(numCircles):
            x = dW*(j+1)
            y = dH*(i+1)
            vxR = random.uniform(-1,1)
            vyR = random.uniform(-1,1)
            gcList.append( GC(x,y,vxR,vyR,rC) )
    fig, ax = plt.subplots()
    fig.set_size_inches(GC.figW,GC.figH)
    ax.grid(b=True, which='major', color='lightgrey')
    #ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Ghost Circles')
    ax.axis('scaled')
    ax.set_xlim([GC.boxL,GC.boxR])
    ax.set_ylim([GC.boxD,GC.boxU])
    # correctIC(gcList)
    for gc in gcList:
        # gc.updateGraphic()
        ax.add_patch(gc.graphic)
    plt.show()
