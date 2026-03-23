# PersonBot
Mockingly imitates people based on a json file.

WARNING! Token is stored in plain text, make sure you know what you're doing before you host this.

## Features:
- Random response
- Respond to certain words
- Add to responses
- Have functions called as a response

## Dockerfile
Build using `docker build . -t joploljojo3/personbot --build-arg CONFIG=[CONFIGFILE]` (default config file is "config.json")
Run using `docker run -v ./config:/app/config joploljojo3/personbot`
Docker container mounts /config, so config files can be updated on-the-fly