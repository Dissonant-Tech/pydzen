
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

Adding your own plugin
======================

First, you would add your plugin to the plugin directory.

```
cd .pydzen
touch plugin/myplugin.py
```

Your plugin **must** contain an update method that takes one argument named queue, your output must be sent
as a dictionary object to the queue variable as shown below. If your plugin has no output, maybe it's acting
as a backend to another plugin, you dont need to put anything into the queue, but do still need to add it to 
pydzenrc as shown below.
Your plugin may optionally import config and utils from pydzen. This will let you read
values in `pydzenrc`.

`myplugin.py`
```python
from pydzen import config, utils

def update(queue):
    queue.put({'plugins.myplugin': Output})

```

Now you must add `plugins.myplugin` to `pydzenrc`

```python
# plugins to load, in no particular order 
PLUGINS = ['plugins.volume','plugins.myplugin']

# order in which to put queue output
ORDER = dict (
                LEFT = [],
                CENTER = [plugins.myplugin],
                RIGHT = [plugins.volume],
                )
```

Thats it!

One final thing to note, while in the `PLUGINS` variable inside of `pydzenrc` you must use the name
of the file inside of the plugin folder, in `ORDER` you must use the name of the dictionary key it
returns to `queue`. 
For an example you can look at the `bspwm.py` plugin, which returns both `plugins.logo` and `plugins.pager`
to the queue.
