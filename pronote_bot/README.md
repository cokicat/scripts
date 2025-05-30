# Pronote Bot
A simple bot that checks every hour if you got a new grade on PRONOTE (a French software for managing schools) and sends it to a Telegram chat.

## Dependencies
This script is made in python and needs [pronotepy](https://github.com/bain3/pronotepy)
```sh
pip install -U pronotepy
```
Others dependencies (requests, getpass, sys, time and datetime) are Python built-ins. 

## Configuration
**Warning:** You must specify the URL of your school's PRONOTE server, which is the same one you use to log in to PRONOTE from a web browser.
```python
    client = pronotepy.Client(
        'https://0560026z.index-education.net/pronote/eleve.html', # change this
        username=PRONOTEPY_USERNAME,
        password=PRONOTEPY_PASSWORD
    )
```

## Launching
The PRONOTE username, password, Telegram bot token, and chat ID are prompted on start.  
The script needs to stay active continuously so I usually launch it in a detached tmux session on my server.
