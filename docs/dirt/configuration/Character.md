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

# The character tag itself
The character tag itself has a number of attributes you can give it. Only `id` is required.

* `id`: the id of the character. Must be unique. Required.
* `species`: an id of a species defined elsewhere in the water. Optional.
* `node`: an id of a node to start the character in. Only provide this if the character is being defined in the water. If you define the character in the node, that sets its node. Optional.

## Accepted child tags

### skill
Skill tags in characters are essentially just pointers back to a skill tree defined elsewhere.

Here's an example:
```
<skill tree="PC" id="fan_the_hammer" ignore_prerequisites="True"/>
```

Both `tree` and `id` are required, but `ignore_prerequisites` is optional.

The `tree` attribute points to the id defined in a `skill_tree` tag. The `id` attribute points to the id of the skill in the tree.

If you don't specify `ignore_prerequisites="True"` in your skill tag, and the character doesn't actually meet the prerequisites for having a skill, an error will be thrown.

### template_action
TODO

### action
[action](common_action.md) tags are common among nodes and characters, and in both spots, they follow the same rules, and do the same thing. When in characters, they provide characters the ability to perform the action anywhere, by typing in a command which fits the `trigger`s, and as long as the `condition`s are met, the `effect`s occur. See the [action page itself](common_action.md) for more information.

### state_var tags
[state_var](common_state_var.md) tags are common among nodes and characters, and in both spots, they follow the same rules, and do the same thing. They are used to create and hold data onto the thing they are defined under (in this case nodes). They provide a variable of a certain type, with a name, and a default value. The data can be accessed and changed as a part of actions, conditions, changing `text_block` text, or via template action code. see the [state_var page itself](common_state_var.md] for more information.

# An example

```
<character id="bill_billson" species="human" node="rattlesnake_hallway_1">

	<skill tree="PC" id="pistol_proficiency" />
	<skill tree="PC" id="fan_the_hammer" />

	<template_action id="look">
		<matched_text> look </matched_text>
		<matched_text> read </matched_text>
	</template_action>
	
	<action>
		<trigger target_for="look"> myself </trigger>
		<trigger target_for="look"> me </trigger>
		<effect type="display_text"> You're one attractive dude. </effect>
	</action>
	
	<state_var name="hair_good" type="boolean" default="True" />
	
</character>
```
A breakdown:

* This character has the id `bill_billson` if you need to refer to the character by id for an action.
* This character has the species `human`, which must be defined elsewhere.
* This character, by default, is placed in the node `rattlesnake_hallway_1`. Because the node is defined this way, this xml would not be valid if defined within a node.
* This character has 2 skills in the PC tree, pistol proficiency and fan the hammer.
* This character has a `look` template action, and an action which uses it, which the character can use in any node.
* This character has a state variable called `hair_good`, which is True. This can be set by actions and read by checks in text blocks.