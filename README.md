# PersonBot
Mockingly imitates people based on a json file.

WARNING! Token is stored in plain text, make sure you know what you're doing before you host this.

## Table of Contents
* [Features](#features)
* [Dockerfile](#dockerfile)
* [Docker compose](#docker-compose)
* <details>
    <summary><a href="#config">Config</a></summary>

    + [Template](#template)
    + [Name](#name)
    + [Nickname](#nickname)
    + [Token](#token)
    + [Owners](#owners)
    + [WhitelistedBots](#whitelistedbots)
    + [RandomChance](#randomchance)
    + [AddChance](#addchance)
    + [Randoms](#randoms)
    + [Additives](#additives)
    + [Stims](#stims)
    </details>
* <details>
    <summary><a href="#config-formatting">Config Formatting</a></summary>

    + [Supported tags](#supported-tags)
    </details>
* [Functions](#functions)

## Features
- Random response
- Respond to certain words
- Add to responses
- Have functions called as a response

## Dockerfile
Build using `docker build . -t joploljojo3/personbot --build-arg CONFIG=[CONFIGFILE]` (default config file is "config.json")
Run using `docker run -v ./config:/app/config joploljojo3/personbot`
Docker container mounts /config, so config files can be updated on-the-fly

## Docker compose
A compose.yml file is included, and can be used by just changing what config file is used. You can add more versions by duplicating everything under and including the "bot:" section.

## Config
The config file is used to configure the bot to your liking.
### Template
```json
{
    "Name": "",
    "Nickname": "",
    "Token": "",
    "Owners": [],
    "WhitelistedBots": [],
    "RandomChance": 0,
    "AddChance": 0,
    "Randoms": [
        ""
    ],
    "Additives": [
        ""
    ],
    "Stims": {
        "": [""]
    }
}
```

### Name
This is used as the bot's name. If this is mentioned in a message, it will respond to it based on [NameChance](#namechance).

### Nickname
This is the name that will be used as the bot'snickname in all guilds it's in. Also listens to thisfor reloading config.

### Token
This is the bot's token. Currently stored in plaintext, so make sure you know what you're doing when deploying.

### Owners
A list of "owner" IDs that are allowed to reload the bot's config.

### WhitelistedBots
A list of whitelisted bot's IDs that will not be ignored, despite them being a bot.

### RandomChance
The chance (1 in n) to respond to any message sent by a user. (bots are ignored)

### AddChance
The chance (1 in n) to add an extra message onto a response after a delay.

### NameChance
The chance (1 in n) to respond to the bot's [name](#name)

### Randoms
A list of random messages to choose from when responding to a message. (supports [formatting](#config-formatting) and [functions](#functions))

### Additives
A list of random additive messages to choose from when adding onto a response. (supports [formatting](#config-formatting) and [functions](#functions))

### Stims
A key-pair value of things to specifically respond to. When key is found, it chooses a random value from the list supplied, and responds with that. first value of the list must be a number, and specifies the odds of responding with that stim. (cancels any further random interaction, also supports [formatting](#config-formatting) and [functions](#functions))

## Config Formatting
Any formatting-supported text can use tags to replace text.

### Supported tags
- %USER%
Gets replaced with the message author's name. (or nickname if applicable)

## Functions
Functions are called from randomly selected responses, and are defined as follows:
```json
"Randoms": [
    "My Response",
    ["My Function", "param1", "param2"]
]
```

these are then called and executed. There's some default functions provided, but it's recommended you make your own according to your liking.