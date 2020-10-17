import discord, requests, json, re


images = {"The Skeld":"https://i.imgur.com/1DrQQAC.png",
          "Mira HQ":"https://i.imgur.com/HiDaCnp.png",
          "Polus":"https://i.imgur.com/449xJFg.png"}

reposts = dict()
settings = None
with open("./settings.json", "r") as sfile:
    settings = json.load(sfile)

async def helpmsg(msg):
    embed = discord.Embed(title="Available commands:", description=\
"""`fl!help` - Displays this message.
`fl!game <code> <server> [map] [imps] [confirm] [visual]` - Displays a custom formatted message according to the game info. \
Default settings are: skeld, 2, off, off.
`fl!gamedel` - Same as fl!game, except it deletes your own message.
`fl!repost` - Reposts the last advertised game from this server, provided it's not too old.
`fl!poll <emojis, no spaces> <message>` - Creates a poll in the polling channel.
`fl!pollchannel` - Sets the polling channel. Caller must have sufficient server permissions.
`fl!cat` - Displays a random cat picture. Only works in spam channels.
`fl!dog` - Displays a random dog picture. Only works in spam channels.
`fl!inspire` - Generate inspiring imagery. Only works in spam channels.
`fl!mayo` - naret.""")
    
    await msg.channel.send(embed=embed)

async def subreddit(msg, matches):
    desc = "**Subreddits I found in your message:**"
    isempty = True
    for match in matches:
        isempty = False
        desc += "\n[{0}](https://reddit.com/{0})".format(match.group(1))
    if isempty:
        return

    embed = discord.Embed(description=desc)
    await msg.channel.send(embed=embed)

reg = {"help":helpmsg}
def command(func):
    reg[func.__name__] = func
    return func

@command
async def game(msg):
    msglst = msg.content.split(" ")
    if msg.content.endswith("@here"):
        msglst = msglst[:-1]

    if len(msglst) < 3:
        return await failure(msg, "too few arguments.")
    if len(msglst[1]) != 6:
        return await failure(msg, "invalid game code(1): " + msglst[1])
    if not set(msglst[1].lower()).issubset(set("abcdefghijklmnopqrstuvwxyz")):
        return await failure(msg, "invalid game code(2): " + msglst[1])

    # Format the server
    server = msglst[2].lower()
    if server in ["na", "america", "northamerica", "north", "murica", "freedom", "freedomland", "guns",\
                  "rootytootypointandshooty", "an", "ns", "nq", "nz", "ma", "ba", "ja", "boba"]:
        server = "North America"
    elif server in ["eu", "europe", "eur", "euro", "baguettes", "pasta", "impasta", "sweden", "italy", "ue",\
                    "germany", "france", "tea", "norway", "buttertea", "wu", "ru", "du", "ei", "ey", "ej", "nimrob"]:
        server = "Europe"
    elif server in ["as", "asia", "nobodyusesthisserver", "rice", "oranges", "sa"]:
        server = "Asia"
    else:
        return await failure(msg, "invalid server: " + server)

    # Format the map
    mapname = msglst[3].lower() if len(msglst) > 3 else "skeld"
    if distance_fast(mapname, "skeld") < 3 or mapname == "s":
        mapname = "The Skeld"
    elif distance_fast(mapname, "mira") < 3 or mapname == "m":
        mapname = "Mira HQ"
    elif distance_fast(mapname, "polus") < 3 or mapname == "p":
        mapname = "Polus"
    else:
        return await failure(msg, "invalid map name")
    
    icon = images[mapname]
    
    def format_on_off(string):
        out = string.lower()
        if out in ["off", "no", "false", "0", "negative", "null", "nada", "nah", "ew"]:
            out = "Off"
        elif out in ["on", "yes", "true", "1", "positive", "affirmative", "yos", "mhm"]:
            out = "On"
        else:
            out = "fail"
        
        return out
    
    num = msglst[4] if len(msglst) > 4 else "2"
    if num not in ["1", "2", "3"]:
        return await failure(msg, "invalid number of impostors: " + num)
    
    confirm = format_on_off(msglst[5] if len(msglst) > 5 else "Off")
    if confirm == "fail":
        return await failure(msg, "invalid confirm state: " + msglst[5])
    visual = format_on_off(msglst[6] if len(msglst) > 6 else "Off")
    if visual == "fail":
        return await failure(msg, "invalid visual state: " + msglst[6])

    embed = discord.Embed(title="{0} - {1}".format(msglst[1].upper(), server))\
        .add_field(name="Confirm Ejects", value=confirm)\
        .add_field(name="Visual Tasks", value=visual)\
        .set_author(name="{0} | {1} Impostor{2}".format(mapname, num, "" if num == "1" else "s"),\
            icon_url=icon)
    
    await msg.channel.send(embed=embed)
    reposts[msg.guild.id] = (embed, msg.created_at)
    return True

@command
async def gamedel(msg):
    output = await game(msg)
    if output:
        await msg.delete()

@command
async def cat(msg):
    if msg.channel.name.find("spam") == -1:
        return await failure(msg, "not a spam channel.")
    r = requests.get("http://aws.random.cat/meow")
    link = r.json()["file"]
    embed = discord.Embed().set_image(url=link)
    await msg.channel.send(embed=embed)

@command
async def dog(msg):
    if msg.channel.name.find("spam") == -1:
        return await failure(msg, "not a spam channel.")
    r = requests.get("https://random.dog/woof.json?include=jpg,jpeg,png,gif")
    link = r.json()["url"]
    embed = discord.Embed().set_image(url=link)
    await msg.channel.send(embed=embed)

@command 
async def inspire(msg):
    if msg.channel.name.find("spam") == -1:
        return await failure(msg, "not a spam channel.")
    r = requests.get("https://inspirobot.me/api?generate=true")
    link = r.text
    embed = discord.Embed().set_image(url=link)
    await msg.channel.send(embed=embed)

@command
async def mayo(msg):
    if msg.author.id != 311715723489705986:
        return await failure(msg, "you're not naret.")
    
    await msg.channel.send("<:Naret:765627711778848851>")

@command
async def scribble_add(msg): #Incomplete. For now it links values with just a number, the idea is to associate words with users
    if msg.channel.id != msg.author.dm_channel.id:
        return await failure(msg, "This command only works for direct messages")

    word_list = [word.strip() for word in msg.content.split(",")]

    try:
        with open("words.json") as word_file:
            word_dict = json.load(word_file)
    except FileNotFoundError:
        word_dict = {}

    for word in word_list:
        word_dict[len(word_dict) + 1] = word

    with open("words.json", "w") as word_file:
        json.dump(word_dict, word_file)

@command
async def scribble_list(msg):
    result_msg = ""
    if msg.channel.id != msg.author.dm_channel.id:
        return await failure(msg, "This command only works for direct messages")

    with open("words.json") as world_file:
        word_dict = json.load(world_file)

    for i in word_dict:
        result_msg += ", " + word_dict[i]

    await msg.channel.send(result_msg[2:])

@command
async def repost(msg):
    gid = msg.guild.id
    if gid in reposts:
        embed, time = reposts[gid]
        elapsed = (msg.created_at - time).total_seconds()
        if elapsed > 18000: # 5 hours
            return await failure(msg, "last game ad was too long ago!")
        
        await msg.channel.send(embed=embed)
        reposts[gid] = (embed, msg.created_at)
    else:
        await failure(msg, "no previous game on record.")

@command
async def pollchannel(msg):
    gid = str(msg.guild.id)
    perms = msg.author.guild_permissions
    if not (perms.manage_channels or perms.manage_guild):
        return await failure(msg, "you don't have the necessary permissions!")
    
    if len(msg.channel_mentions) == 0:
        return await failure(msg, "no channel mentioned.")

    if gid not in settings:
        settings[gid] = {}
    settings[gid]["poll_channel"] = msg.channel_mentions[0].id
    with open("./settings.json", "r+") as sfile:
        json.dump(settings, sfile)
    
    return await msg.add_reaction("✔")

emoji_rgx = re.compile(r"(<:\w{2,}:\d{,20}>|[\U00002702-\U000027B0\U0001F1E0-\U0001FAFF])")
@command 
async def poll(msg):
    msglst = msg.content.split(" ")
    if len(msglst) < 3:
        return await failure(msg, "please specify at least 2 emojies and a message.")
    gid = str(msg.guild.id)
    if gid not in settings:
        return await failure(msg, "no polling channel set. Please set one using `fl!pollchannel`.")
    channel = find_channel(msg.guild, settings[gid]["poll_channel"])
    if channel == None:
        return await failure(msg, "invalid channel on record. Please set a new polling channel using `fl!pollchannel`.")
    
    newmsg = await channel.send(" ".join(msglst[2:]))
    emojis = msglst[1]
    for emoji in emoji_rgx.finditer(emojis):
        try:
            await newmsg.add_reaction(emoji.group(1))
        except discord.HTTPException:
            pass


def find_channel(guild, cid):
    for channel in guild.text_channels:
        if channel.id == cid:
            return channel

reg = {**reg, "kitten":cat, "puppy":dog, "doggo":dog, "catto":cat} # aliases

async def failure(msg, error):
    await msg.add_reaction("❌")
    await msg.channel.send("Error: " + error)
    return False



# borrowed my own code :)

def distance_fast(s1, s2):
    memory = {}
    return distance_mem(s1, s2, 0, 0, memory)

def distance_mem(s1, s2, a, b, memory):
    if (a, b) not in memory:
        if len(s1) - a == 0 or len(s2) - b == 0:
            memory[(a,b)] = max(len(s1) - a, len(s2) - b)
            return memory[(a,b)]
        
        if s1[a] == s2[b]:
            memory[(a,b)] = distance_mem(s1, s2, a+1, b+1, memory)
            return memory[(a,b)]
        
        add_to_first = 1+distance_mem(s1, s2, a, b+1, memory)
        
        replace_first = 1+distance_mem(s1, s2, a+1, b+1, memory)
        
        if len(s1) - a > 1 and s1[a+1] == s2[b]:
            remove_first = 1+distance_mem(s1, s2, a+2, b+1, memory)
            memory[(a,b)] = min(add_to_first, replace_first, remove_first)
            return memory[(a,b)]
        else:
            memory[(a,b)] = min(add_to_first, replace_first)
            return memory[(a,b)]
    else:
        return memory[(a, b)]