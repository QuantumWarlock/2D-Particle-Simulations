# -*- coding: utf-8 -*-
"""
Program: hard_diffmass_box
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
colorMap = cm.get_cmap('gist_rainbow')
# colorMap = cm.get_cmap('seismic')

### CLASSES
class HB:
    """
    HB: Hard Box Class with Mass

        * Circles interact with each other via elastic collisions, i.e.
              2D version of hard sphere scattering.
        * Circles interact with the walls of the box.
        * Circles have mass. The radius scales with mass and has the
          following relationship: m = r**2.
    """
    # Class Variables
    numInstances = 0         # #         Number of instanciations of this class.
    dt     = 0.01            # seconds   Time-Step
    boxU   = 10.0            # meters    Top of Box (Up)
    boxD   = 0.0             # meters    Bottom of Box (Down)
    boxL   = 0.0             # meters    Left Side of Box (Left)
    boxR   = 10.0            # meters    Right Side of Box (Right)
    figW   = 8               # inches    Width of Figure (Plot)
    figH   = 8               # inches    Height of Figure (Plot)

    def __init__(self,x=0,y=0,vx=0,vy=0,radius=0.1):
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
        radius : DOUBLE, optional
                Radius of circle [m]. The default is 0.1.

        Returns
        -------
        None.

        """
        HB.numInstances += 1
        self.r      = np.array([x,y])        # Position Vector
        self.v      = np.array([vx,vy])      # Velocity Vector
        self.a      = np.array([0,0])        # Acceleration Vector
        self.xC     = x/HB.boxR
        self.radius = radius
        self.mass   = radius**2
        self.t      = 0.0
        vH = m.hypot(vx,vy)
        if( vH != 0 ):
            dt = radius/(2.0*vH)             # Time step control. Prevent circle centers
                                             # from crossing in a single time-step.
            HB.dt = min(HB.dt,dt)
        self.graphic = plt.Circle((x,y), radius=radius, fill=False,
                                  color=colorMap(self.xC), linewidth=1)
    def __del__(self):
        """
        Hard Box Destructor
        """
        HB.numInstances -= 1

    @property
    def x(self):
        return self.r[0]
    @x.setter
    def x(self, value):
        self.r[0] = value
    @property
    def y(self):
        return self.r[1]
    @y.setter
    def y(self, value):
        self.r[1] = value
    @property
    def vx(self):
        return self.v[0]
    @vx.setter
    def vx(self, value):
        self.v[0] = value
    @property
    def vy(self):
        return self.v[1]
    @vy.setter
    def vy(self, value):
        self.v[1] = value
    @property
    def ax(self):
        return self.a[0]
    @ax.setter
    def ax(self, value):
        self.a[0] = value
    @property
    def ay(self):
        return self.a[1]
    @ay.setter
    def ay(self, value):
        self.a[1] = value

    def move(self):
        """
        Move circle according to its velocity.
        """
        dt = HB.dt
        self.r += self.v * dt
        # Collision with wall?
        self.__boundaries()
        # Time
        self.t += dt

    def __boundaries(self):
        """
        Particle interaction with boundary:

        Step 1: Check for particles that have crossed the
                boundaries.
        Step 2: If particle is at or past boundary reflect
                it.

        Returns
        -------
        None.

        """
        x = self.x
        y = self.y
        radius = self.radius
        bD = HB.boxD
        bU = HB.boxU
        bL = HB.boxL
        bR = HB.boxR
        # Y
        if( y < (bD + radius) ):
            self.vy *= -1.0
            self.y = bD + radius
        elif( y > (bU - radius) ):
            self.vy *= -1.0
            self.y = bU - radius
        # X
        if( x < (bL + radius) ):
            self.vx *= -1.0
            self.x = bL + radius
        elif( x > (bR - radius) ):
            self.vx *= -1.0
            self.x = bR - radius

    def updateGraphic(self):
        """
        Update graphic after a move.
        """
        self.graphic = plt.Circle((self.x,self.y), radius=self.radius,
                                  color=colorMap(self.xC), fill=False,
                                  linewidth=1)
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
            d   = balls[i].radius + balls[j].radius
            rij = balls[i].r - balls[j].r
            rijN = np.linalg.norm( rij )
            if( rijN < d ):
                # COLLISION! Case #1: Penetration
                # Game Engine Style Collision Correction
                mi = balls[i].mass
                mj = balls[j].mass
                M  = mi + mj
                rijU = rij/rijN                               # Unit Vector
                offset = (d - rijN)/2.0
                dr = offset*rijU
                balls[i].r += dr
                balls[j].r -= dr
                vij = balls[i].v - balls[j].v
                dv = 2.0*np.dot(vij,rijU)*rijU/M
                balls[i].v -= mj*dv
                balls[j].v += mi*dv
            elif( rijN == d ):
                # COLLISTION! Case #2: Perfect
                # This is going to be a VERY rare event ...
                mi = balls[i].mass
                mj = balls[j].mass
                M  = mi + mj
                rijU = rij/rijN                               # Unit Vector
                vij = balls[i].v - balls[j].v
                dv = 2.0*np.dot(vij,rijU)*rijU/M
                balls[i].v -= mj*dv
                balls[j].v += mi*dv

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
    rC = m.hypot(dW, dH)/4.0          # Diameter of circle is 1/2 of initial circle spacing.
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
            vxR = random.uniform(-10,10)   # Want ghosts to move faster? Crank this up!
            vyR = random.uniform(-10,10)   # Want ghosts to move faster? Crank this up!
            if( vxR <= 0 ):
                rcNew = rC/2.0
            else:
                rcNew = rC
            hbList.append( HB(x,y,vxR,vyR,rcNew) )
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
    ani = animation.FuncAnimation(fig, animate, frames=101,
                                  interval=100, blit=True,
                                  init_func=init, repeat=False)

    # Uncomment next two lines to write file to disk.
    # pwriter = animation.PillowWriter(fps=10, metadata=dict(artist='Dr. Ryan Clement'))
    # ani.save('../movies/hard_diffmass_box.gif',writer=pwriter)
    plt.show()