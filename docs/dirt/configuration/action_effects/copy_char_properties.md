# `copy_char_properties` Effect Configuration
This effect copies properties from one character into another, overwriting the properties of the other character.

The character that the properties are copied into is, by default, the character doing the action, but it can be configured to be any other character.

By default, all properties are copied, making the characters effectively identical.

# Examples

```
<effect type="copy_char_properties" copyFrom="bill_billson" />
<effect type="copy_char_properties" copyFrom="bill_billson" copyTo="john_johnson" />
<effect type="copy_char_properties">
	skills, currentNode
</effect>
```

# Effect Tag Configuration
The effect tag requires an attribute `copyFrom`, and can have the optional attribtue `copyTo`. Both take the id of a character.

If not provided, `copyTo` will be filled with the character that is preforming the action.

If there is text in the tag, it will be a comma-separated list of things to copy. The list of allowed things in the list is below.

## Things that can be copied
The following things are allowed in the text of the tag, all of which do what you'd expect:

* currentNode
* templateActions
* state
* actions
* species
* skills

### Things that cannot be copied
* id
* controller
