import discord
from sys import argv
from os.path import exists
from json import loads
from random import randrange, choice, random
from asyncio import sleep

def process_formatting(text:str, message:discord.Message):
    return text.replace("%USER%", message.author.name)

def main():
    if len(argv) < 2:
        print("Invalid arguments, expected filename")
        exit(1)
    FILENAME = f"config/{argv[1]}"

    if not exists(FILENAME):
        raise FileNotFoundError(f"File \"{FILENAME}\" does not exist")
    DATA = {}
    with open(FILENAME, 'r') as file:
        DATA = loads(file.read())

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client=client)
    chars = "abcdefghijklmnopqrstuvwxyz"
    authorizedIDs = [] # Add your discord ID in here to be able to sync the bot's tree commands.

    @client.event
    async def on_ready():
        for guild in client.guilds:
            await guild.get_member(client.user.id).edit(nick=DATA["Nickname"])

    @client.event
    async def on_message(message: discord.Message):
        if message.author.id in authorizedIDs:
            if message.content == f"Hey {message.guild.get_member(client.user.id).nick}, could you sync please? Thank you!":
                    await tree.sync()
                    await message.add_reaction("✅")
                    return
            elif message.content == f"Hey {message.guild.get_member(client.user.id).nick}, could you reload your config please? Thank you!":
                    with open(FILENAME, 'r') as file:
                        DATA = loads(file.read())
                    await message.add_reaction("✅")
                    return
        
        if not message.author.bot:
            stimmed = False
            for stim, response in DATA["Stims"].items():
                if stim.lower() in message.content.lower():
                    stimmed = True
                    await message.reply(process_formatting(
                        text=choice(response),
                        message=message
                    ))
            if stimmed:
                return None
            if (randrange(1,DATA["RandomChance"]) == 1) or (client.user in message.mentions) or (DATA["Name"].lower() in message.content.lower()):
                response = choice(DATA["Randoms"])
                if isinstance(response, str):
                    await message.reply(response)
                    if randrange(1,DATA["AddChance"]) == 1:
                        await sleep((random()+1)*2)
                        await message.channel.send(choice(DATA["Additives"]))
                else:
                    match response[0]:
                        case "random":
                            spam = ""
                            for i in range(0, randrange(response[1],response[2])):
                                spam += choice(chars)
                            if random() > 0.5:
                                spam = spam.upper()
                            await message.reply(spam)
                        case "repeat":
                            await message.reply(response[1] * randrange(response[2], response[3]))


    client.run(DATA["Token"])

if __name__  == '__main__':
    main()