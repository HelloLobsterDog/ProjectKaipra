# Effect types

The following are the allowed values of the `type` attribute on `effect` tags:

* *`[display_text](display_text.md)`*: displays the configured text to the character doing the action.
* `change_node`: changes the current node of the character doing the action to the configured value.
* `set_var`: sets a state_var somewhere (on nodes, characters, etc) to a value.
* `print_node_text`: prints the text of the current node to the character doing the action.
* `bad_command`: displays the unrecognized command text to the character doing the action. (unsure why you would want to do this)