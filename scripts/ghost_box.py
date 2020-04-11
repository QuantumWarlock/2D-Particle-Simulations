# -*- coding: utf-8 -*-
"""
Program: ghost_box
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
# colors = cm.get_cmap('gist_rainbow')
colors = cm.get_cmap('seismic')


### CLASSES
class GC:
    """
    GC: Ghost Circle Class

        NOTE: Circles don't interact with each other (Ghosts).
        NOTE: Circles do interact with the walls of the box (Ghosts are trapped
              by magic and stuff. They bounce of walls like Sir Isaac Newton
              told us they should).
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
        """
        Ghost Circle Constructor

        Parameters
        ----------
        x : DOUBLE, optional
            X-coordinate of circle center [m]. The default is 0.
        y : DOUBLE, optional
            Y-coordinate of circle center [m]. The default is 0.
        vx : DOUBLE, optional
            X-component of circle velocity [m/s].The default is 0.
        vy : DOUBLE, optional
            Y-component of circle velocity [m/s]. The default is 0.
        r : DOUBLE, optional
            Radius of circle [m]. The default is 0.1.

        Returns
        -------
        None.

        """
        GC.numInstances += 1
        self.x  = x
        self.xC = x/GC.boxR
        self.y  = y
        self.vx = vx
        self.vy = vy
        self.r  = r
        self.t  = 0.0
        v = m.hypot(vx,vy)
        dt = r/(2.0*v)          # Time step control. Prevent circle centers
                                # from crossing in a single time-step.
        GC.dt = min(GC.dt,dt)
        self.graphic = plt.Circle((x,y), radius=r, fill=False,
                                  color=colors(self.xC), linewidth=3)
    def __del__(self):
        """
        Ghost Circle Destructor
        """
        GC.numInstances -= 1

    def move(self):
        """
        Move ghost (circle) according to its velocity.
        """
        dt = GC.dt
        # X
        self.x += self.vx*dt
        # Y
        self.y += self.vy*dt
        # Collision with wall?
        self.__boundaries()
        # Time
        self.t += dt
        # Graphic
        self.__updateGraphic()

    def __boundaries(self):
        dt = GC.dt
        x  = self.x
        y  = self.y
        vx = self.vx
        vy = self.vy
        r  = self.r
        bD = GC.boxD
        bU = GC.boxU
        bL = GC.boxL
        bR = GC.boxR
        # Y
        if( y < bD+r ):
            tD = dt - abs( (bD - y)/vy )
            self.vy *= -1.0
            self.y = bD + vy*tD + r
        elif( y > bU-r ):
            tU = dt - abs( (bU - y)/vy )
            self.vy *= -1.0
            self.y = bU + vy*tU - r
        # X
        if( x < bL+r ):
            tL = dt - abs( (bL - x)/vx )
            self.vx *= -1.0
            self.x = bL + vx*tL + r
        elif( x > bR-r ):
            tR = dt - abs( (bR - x)/vx )
            self.vx *= -1.0
            self.x = bR + vx*tR - r

    def __updateGraphic(self):
        """
        Update graphic after a move.
        """
        self.graphic = plt.Circle((self.x,self.y), radius=self.r,
                                  color=colors(self.xC),
                                  fill=False, linewidth=3)
# END: GC
### END: CLASSES


### FUNCTIONS
# correctIC
def correctIC(gcList):
    """
    Look for overlapping circles after initial conditions/set-up
    as random number generator doesn't know any better (if random
    positions are chosen). IMPORTANT: As this check is only
    pair-wise it will not work for a large number of particles
    as multiple circles will simultaneously overlap.

    NOTE: Unused. Included for user who may wish to use a random
          initial distribution of circles (see limitations above).

    Parameters
    ----------
    gcList : GC
        Python list of GC instances.

    Returns
    -------
    None.

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

## Animation Functions:
def init():
    patches = []
    return patches

def animate(i):
    patches = []
    if( i > 0 ):
        # 10 time-steps per graphics update
        for j in np.arange(10):
            for gc in gcList:
                gc.move()
    # Graphics update
    s = 'Time = %.2f s' % gcList[0].t
    tText.set_text(s)
    for gc in gcList:
        patches.append(ax.add_patch(gc.graphic))
    patches.append(tText)
    return patches
## END: Animation Functions
### END: FUNCTIONS


if __name__ == '__main__':
    numCircles = 3                     # Number of circles along an axis. Total number of
                                       # circles is numCircles**2
    dW = GC.boxR/(numCircles+1)
    dH = GC.boxU/(numCircles+1)
    rC = m.hypot(dW, dH)/10.0          # Diameter of circle is 1/5 of initial circle spacing.
    gcList = []
    for i in np.arange(numCircles):
        for j in np.arange(numCircles):
            x = dW*(j+1)
            y = dH*(i+1)
            # NOTE: Time-step control will adjust based on the velocities, i.e. the
            #       larger the velocity the smaller the time-step.
            # NOTE: This simulation assumes non-relativistic velocities. If you want
            #       to REALLY crank-up the velocities please consider appropriate
            #       adjustments to the physics.
            vxR = random.uniform(-10,10)   # Want ghosts to move faster? Crank this up!
            vyR = random.uniform(-10,10)   # Want ghosts to move faster? Crank this up!
            gcList.append( GC(x,y,vxR,vyR,rC) )
    fig, ax = plt.subplots()
    fig.set_size_inches(GC.figW,GC.figH)
    ax.grid(b=True, which='major', color='lightgrey')
    # ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Ghost Circles')
    ax.axis('scaled')
    ax.set_xlim([GC.boxL,GC.boxR])
    ax.set_ylim([GC.boxD,GC.boxU])
    tText = ax.text(4, 9.5, 'Time = ')
    ani = animation.FuncAnimation(fig, animate, frames=101,
                                  interval=100, blit=True,
                                  init_func=init, repeat=False)
    plt.show()
