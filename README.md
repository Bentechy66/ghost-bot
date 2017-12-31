# Werewolves Ghost Bot
This bot was created to add some automated functionality to there werewolves discord server.

Created by ed588 for randium and co at the werewolves server.

## What it does
The bot allows dead participants to choose a word out of a list of 10 every 15 seconds. These words get concatenated into a sentence, and when it reaches a `.`, `?`, or `!`, it gets sent to a public channel. See [the specification from randium](spec.md) for more info.

Words are stored in `words.txt`, separated by newlines.

Configuration data is stored in `data.dat`: if you need to reset the configuration simply delete that file.

## How to use it
1. Change the SERVER_ID constant to the id of the server.
2. Change the BOT_TOKEN constant to the client token of the bot account you are using.
3. Run `main.py`
4. Get the owner of the server specified in step 1 to type `!ghost_setup` in whatever channel they want to do setup in.
5. Follow the instructions from there.
6. Get a game master to type `!ghost_stop` at any time if you want the bot to stop.

## Command list
| Command | Effect |
| :--- | :--- |
| `!ghost_setup` | Begin setup. Only usable by server owner. Only usable when the bot detects it has not been set up yet.
|  `!ghost_gmrole`, `!ghost_tavern`, `!ghost_spooky` | Used when setting up the bot. Follow the instructions given to know how to use these.
| `!ghost_stop` | Shuts down the bot. Usable by game master only.
| `!ghost_status` | Gives a nice status message. Usable by game master only.
| `!ghost_debug_reveal` | Prints a list of global variables and their values to the console. Intended for debugging purposes. Usable by game master only.

## Installation and requirements
This program requires [discord.py](https://github.com/Rapptz/discord.py/) and therefore python 3.4+. Tested and developed with python 3.6.1. and discord.py 0.16.7.
