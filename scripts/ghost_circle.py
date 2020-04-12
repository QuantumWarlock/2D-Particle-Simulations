# -*- coding: utf-8 -*-
"""
Program: ghost_circle
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
colors = cm.get_cmap('gist_rainbow')
# colors = cm.get_cmap('seismic')

### CLASSES
class GC:
    """
    GC: Ghost Circle Class

    """
    # Class Variables
    numInstances = 0         # #         Number of instanciations of this class.
    dt           = 0.01      # seconds   Time-Step
    bcR          = 5.0       # meters    Radius of bounding circle.
    # mass       = 1.0       # units    Future: Mass of Circle (Do ghosts have mass?)
    figW         = 8         # inches    Width of Figure (Plot)
    figH         = 8         # inches    Height of Figure (Plot)

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
        self.y  = y
        self.vx = vx
        self.vy = vy
        self.r  = r
        self.t  = 0.0
        v = m.hypot(vx,vy)
        dt = r/(2.0*v)          # Time step control. Prevent circle centers
                                # from crossing in a single time-step.
        GC.dt = min(GC.dt,dt)
        self.xC = m.sqrt(2)*m.hypot(x, y)/GC.bcR
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
        dt  = GC.dt
        x   = self.x
        y   = self.y
        vx  = self.vx
        vy  = self.vy
        r   = self.r
        bcR = GC.bcR
        d   = m.hypot(x, y)   # Distance of particle center from origin of boundary circle.
        # R
        if( d+r > bcR ):
            # Mid-point approximation to true circle crossing. This method could be iterated
            # to a given tolerance. The time-step control should work well with this
            # approximation. If larger time-steps are used a few iterations may be needed.
            xm = x - vx*dt/2.0
            ym = y - vy*dt/2.0
            rm = m.hypot(xm, ym)
            frac = bcR/rm
            xc = frac*xm
            yc = frac*ym
            # rc = m.hypot(xc, yc)
            # rcx = xc/rc
            # rcy = yc/rc
            rux = xm/rm   # X-component of unit vector
            ruy = ym/rm   # Y-component of unit vector
            vc = vx*rux + vy*ruy
            vcx = vc*rux
            vcy = vc*ruy
            self.vx -= 2.0*vcx
            self.vy -= 2.0*vcy
            self.x = xc - r*rux
            self.y = yc - r*ruy

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
    boundaryCircle = plt.Circle((0,0), radius=GC.bcR,
                                  color='black',
                                  fill=False, linewidth=1)
    patches.append(ax.add_patch(boundaryCircle))
    return patches

def animate(i):
    ax.clear()
    ax.grid(b=True, which='major', color='lightgrey')
    # ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Ghost Circles')
    ax.axis('scaled')
    ax.set_xlim([-1.1*GC.bcR,1.1*GC.bcR])
    ax.set_ylim([-1.1*GC.bcR,1.1*GC.bcR])
    tText = ax.text(-GC.bcR+0.1, GC.bcR-0.1, 'Time = ')
    patches = []
    boundaryCircle = plt.Circle((0,0), radius=GC.bcR,
                                  color='black',
                                  fill=False, linewidth=1)
    patches.append(ax.add_patch(boundaryCircle))
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
    numCircles = 10                        # Number of circles along an axis. Total number of
                                          # circles is numCircles**2
    sq2 = m.sqrt(2)
    dS = sq2*GC.bcR/(numCircles+1)
    rC = dS/6.0                          # Diameter of circle is 1/3 of initial circle spacing.
    gcList = []
    for i in np.arange(numCircles):
        for j in np.arange(numCircles):
            x = dS*(j+1) - GC.bcR/sq2
            y = dS*(i+1) - GC.bcR/sq2
            # NOTE: Time-step control will adjust based on the velocities, i.e. the
            #       larger the velocity the smaller the time-step.
            # NOTE: This simulation assumes non-relativistic velocities. If you want
            #       to REALLY crank-up the velocities please consider appropriate
            #       adjustments to the physics.
            vxR = random.uniform(-3,3)   # Want ghosts to move faster? Crank this up!
            vyR = random.uniform(-3,3)   # Want ghosts to move faster? Crank this up!
            gcList.append( GC(x,y,vxR,vyR,rC) )
    fig, ax = plt.subplots()
    fig.set_size_inches(GC.figW,GC.figH)
    ax.grid(b=True, which='major', color='lightgrey')
    # ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Ghost Circles')
    ax.axis('scaled')
    ax.set_xlim([-1.1*GC.bcR,1.1*GC.bcR])
    ax.set_ylim([-1.1*GC.bcR,1.1*GC.bcR])
    tText = ax.text(-GC.bcR+0.1, GC.bcR-0.1, 'Time = ')
    ani = animation.FuncAnimation(fig, animate, frames=101,
                                  interval=60, blit=True,
                                  init_func=init, repeat=False)
    # patches = []
    # boundaryCircle = plt.Circle((0,0), radius=GC.bcR,
    #                               color='black',
    #                               fill=False, linewidth=1)
    # patches.append(ax.add_patch(boundaryCircle))
    # for gc in gcList:
    #     patches.append(ax.add_patch(gc.graphic))
    # Uncomment next two lines to write file to disk.
    # pwriter = animation.PillowWriter(fps=10, metadata=dict(artist='Dr. Ryan Clement'))
    # ani.save('../movies/ghost_circle.gif',writer=pwriter)
    plt.show()
