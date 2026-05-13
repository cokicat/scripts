# Wallpaper  
A script I made for my dotfiles.  
Choose an image from `~/Pictures` and set it as wallpaper.

## Configuration
```shell
MENU="fuzzel -d" # Set the menu to fuzzel
WALLPAPER_COMMAND="swaybg -i" # Set the command used to change wallpaper
```
Make sure that the wallpaper is set at startup in your WM/compositor's config file, like:
```shell
swaybg -i ~/wallpaper >/dev/null 2>&1 &
```
