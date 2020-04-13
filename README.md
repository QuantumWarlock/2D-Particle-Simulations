# 2D-Particle-Simulations

https://quantumwarlock.github.io/2D-Particle-Simulations/

This repository features several scripts for simulating non-relativistic elastic 2D collisions. In all cases, the particles are modeled as circles.

I may include a relativistic, inelastic example from nuclear physics in the future. Please send me an e-mail, if there is enough interest I'll include it sooner than later.

## Requirements
**Anaconda Python** is recommended (need version information) but not required. A **Python3** distribution with the following modules are required: **numpy**, **random**, **matplotlib**, **math**. 

## Python Scripts
All of the following simulations scale the radius of the particles based on the number of the particles chosen (so they fit nicely and don't overlap). The initial time-step is also scaled based on the radius and initial velocities. The radius and time-step algorithms are conservative and could both easily be increased. The scripts feature various random and initial condition correction code that can be uncommented and used to suite ones needs if useful.

The following files are located in the *scripts* directory:
* **ghost_box.py**

  The ghost particles in this simulation do not interact with each other. They simply pass through each other trying to escape the box. However the walls of the box have been enchanted with magic and stuff so they simply bounce off. It's almost like Sir Isaac Newton specified the laws governing the walls... 
  
* **ghost_circle.py**

  This ghostly simulation is much like the *ghost_box*. However, in this version of pergatory the ghosts are trapped in a circle. There is definitely something magical about finding the correct perpendicular axis to the tangent plane going on here!

* **hard_box.py**

  This simulation is a bit *billiard ball* like. The circular particles are now theoretically impenetrable. One may even conclude the collisions are elastic. Of course, my computer represents numbers by a finite collection of binary "bits" and the time-steps are kinda large by calculus standards. I'm just saying interesting (non-physical) things can happen. There is also the infinite potential at the surface of the circle assumption thing...

* **hard_circle.py**

  Hard-sphere elastic collitions in a circle.

* **hard_gravity_box.py**

  Particles undergo elastic collisions between each other and the walls while in a uniform gravity field.  

* **hard_diffmass_box.py**

  Similar to *hard_box* but now the particles all have different masses which are represented by correspondingly larger or smaller radii. The radius scaling is based on constant density, *i.e.* all balls have the same density. The relationship between the radius and the mass is given by: mass = radius**2 (density = 1/Pi).

* **hard_diffmass_circle.py**

  Similar to *hard_diffmass_box* but in a circular boundary.

* **pentagon_zombie_apocalypse.py**

  This simulation features hard-sphere elatic collions in a pentagon. While this simulation is a bit *"...and now for something completely different"* its purpose is to create an application for the type of physics represented in this repository.
  
* **nuclear_box.py**

  TBD

## Movies
The following files are in the *movies* directory. The animated gifs are meant to demonstrate a capability for each simulation of the same name.

* **ghost_box.gif**

  6 circles uniformly distributed in a 10m X 10m box stylishly colored red and blue on a white background. Initial velocities for each particle (circle) are chosen randomly (OK, pseudorandomly) from a uniform distribution between -10m/s and 10m/s. Graphic is updated once for every 10 time-steps. 

* **ghost_circle.gif**

  100 (what value!) circles on a uniform grid, based on the largest square that can be inscribed in a circle (sides chosen parallel to the enclosing box as there are an infinite number of such boxes if orientation is considered ... but, yes, they all have the same area). The circular circle (particle) boundary has a 10m diameter. The circles are colored based on thier abscissa (x-position)  via a wonderfully delightful rainbow scheme! Initial velocities are chosen from a uniform distribution between -3m/s and 3m/s. Graphic is updated every 10 time-steps. 

* **hard_box.gif**

  9 circles uniformly distributed in the enclosing box with initial velocities chosen randomly between -10m/s and 10m/s. The rainbow coloring map is used. If you are feeling stressed choose this simulation to watch ... kinda like a screen-saver.

* **hard_circle.gif**

  400 hard circles bouncing around in a circle. Graphic is updated every 10 time-steps. It's Petri dish like.

* **hard_gravity_box.gif**

  Balls are released with zero initial velocity. They fall in vertical columns under the influence of gravity and then do only what a simulation can.

* **hard_diffmass_box.gif**

  100 particles are given random velocities between -10m/s and 10m/s. If the x-component of velocity is in the interval [-10,0] the radius is halved and, therefore, the mass reduced by a factor of 4. If you ever wondered what soap bubbles would do if they didn't stick or pop this is what you have been waiting to see!

* **hard_diffmass_circle.gif**

  TBD

* **pentagon_zombie_apocalypse.gif**

  TBD

* **nuclear_box.gif**

  TBD




