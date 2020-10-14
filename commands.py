import discord

images = {"The Skeld":"https://i.imgur.com/1DrQQAC.png",
          "Mira HQ":"https://i.imgur.com/HiDaCnp.png",
          "Polus":"https://i.imgur.com/449xJFg.png"}

async def helpmsg(msg):
    embed = discord.Embed(title="Available commands:", description=\
"""`fl!help` - Displays this message.
`fl!game <code> <server> [map] [imps] [confirm] [visual]` - Displays a custom formatted message according to the game info. \
Default settings are: skeld, 2, off, off.
`fl!gamedel` - Same as fl!game, except it deletes your own message.""")
    
    await msg.channel.send(embed=embed)

async def game(msg):
    msglst = msg.content.split(" ")

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
    return True

async def gamedel(msg):
    output = await game(msg)
    if output:
        await msg.delete()

async def subreddit(msg, match):
    desc = "**Subreddits I found in your message:**"
    isempty = True
    for match in matches:
        isempty = False
        desc += "\n[{0}](https://reddit.com/{0})".format(match.group(1))
    if isempty:
        return

    embed = discord.Embed(description=desc)
    await msg.channel.send(embed=embed)

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