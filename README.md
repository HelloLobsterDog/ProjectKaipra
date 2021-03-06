# Project Kaipra
Project Kaipra is a Sci-Fi themed [MUD](https://en.wikipedia.org/wiki/MUD) set in the Kaipra system.

Planned features include:
* A snazzy custom setting
* A deep skill tree system, with no limited pre-defined classes
* An engaging conversation system
* A tactically sophisticated time-based combat system
* Seamless multiplayer

## Running Kaipra
Kaipra has a number of planned use cases, but currently the only one supported is running a single-user session in the command line.

To run the game, run the run_kaipra.bat file in the root of the repository, or the following command, which is all that's included in that file (minus some debugging assistance flags): 
```
python LocalClientServer.py water/kaipra/
```

## The Engine
Kaipra is built in the [Dirt](docs/dirt/dirt.md) engine, a python-based, text game engine, purpose built to make Kaipra happen, but not limited to this particular game.

It's configurable by non-developers, as long as they don't mind XML.

# Contributing
Kaipra is currently only open to contribution from those in the project already, but if you really want to help, we're quite willing to get to know you.

Those involved should consult the [contribution page](docs/kaipra/contribution.md), a bit of a dashboard on which we keep track of what needs to be done and how we plan on doing it. Keep in mind, if you plan to be a player, that page is full of spoilers.