# MinimalCommandLineMenu
A minimal python module for interactive command line menus.

A Menu has a name and menu items.
A MenuItem has a name and a func, which bears functionality.
A Menu can be prompted by calling prompt_menu and passing it as an argument.  Prompting a menu will display the menu and execute a menu item dependent on user input.
The menu items will be repeatedly prompted until the result of one of the menu funcs is falsey.

Written by John Kelliher