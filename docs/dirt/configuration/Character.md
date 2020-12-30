# Character Configuration
Characters represent all movable, acting things. A player is a character, people are characters, but so is a gun turret, and so is a rat. Anything that does things on it's own is a character.

Characters have the following:
* A species, defining the type of thing the character is, like a Human, a Meiv'os, or a Rat. Species come along with a variety of default actions, stats, etc. See below.
* Controller, the AI or player which decides which actions the character does.
* A current node. This is where the character is at, and if the character is the player, they'll see the node's text when they play the game.
* Template actions, a set of blueprint actions the character can do, given a target or additional data. If a node has the action "look at door", the character will have a template action for looking, and the target will be the door. The template action enforces restrictions like the character being temporarily blinded, or not being able to see ultraviolet light, etc.
* A list of skill trees and a list of which skills they have in those trees. Skills are the main way characters get more powerful and gain abilities.
* Actions they can perform by themselves, similar to actions available in nodes, but you can do these actions anywhere.
* State data, set by performing actions. This can contain anything you want.
* Stats, defining a character's basic abilities to do things like lift heavy objects or speak eloquently.