#!/usr/bin/env python

from distutils.core import setup

import dirt

setup(name='Dirt',
      version=dirt.__version__,
      description='Dirt is a text-based MMO game engine. Add Water (an XML game data format which Dirt reads), and you get a MUD (Multi-User Dungeon).',
      author='Daniel Westbrook',
      author_email='dan@pixelatedawesome.com',
      url='http://projects.pixelatedawesome.com/dirt/',
      packages=['dirt'],
     )
