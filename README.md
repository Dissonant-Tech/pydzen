pydzen
======

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
seperate processes. Some of the benefits using multiple processes provides are

1. Plugins can update independantly of eachother (see volume plugin)
2. Better overall performance
3. Better battery life, as non-critical plugins can be updated less often
4. More modularity is always good :)

Installing
==========

I use pydzen with [bspwm](https://github.com/baskerville/bspwm). Setup is as simple as

```
git clone https://github.com/Dissonant-Tech/pydzen ~/.pydzen
```

Then edit `~/.config/bspwm/bspwmrc` and add `cd ~/.pydzen && ./pydzen &` at the botom.


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
    dzen accordingly
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
    output = 'dzen formated outout here'
    queue.put({'plugins.myplugin': output})

```

Now you must add `plugins.myplugin` to `pydzenrc`

```python

# plugins to load, in no particular order 
PLUGINS = ['plugins.volume','plugins.myplugin']

# order in which to put queue output
ORDER = dict (
                LEFT = [],
                CENTER = ['plugins.myplugin'],
                RIGHT = ['plugins.volume'],
                )
```

Thats it!

One final thing to note, while in the `PLUGINS` variable inside of `pydzenrc` you must use the name
of the file inside of the plugin folder, in `ORDER` you must use the name of the dictionary key it
returns to `queue`. 
For an example you can look at the `bspwm.py` plugin, which returns both `plugins.logo` and `plugins.pager`
to the queue.


Contributing
============

...Is a great idea!

There is currently a lot of work left to put into this plugin, more than I currently have time for, so if you'd like to contribute, please do!
The most notable features I have in mind are:

1. Start dzen2 from inside `pydzen.py` rather than `pydzen`. This way we can start 3 dzen instances, one for left, right and center, allowing some proper text alignment.
2. Better logging. Currently logging is handled by `centrallogger.py` so any plugins wishing to use the central logger have to call `logger = Logger(config.LOG_QUEUE)`. It would be much cleaner to have logging work with less involvment from the plugin.
3. Create an `onclick` interface that plugins can use to call scripts when clicked.
4. Create a plugin class that can be inherited?
