# 2D-Particle-Simulations

https://quantumwarlock.github.io/2D-Particle-Simulations/

This repository features several scripts for simulating non-relativistic elastic 2D collisions. In all cases, the particles are modeled as circles. 

## Requirements
**Anaconda Python** is recommended (need version information) but not required. A **Python3** distribution with the following modules are required: **numpy**, **random**, **matplotlib**, **math**. 

## Python Scripts
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

  Similar to *hard_box* but now the particles all have different masses which are represented by correspondingly larger or smaller radii. The radius scaling is based on constant density, *i.e.* all balls have the same density.

* **hard_diffmass_circle.py**

  Similar to *hard_diffmass_box* but in a circular boundary.

* **pentagon_zombie_apocalypse.py**

  This simulation features hard-sphere elatic collions in a pentagon. While this simulation is a bit *"...and now for something completely different"* its purpose is to create an application for the type of physics represented in this repository.

## Movies
The following files are in the *movies* directory. The animated gifs are meant to demonstrate a capability for each simulation of the same name.

* **ghost_box.gif**

* **ghost_circle.gif**

* **hard_box.gif**

* **hard_circle.gif**

* **hard_gravity_box.gif**

* **hard_diffmass_box.gif**

* **hard_diffmass_circle.gif**

* **pentagon_zombie_apocalypse.gif**




