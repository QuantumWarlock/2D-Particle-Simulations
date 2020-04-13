# -*- coding: utf-8 -*-
"""
Program: hard_circle
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
class HC:
    """
    HC: Hard Circle Class

    """
    # Class Variables
    numInstances = 0         # #         Number of instanciations of this class.
    dt           = 0.01      # seconds   Time-Step
    bcR          = 5.0       # meters    Radius of bounding circle.
    figW         = 8         # inches    Width of Figure (Plot)
    figH         = 8         # inches    Height of Figure (Plot)

    def __init__(self,x=0,y=0,vx=0,vy=0,r=0.1):
        """
        Hard Circle Constructor

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
        HC.numInstances += 1
        self.x  = x
        self.y  = y
        self.vx = vx
        self.vy = vy
        self.r  = r
        self.t  = 0.0
        v = m.hypot(vx,vy)
        if( v != 0 ):
            dt = r/(4.0*v)          # Time step control. Prevent circle centers
                                    # from crossing in a single time-step.
            HC.dt = min(HC.dt,dt)
        self.xC = m.sqrt(2)*m.hypot(x, y)/HC.bcR
        self.graphic = plt.Circle((x,y), radius=r, fill=False,
                                  color=colors(self.xC), linewidth=1)
    def __del__(self):
        """
        Hard Circle Destructor
        """
        HC.numInstances -= 1

    def move(self):
        """
        Move hard circle according to its velocity.
        """
        dt = HC.dt
        vx = self.vx
        vy = self.vy
        # X
        self.x += vx*dt
        # Y
        self.y += vy*dt
        # Collision with wall?
        self.__boundaries()
        # Time
        self.t += dt
        # Graphic
        # self.updateGraphic()

    def __boundaries(self):
        dt  = HC.dt
        x   = self.x
        y   = self.y
        vx  = self.vx
        vy  = self.vy
        r   = self.r
        bcR = HC.bcR
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

    def updateGraphic(self):
        """
        Update graphic after a move or collision.
        """
        self.graphic = plt.Circle((self.x,self.y), radius=self.r,
                                  color=colors(self.xC),
                                  fill=False, linewidth=1)
# END: HC
### END: CLASSES

### FUNCTIONS
## Collision Functions
def collision(balls):
    """
    Step 1: Detect collisions
        TODO: Algorithm Documentation ...
    Step 2: Handle collisions
        TODO: Algorithm Documentation ...

    Parameters
    ----------
    balls : Python list.
        List of HC instances.

    Returns
    -------
    None.

    """
    for i in np.arange(HC.numInstances-1):
        for j in np.arange(i+1,HC.numInstances):
            d   = balls[i].r + balls[j].r
            drx = balls[i].x - balls[j].x
            dry = balls[i].y - balls[j].y
            dr  = m.hypot(drx, dry)
            if( dr < d ):
                # COLLISION! Case #1: Penetration
                # Game Engine Style Collision Correction
                offset = (d - dr)/2.0
                dx = offset*drx/dr
                dy = offset*dry/dr
                xiNew = balls[i].x + dx
                yiNew = balls[i].y + dy
                xjNew = balls[j].x - dx
                yjNew = balls[j].y - dy
                drx = xiNew - xjNew
                dry = yiNew - yjNew
                dvx = balls[i].vx - balls[j].vx
                dvy = balls[i].vy - balls[j].vy
                fac = (dvx*drx + dvy*dry)/(d*d)
                delvx = fac*drx
                delvy = fac*dry
                balls[i].vx -= delvx
                balls[i].vy -= delvy
                balls[j].vx += delvx
                balls[j].vy += delvy
                balls[i].x = xiNew
                balls[i].y = yiNew
                balls[j].x = xjNew
                balls[j].y = yjNew
            elif( dr == d ):
                # COLLISTION! Case #2: Perfect
                # This is going to be a VERY rare event ...
                dvx = balls[i].vx - balls[j].vx
                dvy = balls[i].vy - balls[j].vy
                fac = (dvx*drx + dvy*dry)/(d*d)
                delvx = fac*drx
                delvy = fac*dry
                balls[i].vx -= delvx
                balls[i].vy -= delvy
                balls[j].vx += delvx
                balls[j].vy += delvy
## END: Collision Functions

## Animation Functions:
def init():
    patches = []
    boundaryCircle = plt.Circle((0,0), radius=HC.bcR,
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
    ax.set_title('Hard Circles in a Hard Circle')
    ax.axis('scaled')
    ax.set_xlim([-1.1*HC.bcR,1.1*HC.bcR])
    ax.set_ylim([-1.1*HC.bcR,1.1*HC.bcR])
    tText = ax.text(-HC.bcR+0.1, HC.bcR-0.1, 'Time = ')
    patches = []
    boundaryCircle = plt.Circle((0,0), radius=HC.bcR,
                                  color='black',
                                  fill=False, linewidth=1)
    patches.append(ax.add_patch(boundaryCircle))
    if( i > 0 ):
        # N time-steps per graphics update
        for j in np.arange(10):
            for hc in hcList:
                hc.move()
            collision(hcList)
        for hc in hcList:
                hc.updateGraphic()
    # Graphics update
    s = 'Time = %.2f s' % hcList[0].t
    tText.set_text(s)
    for hc in hcList:
        patches.append(ax.add_patch(hc.graphic))
    patches.append(tText)
    return patches
## END: Animation Functions
### END: FUNCTIONS


if __name__ == '__main__':
    numCircles = 20                       # Number of circles along an axis. Total number of
                                          # circles is numCircles**2
    sq2 = m.sqrt(2)
    dS = sq2*HC.bcR/(numCircles+1)
    rC = dS/6.0                           # Diameter of circle is 1/3 of initial circle spacing.
    hcList = []
    for i in np.arange(numCircles):
        for j in np.arange(numCircles):
            x = dS*(j+1) - HC.bcR/sq2
            y = dS*(i+1) - HC.bcR/sq2
            # NOTE: Time-step control will adjust based on the velocities, i.e. the
            #       larger the velocity the smaller the time-step.
            # NOTE: This simulation assumes non-relativistic velocities. If you want
            #       to REALLY crank-up the velocities please consider appropriate
            #       adjustments to the physics.
            vxR = random.uniform(-3,3)   # Want ghosts to move faster? Crank this up!
            vyR = random.uniform(-3,3)   # Want ghosts to move faster? Crank this up!
            hcList.append( HC(x,y,vxR,vyR,rC) )
    fig, ax = plt.subplots()
    fig.set_size_inches(HC.figW,HC.figH)
    ax.grid(b=True, which='major', color='lightgrey')
    # ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Ghost Circles')
    ax.axis('scaled')
    ax.set_xlim([-1.1*HC.bcR,1.1*HC.bcR])
    ax.set_ylim([-1.1*HC.bcR,1.1*HC.bcR])
    tText = ax.text(-HC.bcR+0.1, HC.bcR-0.1, 'Time = ')
    ani = animation.FuncAnimation(fig, animate, frames=101,
                                  interval=100, blit=True,
                                  init_func=init, repeat=False)
    # patches = []
    # boundaryCircle = plt.Circle((0,0), radius=HC.bcR,
    #                               color='black',
    #                               fill=False, linewidth=1)
    # patches.append(ax.add_patch(boundaryCircle))
    # for hc in hcList:
    #     patches.append(ax.add_patch(hc.graphic))
    # ***** Uncomment next two lines to write file to disk. *****
    pwriter = animation.PillowWriter(fps=10, metadata=dict(artist='Dr. Ryan Clement'))
    ani.save('../movies/hard_circle.gif',writer=pwriter)
    plt.show()

