# Color Scanner
Parse a file for hex colors and display them in a GTK window, allowing click-to-copy to clipboard (usfull for making rices).

## Dependncies
This script is written in Python using GTK3. So you need to install PyGobject with pip:
```
pip install PyGobject
```
Or with your distro's package manager (usually `python-gobject` or `python3-gi`)

## Usage
```
color_scanner
```

Use the "Open" button to select a file.
Click on any color in the window to copy its hex code to the clipboard.

## TODO
- Parse alpha colors
