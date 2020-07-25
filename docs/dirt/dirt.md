# Dirt
Dirt is the python-based text game engine that makes Kaipra happen.

It is architected such that it's not limited to just this game, but it is custom-built for this particular game, so alot of text based games may be possible in Dirt, but those set in other types of settings (fantasy, for instance) aren't quite as supported as our sci-fi setting.

## Configuration
Dirt is configured by adding "water", the xml configuration files which "hydrate" the bare engine with content, to make a multiplayer text based game, which is often called a MUD.

The water format is designed such that non-developers (who can handle xml) can configure it. Documentation on configuring the engine is available [here](configuration/overview.md).

## Using Dirt as a library
Dirt can be installed in python as a standalone library, for integating into projects other than this one.

The plan is to have Dirt up on PyPi, such that the following command will download and install it into your python:
```
pip install dirt
```
...but this hasn't quite happened yet. This will occur once the engine is mature enough to be worth downloading, which will occur as a consequence of making Kaipra.