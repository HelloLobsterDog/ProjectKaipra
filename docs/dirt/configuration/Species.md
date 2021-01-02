# Species Configuration
Species represent what type of thing a character is. For instance, a species may be Human, Meiv'os, Rat, Gun Turret, etc.

Species allow you to provide default actions, template actions and stat ranges for each of these types of thing, so you they're available to all characters of that species, and so you don't need to specify them every time you create characters.


Species have the following:
* Actions all characters of the species can perform by themselves, similar to actions available in nodes, but any character of the species can do these actions anywhere.
* Template actions, a mechanism to provide triggers and conditions for actions without needing to specify them every time. Examples include "look", "go", "smell" etc, which can be affected by things like being blinded, crippled, or not having a sense of smell, for instance if you're a robot.
* TODO Stats

# Configuration

## The Species tag itself
The species tag is specified in the water tag.

It has one attribute, `id` which is required, and must be unique among all species.

## Accepted child tags

### template_action
[template_action tags](template_action.md) provide templates for actions which you can reuse, without needing to configure all of the triggers, conditions and logic necessary to make them work every single time. Providing them at the character level makes them available to the character at all nodes.

### action
[action](common_action.md) tags are common among nodes and characters, and in both spots, they follow the same rules, and do the same thing. When in characters, they provide characters the ability to perform the action anywhere, by typing in a command which fits the `trigger`s, and as long as the `condition`s are met, the `effect`s occur. See the [action page itself](common_action.md) for more information.

## An example
```
<species id="human">
	<template_action id="look">
		<matched_text> look </matched_text>
		<matched_text> read </matched_text>
	</template_action>
	
	<action>
		<trigger target_for="look"> myself </trigger>
		<trigger target_for="look"> me </trigger>
		<effect type="display_text"> You sure are a human. </effect>
	</action>
</species>
```
A breakdown:

* This species has the id `human`, and any character may specify that they are a member of this species by providing this id in their species attribute.
* This species has a `look` template action, and an action which uses it, which any characters of this species can use in any node.