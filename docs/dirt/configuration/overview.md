# Configuration Overview
There are only a handful of basic things that make up a Dirt game. All of them are created, named, configured, and filled with content in the xml configuration files.

At the top level of all configuration files is the `<water>` tag. Water tags have the following attributes, all of which are optional:

* default-lang: This attribute specifies the default language for all text-bearing tags inside this water tag, unless they specify a `lang` attribute themselves to override it. Allowable values are any of the [standard language codes](https://en.wikipedia.org/wiki/IETF_language_tag), and by default, is "en-us".

The major tags allowable inside the water tag, and by extension, the basic building blocks which make up the engine are:

* Nodes
* Characters

Other than a handful of fairly minor tags, That's it for the water tag, and that's it for the dirt engine.

## Nodes
Nodes represent a "current location" for characters to inhabit. All characters, at all times, are "at" one node. That said, nodes are not required to actually represent a real physical location. If your story in your game has characters walking around and interacting, nodes are probably going to map pretty readily to physical location, but can just as easily map to mental states. Nodes, therefore, are a somewhat more abstract concept, and knowing what they contain will allow you to know what they can represent.

Nodes have the following:
* Text, print to the users of the characters that are there.
* State, accessible and changable by characters via actions.
* Actions, available to do by any character within the node.

[Full documentation on configuring nodes is here.](Node.md)

## Characters
Characters are all movable, acting things. A player is a character, people are characters, but so is a gun turret, and so is a rat. Anything that does things on it's own is a character.

Characters have the following:
* Controller, the AI or player which decides which actions the character does.
* A current node. This is where the character is at, and if the character is the player, they'll see the node's text when they play the game.
* Template actions, a set of blueprint actions the character can do, given a target or additional data. If a node has the action "look at door", the character will have a template action for looking, and the target will be the door. The template action enforces restrictions like the character being temporarily blinded, or not being able to see ultraviolet life, etc.

[Full documentation on configuring characters is here.](Character.md)

## Minor top-level tags

* `<bad_command_error_text>`: This tag specifies the text to print whenever the user enters text as a command which isn't recognized as a command. This is a text bearing tag and allows an optional lang attribute.
* `<template_action>`: TODO