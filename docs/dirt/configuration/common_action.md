# The action Tag
Actions are the primary way characters influence the state of the world, and are therefore the primary mechanism through which players play the game.

Actions must have 2 things:
* at least one trigger - text enterable by the player which will trigger the action to fire. This can either be straight up text or something along with a [template action](template_action.md).
* at least one effect - things that fire off and influence the world when the action fires.

And can optionally have conditions, which check that something is true, otherwise, even if the player enters text which meets one of the triggers, will prevent the action from firing.

## An Example
Here's an example of 2 actions, with all of these components, put together in a functional way:

```
<action>
	<condition var="node.grate"> False </condition>
	<trigger> pry screws </trigger>
	<trigger> lift grate </trigger>
	<effect type="display_text"> You remove the screws from the grate and lift the grate. The vents are now yours to explore. </effect>
	<effect type="set_var" var="node.grate"> True </effect>
</action>
<action>
	<condition var="node.grate"> True </condition>
	<trigger uses="go"> enter vents </trigger>
	<trigger uses="go"> enter vent </trigger>
	<effect type="display_text"> You crawl into the vents. </effect>
	<effect type="change_node"> Rattlesnake Dormitory Vents </effect>
</action>
```

Here's a breakdown:
* The first action will trigger if the player types the text "pry screws" or "lift grate"
* Because of the condition, the first action won't fire even if you type that text, if the variable "node.grate" isn't False. The variable "node.grate" means that it reads the [state_var](common_state_var.md) "grate" on the current node.
* If the player types that text, and the condition is met, the effects will fire of the first action. This action has 2: The first simply displays text to the character that did the action, and the second sets the variable "node.grate" to the value True.
* The second action has 2 triggers, all of which are dependent in some fashion on the [template action](template_action.md) "go", which is defined elsewhere. They match the text "enter vents" and "enter vent" just like the triggers on the first action, but the template action "go" can prevent the trigger from taking effect, if, for instance, the player is crippled.
* The second action has the inverse condition of the first action. If "node.grate" is False, it can fire. Note that this variable is set to this value by the first action.
* The second action has 2 effects which fire when it's triggers/conditions are met: the first displays text, and the second changes the current node of the character that does the action.

This, plus a description in the node, describing a grate, held on by rusted, flimsy screws, plus a simple [state_var](common_state_var.md) on the node, is all that's required to provide the player experience of being able to pry the screws off of a grate in front of you and crawl inside, entering the vents.

# Details of the tags
The action tag itself accepts no attributes, and no text, it is purely a container for the below 3 tags:

## Trigger
TODO

## Condition
TODO

## Effect
`effect` tags vary wildly depending on what type of effect it is. The type of effect is determined by the value of the attribute `type` on the `effect` tag, so that attribute is required.

Effects, when firing, are executed in order, from top to bottom.

[The allowed types, as well as what they do and how to configure them is available here.](action_effects/action_effects_table_of_contents.md)