# Configuration Overview
There are only a handful of basic things that make up a Dirt game. All of them are created, named, configured, and filled with content in the xml configuration files.

At the top level of all configuration files is the `<water>` tag. Water tags have the following attributes, all of which are optional:

* default-lang: This attribute specifies the default language for all text-bearing tags inside this water tag, unless they specify a `lang` attribute themselves to override it or provide translation. Allowable values are any of the [standard language codes](https://en.wikipedia.org/wiki/IETF_language_tag), and by default, purely because of the native language of the developers, is "en-us".

The major tags allowable inside the water tag, and by extension, the basic building blocks which make up the engine are:

* Nodes
* Characters
* Skill Trees
* Species

Other than a handful of fairly minor tags, That's it for the water tag, and that's it for the dirt engine.

## Nodes
Nodes represent a "current location" for characters to inhabit. All characters, at all times, are "at" one node. That said, nodes are not required to actually represent a real physical location. If your story in your game has characters walking around and interacting, nodes are probably going to map pretty readily to physical location, but can just as easily map to mental states. Nodes, therefore, are a somewhat more abstract concept, and knowing what they contain will allow you to know what they can represent.

Nodes themselves have the following:
* Text, printed to the users of the characters that are there.
* State, accessible and changable by characters via actions.
* Actions, available to do by any character within the node.

[Full documentation on configuring nodes is here.](Node.md)

## Characters
Characters represent all movable, acting things. A player is a character, people are characters, but so is a gun turret, and so is a rat. Anything that does things on it's own is a character.

[Full documentation on configuring characters is here.](Character.md)

## Species
A species defines the default description, actions, template actions, stats, etc available to a character of that species. They are used to make it easier to define a character, because you don't have to re-define all the stat ranges, descriptions and actions available to all the charaters of that species.

Examples: Human, Meiv'os, Mantid, OGX-465 model gun drone, Rat.

[Full documentation on configuring species is here.](Species.md)

## Skill Trees
A skill tree is a graph of all skills available to someone who has access to the tree. They're defined as a list of skills, which define prerequisites, which is how you define the order in which characters can gain the skills within the tree.

[Full documentation on configuring skill trees and skills is here.](Skills.md)

## Minor top-level tags

* `<bad_command_error_text>`: This tag specifies the text to print whenever the user enters text as a command which isn't recognized as a command. This is a text bearing tag and allows an optional lang attribute.
* `<template_action>`: [template_action tags](template_action.md) provide templates for actions which you can reuse, without needing to configure all of the triggers, conditions and logic necessary to make them work every single time. Providing them at the water level makes them available to all species and all characters at all nodes.