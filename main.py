import discord
from sys import argv
from os.path import exists
from json import loads
from random import randrange, choice, random
from asyncio import sleep


CHARS = "abcdefghijklmnopqrstuvwxyz"

def process_formatting(text:str, message:discord.Message):
    return text.replace("%USER%", message.author.display_name)

def process_function(response, message:discord.Message):
    match response[0]:
        case "random":
            spam = ""
            for i in range(0, randrange(response[1],response[2])):
                spam += choice(CHARS)
            if random() > 0.5:
                spam = spam.upper()
            return spam
        case "repeat":
            return response[1] * randrange(response[2], response[3])
    return ""

def main():
    global DATA
    if len(argv) < 2:
        print("Invalid arguments, expected filename")
        exit(1)
    FILENAME = f"config/{argv[1]}"

    if not exists(FILENAME):
        raise FileNotFoundError(f"File \"{FILENAME}\" does not exist")
    DATA = {}
    with open(FILENAME, 'r') as file:
        DATA = loads(file.read())
    if DATA["Token"] == None:
        return

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client=client)
    authorizedIDs = DATA["Owners"]

    @client.event
    async def on_ready():
        for guild in client.guilds:
            await guild.get_member(client.user.id).edit(nick=DATA["Nickname"])

    @client.event
    async def on_message(message: discord.Message):
        global DATA
        if message.author.id in authorizedIDs:
            if message.content == f"Hey {message.guild.get_member(client.user.id).nick}, could you reload your config please? Thank you!":
                    with open(FILENAME, 'r') as file:
                        DATA = loads(file.read())
                    await message.add_reaction("✅")
                    return
        
        if (not message.author.bot) or (message.author.id in DATA["WhitelistedBots"]):
            stimmed = False
            message_lower = message.content.lower()
            for stim, response in DATA["Stims"].items():
                if stim.lower() in message_lower:
                    stimmed = True
                    chosen_response = choice(response)
                    if not isinstance(chosen_response, str):
                        response = process_function(response=chosen_response, message=message)
                    await message.reply(process_formatting(
                        text=chosen_response,
                        message=message
                    ))
            if stimmed:
                return None
            if (randrange(1,DATA["RandomChance"]) == 1) or (client.user in message.mentions) or (DATA["Name"].lower() in message_lower):
                response = choice(DATA["Randoms"])
                if not isinstance(response, str):
                    response = process_function(response=response, message=message) 
                await message.reply(process_formatting(text=response, message=message))
                if randrange(1,DATA["AddChance"]) == 1:
                    await sleep((random()+1)*2)
                    additive = choice(DATA["Additives"])
                    if not isinstance(response, str):
                        additive = process_function(response=response, message=message)
                    await message.channel.send(process_formatting(text=additive, message=message))

    client.run(DATA["Token"])

if __name__  == '__main__':
    main()