# Launch X11 session
Launch a X11 session with `startx` from a tty.

## Usage
Put this in your `.profile`:
```sh
if [ "$TERM" = "linux" ]; then
    ~/scripts/start_x11_session/start_x11_session
fi
```
