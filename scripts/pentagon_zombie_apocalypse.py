# -*- coding: utf-8 -*-
"""
Program: pentagon_zombie_apocalypse
Created: Apr 2020
@author: Ryan Clement (RRCC)
         scisoft@outlook.com
"""

### IMPORTS
import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import AutoMinorLocator


### CLASSES
class Pentagon:
    # Class Variables
    rO       = 5   # UNITS: meters
    rI       = 2   # UNITS: meters
    numVerts = 5   # Number of Verticies
    area     = numVerts*(rO**2 - rI**2)*m.sin(m.pi/numVerts)*m.cos(m.pi/numVerts)
    # print('Area of Pentagon Hallway: ',area)

    def __init__(self):
        # Inner Pentagon
        self.pVertsI = self.__calcVerts(Pentagon.rI)
        self.pGraphI = self.__createGraphic(self.pVertsI)
        self.pVecsI  = self.__calcVecs(self.pVertsI)        # These vectors are perpendicular to the
                                                            # faces of the inner pentagon.
        self.vecMagI = np.linalg.norm(self.pVecsI[0])
        self.pUVecs = self.pVecsI/self.vecMagI              # Unit vectors perpendicular to faces of
                                                            # both pentagons (faces are parallel).
        # Outer Pentagon
        self.pVertsO = self.__calcVerts(Pentagon.rO)
        self.pGraphO = self.__createGraphic(self.pVertsO)
        self.pVecsO  = self.__calcVecs(self.pVertsO)        # These vectors are perpendicular to the
                                                            # faces of the outer pentagon.
        self.vecMagO = np.linalg.norm(self.pVecsO[0])

    def __del__(self):
        pass

    def __calcVerts(self,r):
        pVerts = []
        a, b = 2.0*m.pi/Pentagon.numVerts, m.pi/2.0
        for i in np.arange(Pentagon.numVerts):
            pVerts.append( np.array( [r*np.cos(a*i + b), r*np.sin(a*i + b)] ) )
        return pVerts

    def __calcVecs(self,pVerts):
        pVecs = []
        for i in np.arange(Pentagon.numVerts-1):
            v = (pVerts[i] + pVerts[i+1])/2.0
            pVecs.append(v)
        v = (pVerts[0] + pVerts[-1])/2.0
        pVecs.append(v)
        return pVecs

    def __createGraphic(self,pVerts):
        x = []
        y = []
        for i in np.arange(Pentagon.numVerts):
            x.append(pVerts[i][0])
            y.append(pVerts[i][1])
        x.append(pVerts[0][0])
        y.append(pVerts[0][1])
        graphic = plt.plot(x,y,c='black')
        return graphic

    def boundaryCheck(self,parList):
        for p in parList:
            d = 0
            indP = -1
            # Where is particle?
            for j in np.arange(Pentagon.numVerts):
                test = np.dot(self.pUVecs[j], p.r)
                if test > 0:
                    if test > d:
                        d = test
                        indX = j
                    # Corner case check (literally)
                    if j != indX and abs(d - test) < 1.0e-13:
                        indP = j
            # Has it crossed a boundary?
            dI = d - self.vecMagI - Particle.radius
            dO = self.vecMagO - d - Particle.radius
            if ( dI <= 0 ):
                # Crossed inner boundary
                if indP == -1:
                    vDpU = np.dot(self.pUVecs[indX],p.v)
                    delt = dI/vDpU
                    p.r -= delt*p.v
                    p.v += -2.0*vDpU*self.pUVecs[indX]
                else:   # Corner case
                    uVec = (self.pUVecs[indX] + self.pUVecs[indP])/2.0
                    mag  = np.linalg.norm(uVec)
                    uVec /= mag
                    p.r += Particle.radius*uVec
                    p.v *= -1.0

            elif ( dO <= 0 ):
                # Crossed outer boundary
                if indP == -1:
                    vDpU = np.dot(self.pUVecs[indX],p.v)
                    delt = dO/vDpU
                    p.r += delt*p.v
                    p.v += -2.0*vDpU*self.pUVecs[indX]
                else:   # Corner case
                    uVec = (self.pUVecs[indX] + self.pUVecs[indP])/2.0
                    mag  = np.linalg.norm(uVec)
                    uVec /= mag
                    p.r -= Particle.radius*uVec
                    p.v *= -1.0

    def wallDistancing(self,x,y):
        d = 0
        xy = np.array([x,y])
        for i in np.arange(Pentagon.numVerts):
            test = np.dot(self.pUVecs[i], xy)
            if test > d:
                d = test
                # indX = i
        dI = d - self.vecMagI - 1.0*Particle.radius
        dO = self.vecMagO - d - 1.0*Particle.radius
        if dI < 0 or dO < 0:
            ans = False
        else:
            ans = True
        return ans

    def plotVecs(self):
        # Plot Vectors
        originX = originY = np.zeros(5)
        xI = []
        yI = []
        xO = []
        yO = []
        xU = []
        yU = []
        for i in np.arange(Pentagon.numVerts):
            xU.append(self.pUVecs[i][0])
            yU.append(self.pUVecs[i][1])
            xI.append(self.pVecsI[i][0])
            yI.append(self.pVecsI[i][1])
            xO.append(self.pVecsO[i][0])
            yO.append(self.pVecsO[i][1])
        plt.quiver(originX,originY,xO,yO,color='b',scale_units='xy',scale=1.)
        plt.quiver(originX,originY,xI,yI,color='r',scale_units='xy',scale=1.)
        plt.quiver(originX,originY,xU,yU,color='k',scale_units='xy',scale=1.)
# END: Pentagon

class Particle:
    # Class Variables
    numInst = 0
    radius  = 0.1
    area = m.pi*radius**2
    boxArea = 4*radius**2
    # print('Area of Particle: ', area)

    def __init__(self, x, y, form, vx=0.0, vy=0.0):
        Particle.numInst += 1
        self.form = form
        if form == 'zombie':
            self.color = 'lime'
        elif form == 'human':
            self.color = 'blue'
        else:
            self.color = 'red'
        self.mass = Particle.radius**2
        self.r = np.array([x,y])
        self.v = np.array([vx,vy])

    def __del__(self):
        Particle.numInst -= 1

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
# END: Particle

class Physics:
    # Class Variables
    dt = 0.1
    time = 0.0

    def __init__(self, parList):
        self.setTimeStep(parList)

    def __del__(self):
        pass

    def setTimeStep(self,parList):
        """
        Time step control. Prevent circle centers
        from crossing in a single time-step.

        Parameters
        ----------
        parList : Python List
            List of particles used in simulation.

        Returns
        -------
        None.

        """
        for p in parList:
            vMag = m.hypot(p.vx,p.vy)
            if( vMag != 0 ):
                dt = Particle.radius/(2.0*vMag)
                Physics.dt = min(Physics.dt,dt)

    def move(self,parList):
        """
        Move particles one timestep.

        Parameters
        ----------
        parList : Python List.
            List of particles used in simulation.

        Returns
        -------
        None.

        """
        for p in parList:
            p.r += p.v*Physics.dt
        Physics.time += Physics.dt

    def collision(self,parList):
        """
        Particle collision handler.

        Parameters
        ----------
        parList : Python List.
            List of particles used in simulation.

        Returns
        -------
        None.

        """
        zombified = 0
        listLen = len(parList)
        for i in np.arange(listLen-1):
            for j in np.arange(i+1,listLen):
                d   = parList[i].radius + parList[j].radius
                rij = parList[i].r - parList[j].r
                rijN = np.linalg.norm( rij )
                if( rijN < d ):
                    # COLLISION! Case #1: Penetration
                    # Game Engine Style Collision Correction
                    mi = parList[i].mass
                    mj = parList[j].mass
                    M  = mi + mj
                    rijU = rij/rijN                               # Unit Vector
                    offset = (d - rijN)/2.0
                    dr = offset*rijU
                    parList[i].r += dr
                    parList[j].r -= dr
                    vij = parList[i].v - parList[j].v
                    dv = 2.0*np.dot(vij,rijU)*rijU/M
                    parList[i].v -= mj*dv
                    parList[j].v += mi*dv
                    # Zombification!
                    if parList[i].form == 'zombie':
                        if parList[j].form != 'zombie':
                            parList[j].form = 'zombie'
                            parList[j].color = 'lime'
                            zombified += 1
                    elif parList[j].form == 'zombie':
                        if parList[i].form != 'zombie':
                            parList[i].form = 'zombie'
                            parList[i].color = 'lime'
                            zombified += 1
                elif( rijN == d ):
                    # COLLISTION! Case #2: Perfect
                    # This is going to be a VERY rare event ...
                    mi = parList[i].mass
                    mj = parList[j].mass
                    M  = mi + mj
                    rijU = rij/rijN                               # Unit Vector
                    vij = parList[i].v - parList[j].v
                    dv = 2.0*np.dot(vij,rijU)*rijU/M
                    parList[i].v -= mj*dv
                    parList[j].v += mi*dv
                    # Zombification!
                    if parList[i].form == 'zombie':
                        if parList[j].form != 'zombie':
                            parList[j].form = 'zombie'
                            parList[j].color = 'lime'
                            zombified += 1
                    elif parList[j].form == 'zombie':
                        if parList[i].form != 'zombie':
                            parList[i].form = 'zombie'
                            parList[i].color = 'lime'
                            zombified += 1
        return zombified
# END: Physics

class Simulation:
    # Class Variables
    figW     = 8   # UNITS: inches
    figH     = 8   # UNITS: inches

    def __init__(self,numPars = 1):
        print('Welcome to the Pentagon Zombie Apocalypse!\n')
        self.numPars = numPars
        self.humans = numPars - 1
        self.zombies = 1
        self.parCnt = 0
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(Simulation.figW,Simulation.figH)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(10))
        self.ax.set_title('Pentagon Zombie Apocalypse')
        self.ax.axis('scaled')
        self.ax.set_xlim([-Pentagon.rO*1.2,Pentagon.rO*1.2])
        self.ax.set_ylim([-Pentagon.rO,Pentagon.rO*1.2])
        self.geom = Pentagon()
        self.particles = []
        self.parPatchs = []
        self.axList = []
        self.__limits()
        self.__setUp()
        self.phys = Physics(self.particles)

    def __del__(self):
        pass

    def initAnimate(self):
        return self.axList

    def animate(self,i):
        self.__cleanPlot()
        self.axList = []
        self.phys.move(self.particles)
        self.geom.boundaryCheck(self.particles)
        newZoms = self.phys.collision(self.particles)
        self.humans -= newZoms
        self.zombies += newZoms
        self.axList.append(self.ax.text(-5, 4.5, 'Time = %.4f s'%Physics.time))
        self.axList.append(self.ax.text(2.5, 4.75, 'Humans  = %i'%self.humans))
        self.axList.append(self.ax.text(2.5, 4.25, 'Zombies = %i'%self.zombies))
        for par in self.particles:
            pp = plt.Circle(par.r, radius=Particle.radius, fill=True, color=par.color)
            self.axList.append(self.ax.add_patch(pp))
        return self.axList

    def run(self,movie=False):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=269,
                                      blit=True, init_func=self.initAnimate,
                                      repeat=False)
        if movie:
            pwriter = animation.PillowWriter(fps=60, metadata=dict(artist='Dr. Ryan Clement'))
            ani.save('../movies/pentagon_zombie_apocalypse.gif',writer=pwriter)

    def __limits(self):
        maxParticles = m.floor(Pentagon.area/Particle.boxArea)   # Estimate
        numParLim = m.floor(0.5*maxParticles)
        if self.numPars <= 0:
            print("Seriously! ... You MUST have at least one person (particle)")
            print("I choose 10 very unlucky people.")
            self.numPars = 10
            self.humans = 9
        if self.numPars > 500:
            print("Set-up may take some time with this many particles.")
        if self.numPars > numParLim:
            print("Estimated Number of particles that will fit: ", maxParticles)
            print("Reducing requested number of particles to: ", numParLim)
            print("Please wait...")
            self.numPars = numParLim
            self.humans = numParLim - 1

    def __setUp(self):
        rCir = self.geom.rO         # Circumbscribed (Outer Pentagon)
        rIns = self.geom.vecMagI    # Inscribed (Inner Pentagon)
        while True:
            randD  = (rCir - rIns)*np.random.random_sample() + rIns
            randA  = 2.0*np.pi*np.random.random_sample()
            rX     = randD*m.cos(randA)
            rY     = randD*m.sin(randA)
            testWD = self.geom.wallDistancing(rX,rY)
            if not testWD:
                continue
            randV = 10.0*np.random.random_sample(2) - 5.0
            par = Particle(rX,rY,'zombie',randV[0],randV[1])  # ZOMBIE!
            self.parCnt += 1
            self.parPatchs.append(plt.Circle(par.r, radius=Particle.radius, fill=True, color=par.color))
            self.particles.append(par)
            break
        if self.numPars > 1:
            # NOTE: Assuming we won't sample another particle overlapping the first.
            while True:
                randD  = (rCir - rIns)*np.random.random_sample() + rIns
                randA  = 2.0*np.pi*np.random.random_sample()
                rX     = randD*m.cos(randA)
                rY     = randD*m.sin(randA)
                testWD = self.geom.wallDistancing(rX,rY)
                if not testWD:
                    continue
                randV = 10.0*np.random.random_sample(2) - 5.0
                par = Particle(rX,rY,'human',randV[0],randV[1])
                self.parCnt += 1
                self.parPatchs.append(plt.Circle(par.r, radius=Particle.radius, fill=True, color=par.color))
                self.particles.append(par)
                break
            while self.parCnt < self.numPars:
                while True:
                    randD  = (rCir - rIns)*np.random.random_sample() + rIns
                    randA  = 2.0*np.pi*np.random.random_sample()
                    rX     = randD*m.cos(randA)
                    rY     = randD*m.sin(randA)
                    testWD = self.geom.wallDistancing(rX,rY)
                    if not testWD:
                        continue
                    testSD = self.__socialDistancing(rX,rY)
                    if not testSD:
                        continue
                    randV = 10.0*np.random.random_sample(2) - 5.0
                    par = Particle(rX,rY,'human',randV[0],randV[1])
                    self.parCnt += 1
                    self.parPatchs.append(plt.Circle(par.r, radius=Particle.radius, fill=True, color=par.color))
                    self.particles.append(par)
                    break

    def __socialDistancing(self,x,y):
        res = True
        d   = 2.0*Particle.radius
        new = np.array([x,y])
        for j in np.arange(self.parCnt):
            rnj = new - self.particles[j].r
            rnjN = np.linalg.norm( rnj )
            if( rnjN < d ):
                res = False
        return res

    def __cleanPlot(self):
        self.ax.clear()
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(10))
        self.ax.set_title('Pentagon Zombie Apocalypse')
        self.ax.axis('scaled')
        self.ax.set_xlim([-Pentagon.rO*1.2,Pentagon.rO*1.2])
        self.ax.set_ylim([-Pentagon.rO,Pentagon.rO*1.2])
        self.tText = self.ax.text(-5, 4.5, 'Time = ')
        self.ax.add_line(self.geom.pGraphI[0])
        self.ax.add_line(self.geom.pGraphO[0])
# END: Simulation
### END: CLASSES

if '__main__' == __name__:
    numPeople = 250
    numFlag   = 1
    sim = Simulation(numPeople+1)
    sim.run(movie=False)
    plt.show()

