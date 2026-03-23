# PersonBot
Mockingly imitates people based on a json file.

WARNING! Token is stored in plain text, make sure you know what you're doing before you host this.

## Features:
- Random response
- Respond to certain words
- Add to responses
- Have functions called as a response

## Dockerfile
Build using `docker build --build-args CONFIG=[CONFIGFILE] [NAME]/personbot:v1 .` (default config file is "config.json")
Run using `docker run [NAME]/personbot:v1`