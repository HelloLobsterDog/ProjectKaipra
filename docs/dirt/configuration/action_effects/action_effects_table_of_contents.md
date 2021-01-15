# Effect types

The following are the allowed values of the `type` attribute on `effect` tags:

* [**`display_text`**](display_text.md): displays the configured text to the character doing the action.
* [**`change_node`**](change_node.md): changes the current node of the character doing the action to the configured value.
* [**`set_var`**](set_var.md): sets a state_var somewhere (on nodes, characters, etc) to a value.
* [**`copy_char_properties`**](copy_char_properties.md): Copies the properties of one character onto another.
* [**`print_node_text`**](print_node_text.md): prints the text of the current node to the character doing the action.
* [**`bad_command`**](bad_command.md): displays the unrecognized command text to the character doing the action. (unsure why you would want to do this)