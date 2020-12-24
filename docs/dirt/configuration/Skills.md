# Skill Tree Configuration
Skill trees themselves are defined very simply; they're essentially just a list of skills. The skills themselves have prerequisites, and that's where the "tree" comes from in the skill tree.

## The skill_tree tag
Skill trees are defined like this:
```
<skill_tree id="PC">
	put some skills here
</skill_tree>
```
Skill trees have an id, and some skills in them. That's it.

Skill tree ids must be unique. `skill_tree` tags are defined in `water` tags.

## Skills
Skills are defined like this:
```
<skill id="fan_the_hammer">
	<text name="Fan the Hammer">
		Unleash the remainder of your cylinder on the enemy. Requires a revolver class weapon. Take -2 to hit on all shots taken during this action.
	</text>
	<prerequisite id="pistol_proficiency" weight="0.8"/>
</skill>
```

This skill's id is fan_the_hammer. This is the name that you use to refer to the skill within the configuration, but it isn't shown to the player at all.

The skill has a single `<text>` tag. You can define multiple translations of the same text to different languages, if you provide a different lang, like `<text name="Mexican Spanish skill name" lang="es-mx">`
The text tag contains a name (this one is shown to the player), in the attribute `name`, and a descrption, defined within the tag, shown to the player as a description of what the skill actually does.

Skills are organized in a "tree" formation, in which players start at the bottom (the trunk, if you will), and must work their way up the tree by learning the skills "below" a skill you want. In order to implement this, skills define prerequisites. Prerequisites point to another skill within the same tree (via the `id` attribute), and that prerequisite has a weight (via the `weight` attribute). Both attributes are required if you declare a prerequisite. Skills with a higher weight are more likely to be learnable first by players.

## A full example
```
	<skill_tree id="PC">
		<skill id="pistol_proficiency">
			<text name="Pistol Proficiency">
				Gain 1 additional damage with all pistol class weapons
			</text>
		</skill>
		<skill id="fan_the_hammer">
			<text name="Fan the Hammer">
				Unleash the remainder of your cylinder on the enemy. Requires a revolver class weapon. Take -2 to hit on all shots taken during this action.
			</text>
			<prerequisite id="pistol_proficiency" weight="0.8"/>
		</skill>
		<skill id="quick_draw">
			<text name="Quick Draw">
				Draw your weapon with no penalty.
			</text>
			<prerequisite id="pistol_proficiency" weight="0.6"/>
		</skill>
	</skill_tree>
```

This skill tree is organized like a Y, with Fan the Hammer and Quick Draw requiring the player to learn Pistol Proficiency before they are learnable.