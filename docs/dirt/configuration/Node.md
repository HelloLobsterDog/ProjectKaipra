# Node Configuration
Nodes are the basic building block of the game.

Nodes can have the following:
* **Text blocks**: One is required per node, but if your water supports multiple languages, there can be one per language. The text block is the text sent to the player when they are in the node. The text can vary based on the state of the node, the state of your character, or the state of other characters in the node.
* **Actions**: Actions defined on the node are made available to any character in the node.
* **State**: Nodes can hold variables, available to modify the text block or to influence actions.
* **Characters**: Characters can be defined inside a node as a convenience feature. This is exactly the same as defining them at the top level, but their default node is set to the node you define them in.

## The Node Tag
Here's a full example node tag, with most of the things in it which are possible to include:
```
<node id="Cell 4414a">
	<text_block>
		This is your prison cell. It is bare, beat-up concrete, with one wall made of steel bars. There is a rusty metal bed frame with an old cot, too small for the frame, sitting on it next to the right wall, and a toilet, badly in need of cleaning, against the left wall at the far end. In the center of the far wall, near the ceiling, is a vent with a grate on it, out of which is coming humid, musty air. It's awfully hot in here. There's no sheets or blankets on the bed, but given the temperature, you'd probably never use them anyway.
	</text_block>
	
	<action>
		<condition var="node.grate"> False </condition>
		<trigger> lift grate </trigger>
		<effect type="display_text"> You remove the screws from the grate and lift the grate. The vents are now yours to explore. </effect>
		<effect type="set_var" var="node.grate"> True </effect>
	</action>
	<action>
		<condition var="node.grate"> True </condition>
		<trigger target_for="go"> vent </trigger>
		<trigger uses="go"> enter vent </trigger>
		<effect type="display_text"> You crawl into the vents. </effect>
		<effect type="change_node"> Vent </effect>
	</action>
	<action>
		<trigger target_for="look"> vent </trigger>
		<effect type="display_text"> The vent is old and rusty, and just barely big enough to fit in. There are a few loose screws that could be pried off to allow you to lift the grate and enter the vents. </effect>
	</action>
	
	<state_var name="grate" type="boolean" default="False" />
</node>
```
Let's break everything down.

### The Node Tag Itself
The node tag sits right inside the water tag. It has to be named "node" and it requires 1 attribute, `id`. The id is the internal name of the node, and it isn't shown to the player. Other than not containing quotes or brackets, it can contain any characters, including spaces. The id must be unique among all nodes anywhere in the water.

### text_block tags
`text_block` tags are simple. They allow the standard optional `lang` attribute, but other than that, simply contain text. The text for nodes is printed to the player when they are in the node.

There must be 1 text_block tag in each node. If there are multiple present, each must have a different `lang` attribute, and only the one for the language the player is using will be shown to them.

### action tags
[action](common_action.md) tags are common among nodes and characters, and in both spots, they follow the same rules, and do the same thing. When in nodes, they provide characters in the node the ability to perform the action, by typing in a command which fits the `trigger`s, and as long as the `condition`s are met, the `effect`s occur. See the [action page itself](common_action.md) for more information.

### state_var tags
[state_var](common_state_var.md) tags are common among nodes and characters, and in both spots, they follow the same rules, and do the same thing. They are used to create and hold data onto the thing they are defined under (in this case nodes). They provide a variable of a certain type, with a name, and a default value. The data can be accessed and changed as a part of actions, conditions, changing `text_block` text, or via template action code. see the [state_var page itself](common_state_var.md) for more information.

## Other things not in the example

### character tags
Characters can be defined in nodes, purely as a convenience feature. Defining a character inside a node works exactly the same as defining them at the top level, but the character's default node is set to the node you're defining them in. If you do this, you cannot specify the character's default node inside [the character tag](Character.md).

The only reason to do this is as an organization mechanism; you do this if the character always starts in the node (maybe this node is the guard's room), or never leaves it (maybe it's a gun turret), or if it's easier for you to remember where they're defined if you define them in the node (maybe you're making a ship with passengers, and this node is the room they're staying in, so they always start here, but they can leave it).

### Template actions
[template_action tags](template_action.md) provide templates for actions which you can reuse, without needing to configure all of the triggers, conditions and logic necessary to make them work every single time. Providing them at the node level makes them available to all characters in the node. This is a bit of a strange use case, but it could be useful if you have one very complicated set of logic which you want to configure for many actions within one node.
