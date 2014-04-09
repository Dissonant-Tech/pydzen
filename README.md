
Orignal Source: https://github.com/xfire/pydzen

Overview
========

pydzen is a wrapper script around dzen, written in python, to easily create 
nice looking statusbars.


This is a fork of the older project [Pydzen](https://github.com/xfire/pydzen)

Why Fork?
=========

The older project has not been updated in a long time (6 years) and 
was missing some key features.


Due to its single threaded nature, it was not possible to update plugins
at different speeds, or near real-time. This is still very much a WIP but so
far the biggest change to the original has to be plugins now running in 
seperate processes.

How it works
============

Again, this is very much a work in progress, so things may be subject to change
but as of now it works some what similar to the original.


A very simple example would be something like:

```
    pydzen.py
        |
        |
    spawns process
    for each plugin
       /|\
      / | \
     /  |  \
    p1  p2  p3
     \  |  /
      \ | /
       \|/
    plugins return
    output to queue
        |
        |
    pydzen.py reads
    queue, updates
    accordingly
```
