# -*- coding: utf-8 -*-
"""
Program: hard_gravity_box
Created: Apr 2020
@author: Ryan Clement (RRCC)
         scisoft@outlook.com
"""

### IMPORTS
# import random
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
class HB:
    """
    HB: Hard Box Class

        * Circles interact with each other via elastic collisions, i.e.
              2D version of hard sphere scattering.
        * Circles interact with the walls of the box.
    """
    # Class Variables
    numInstances = 0         # #         Number of instanciations of this class.
    dt     = 0.01            # seconds   Time-Step
    ay     = -9.81           # m/s**2    Acceleration due to gravity
    boxU   = 10.0            # meters    Top of Box (Up)
    boxD   = 0.0             # meters    Bottom of Box (Down)
    boxL   = 0.0             # meters    Left Side of Box (Left)
    boxR   = 10.0            # meters    Right Side of Box (Right)
    # mass   = 1.0             # units    Future: Mass of Circle (Do ghosts have mass?)
    figW   = 8               # inches    Width of Figure (Plot)
    figH   = 8               # inches    Height of Figure (Plot)

    def __init__(self,x=0,y=0,vx=0,vy=0,r=0.1):
        """
        Hard Box Constructor

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
        HB.numInstances += 1
        self.x  = x
        self.xC = x/HB.boxR
        self.y  = y
        self.vx = vx
        self.vy = vy
        self.r  = r
        self.t  = 0.0
        v = m.hypot(vx,vy)
        if( v != 0 ):
            dt = r/(4.0*v)
            # dt = r/(2.0*v)          # Time step control. Prevent circle centers
            #                         # from crossing in a single time-step.
            HB.dt = min(HB.dt,dt)
        self.graphic = plt.Circle((x,y), radius=r, fill=False,
                                  color=colors(self.xC), linewidth=1)
    def __del__(self):
        """
        Hard Box Destructor
        """
        HB.numInstances -= 1

    def move(self):
        """
        Move circle according to its velocity and accleration using
        leapfrog integration (2nd Order).
        """
        dt = HB.dt
        vx = self.vx
        vy = self.vy
        ay = HB.ay
        # X
        self.x += vx*dt
        # Y
        self.y += vy*dt + ay*(dt*dt)/2.0
        self.vy += (ay + ay)*dt/2.0        # Left in leapfrog form for future
                                           # non-constant acceleration simulations.
        # Collision with wall?
        self.__boundaries()
        # Time
        self.t += dt
        # Graphic
        # self.updateGraphic()

    def __boundaries(self):
        # dt = HB.dt
        x  = self.x
        y  = self.y
        # vx = self.vx
        # vy = self.vy
        r  = self.r
        bD = HB.boxD
        bU = HB.boxU
        bL = HB.boxL
        bR = HB.boxR
        # Y
        if( y < bD+r ):
            # tD = dt - abs( (bD - y)/vy )
            self.vy *= -1.0
            # self.y = bD + vy*tD + r
            self.y = bD + r
        elif( y > bU-r ):
            # tU = dt - abs( (bU - y)/vy )
            self.vy *= -1.0
            # self.y = bU + vy*tU - r
            self.y = bU - r
        # X
        if( x < bL+r ):
            # tL = dt - abs( (bL - x)/vx )
            self.vx *= -1.0
            # self.x = bL + vx*tL + r
            self.x = bL + r
        elif( x > bR-r ):
            # tR = dt - abs( (bR - x)/vx )
            self.vx *= -1.0
            # self.x = bR + vx*tR - r
            self.x = bR - r

    def updateGraphic(self):
        """
        Update graphic after a move.
        """
        self.graphic = plt.Circle((self.x,self.y), radius=self.r,
                                  color=colors(self.xC),
                                  fill=False, linewidth=1)
# END: GC
### END: CLASSES

### FUNCTIONS
## Collision Functions:
def collision(balls):
    """
    Step 1: Detect collisions
        TODO: Algorithm Documentation ...
    Step 2: Handle collisions
        TODO: Algorithm Documentation ...

    Parameters
    ----------
    balls : Python list.
        List of HB instances.

    Returns
    -------
    None.

    """
    for i in np.arange(HB.numInstances-1):
        for j in np.arange(i+1,HB.numInstances):
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
### END: Collision Functions

## Animation Functions:
def init():
    patches = []
    return patches

def animate(i):
    ax.clear()
    ax.grid(b=True, which='major', color='lightgrey')
    # ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Impenetrable Circles')
    ax.axis('scaled')
    ax.set_xlim([HB.boxL,HB.boxR])
    ax.set_ylim([HB.boxD,HB.boxU])
    tText = ax.text(4, 9.5, '')
    patches = []
    if( i > 0 ):
        # N time-steps per graphics update
        for j in np.arange(1):
            for hb in hbList:
                hb.move()
            collision(hbList)
        for hb in hbList:
                hb.updateGraphic()
    # Graphics update
    s = 'Time = %.2f s' % hbList[0].t
    tText.set_text(s)
    for hb in hbList:
        patches.append(ax.add_patch(hb.graphic))
    patches.append(tText)
    return patches
## END: Animation Functions
### END: FUNCTIONS


if __name__ == '__main__':
    numCircles = 10                     # Number of circles along an axis. Total number of
                                       # circles is numCircles**2
    dW = HB.boxR/(numCircles+1)
    dH = HB.boxU/(numCircles+1)
    rC = m.hypot(dW, dH)/6.0          # Diameter of circle is 1/3 of initial circle spacing.
    hbList = []
    for i in np.arange(numCircles):
        for j in np.arange(numCircles):
            x = dW*(j+1)
            y = dH*(i+1)
            # NOTE: Time-step control will adjust based on the velocities, i.e. the
            #       larger the velocity the smaller the time-step.
            # NOTE: This simulation assumes non-relativistic velocities. If you want
            #       to REALLY crank-up the velocities please consider appropriate
            #       adjustments to the physics.
            # vxR = random.uniform(-10,10)   # Want ghosts to move faster? Crank this up!
            # vyR = random.uniform(-10,10)   # Want ghosts to move faster? Crank this up!
            vxR = 0.0
            vyR = 0.0
            hbList.append( HB(x,y,vxR,vyR,rC) )
    fig, ax = plt.subplots()
    fig.set_size_inches(HB.figW,HB.figH)
    ax.grid(b=True, which='major', color='lightgrey')
    # ax.grid(b=True, which='minor', color='lightgrey')
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax.set_title('Impenetrable Circles')
    ax.axis('scaled')
    ax.set_xlim([HB.boxL,HB.boxR])
    ax.set_ylim([HB.boxD,HB.boxU])
    tText = ax.text(4, 9.5, 'Time = ')
    ani = animation.FuncAnimation(fig, animate, frames=201,
                                  interval=100, blit=True,
                                  init_func=init, repeat=False)

    # Uncomment next two lines to write file to disk.
    # pwriter = animation.PillowWriter(fps=10, metadata=dict(artist='Dr. Ryan Clement'))
    # ani.save('../movies/hard_gravity_box.gif',writer=pwriter)
    plt.show()