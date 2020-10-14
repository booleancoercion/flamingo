import discord, commands, re

client = discord.Client()
sub_reg = re.compile(r"(r\/[A-Za-z0-9][A-Za-z0-9_]{2,20})(?:[^A-Za-z0-9]|\Z)", "g")

@client.event
async def on_ready():
    print("Logged in as", client.user)
    act = discord.Activity(name="fl!help", type=discord.ActivityType.listening)
    await client.change_presence(status=discord.Status.online, activity=act)

async def on_disconnect():
    print("Oops! Disconnected...")
    raise KeyboardInterrupt()

@client.event
async def on_message(msg):
    if msg.author == client.user: # ignore the bot's messages
        return

    msglst = msg.content.split(" ")
    """
    if not msglst[0].startswith("fl!"):
        return
    """

    if msglst[0].startswith("fl!"):
        command = msglst[0][3:]
        if command == "help":
            await commands.helpmsg(msg)
        elif command == "game":
            await commands.game(msg)
        elif command == "gamedel":
            await commands.gamedel(msg)
        else:
            await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))
        return
    
    subr_match = sub_reg.match(msg.content)
    if subr_match:
        await commands.subreddit(msg, subr_match)




tokenfile = open("./token", "r")
token = tokenfile.readline()
tokenfile.close()
client.run(token)