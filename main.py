import discord, commands, re, asyncio

client = discord.Client()
sub_reg = re.compile(r"(?:[^A-Za-z0-9]|\A)(r\/[A-Za-z0-9][A-Za-z0-9_]{2,20})(?:[^A-Za-z0-9]|\Z)")
target_channel, flamingos = None, None

@client.event
async def on_ready():
    print("Logged in as", client.user)
    act = discord.Activity(name="fl!help", type=discord.ActivityType.listening)
    await client.change_presence(status=discord.Status.online, activity=act)

    for guild in client.guilds:
        if guild.id != 765157465528336444:
            continue
        global flamingos
        flamingos = guild
        break

@client.event
async def on_disconnect():
    print("Oops! Disconnected...")

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
        cmds = list(commands.reg.keys())
        if command in cmds:
            await commands.reg[command](msg)
        elif command == "channel":
            if msg.author.id != 214732126950522880:
                return await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))

            ch_id = int(msglst[1])
            for channel in flamingos.text_channels:
                if channel.id != ch_id:
                    continue
                global target_channel
                target_channel = channel
                break
        else:
            cmds.remove("say")
            closest = min(cmds, key=(lambda x: commands.distance_fast(x, command)))
            if commands.distance_fast(closest, command) < 3:
                await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference. Perhaps you meant `{1}`?".format(command, closest))
            else:
                await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))
        return
    
    matches = sub_reg.finditer(msg.content)
    await commands.subreddit(msg, matches)

    if msg.channel.id == 766265768295399424 and msg.author.id == 214732126950522880 and target_channel != None:
        async with target_channel.typing():
            await asyncio.sleep(0.3)
            await target_channel.send(msg.content)

tokenfile = open("./token", "r")
token = tokenfile.readline()
tokenfile.close()
client.run(token)