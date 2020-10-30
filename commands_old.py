import discord, requests, json, re, random

flamingo_channel = None
settings = None
with open("./settings.json", "r") as sfile:
    settings = json.load(sfile)

reg = {}
def command(*args):
    if callable(args[0]):
        reg[args[0].__name__] = args[0]
        return args[0]
    
    else:
        def decorator(func):
            for name in args:
                if type(name) != str:
                    raise TypeError()
                reg[name] = func
            return func
        return decorator
            
# Syntax: if you want to add the command as is (i.e. same name as the function),
# write @command above with nothing else. If you want to register aliases, write
# @command(name, alias1, alias2, ...) above the function.

def find_role(lst, role_name):
    role_name = role_name.lower()
    for role in lst:
        if role.name.lower().find(role_name) != -1:
            return role

def remove_duplicate_snowflakes(lst):
    ids = set()
    def func(x):
        if x.id in ids:
            return False
        ids.add(x.id)
        return True
    return list(filter(func, lst))

codenames_timeout = None
@command("codenames-teams")
async def codenames(msg, members=None):
    global codenames_timeout
    if codenames_timeout != None:
        if (msg.created_at - codenames_timeout).total_seconds() < 60:
            pass
    codenames_timeout = msg.created_at

    roles = msg.guild.roles
    red_spy = find_role(roles, "red spy")
    blue_spy = find_role(roles, "blue spy")

    if members == None:
        members = list()
    
    members.extend(msg.mentions)

    first_space = msg.content.find(" ")
    if first_space != -1:
        names = msg.content[first_space+1:].split(",")
        for name in names:
            result = msg.guild.get_member_named(name.strip())
            if result != None:
                members.append(result)
    
    members = remove_duplicate_snowflakes(members)
    random.shuffle(members)

    midpoint = len(members)//2
    red_team = members[:midpoint]
    blue_team = members[midpoint:]

    output_red = "**Red Team:**"
    for member in red_team:
        if member in blue_spy.members:
            await member.remove_roles(blue_spy, reason="Codenames teaming")
        await member.add_roles(red_spy, reason="Codenames teaming")
        output_red += "\n<@{}>".format(member.id)
    
    output_blue = "**Blue Team:**"
    for member in blue_team:
        if member in red_spy.members:
            await member.remove_roles(red_spy, reason="Codenames teaming")
        await member.add_roles(blue_spy, reason="Codenames teaming")
        output_blue += "\n<@{}>".format(member.id)
    
    await msg.channel.send(output_red)
    await msg.channel.send(output_blue)
    
@command("codenames-over")
async def codenames_over(msg):
    roles = msg.guild.roles
    red_spy = find_role(roles, "red spy")
    blue_spy = find_role(roles, "blue spy")

    for member in red_spy.members:
        await member.remove_roles(red_spy, reason="Codenames over")
    
    for member in blue_spy.members:
        await member.remove_roles(blue_spy, reason="Codenames over")
    
    await msg.add_reaction("✅")

@command("codenames-shuffle")
async def codenames_shuffle(msg):
    roles = msg.guild.roles
    red_spy = find_role(roles, "red spy")
    blue_spy = find_role(roles, "blue spy")
    members = red_spy.members + blue_spy.members

    return await codenames(msg, members=members)




@command("cat", "kitten", "catto", "meow")
async def cat(msg):
    if msg.channel.name.find("spam") == -1:
        return await failure(msg, "not a spam channel.")
    r = requests.get("http://aws.random.cat/meow")
    link = r.json()["file"]
    embed = discord.Embed().set_image(url=link)
    await msg.channel.send(embed=embed)

@command("dog", "doggo", "puppy", "woof")
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


@command("scribble-add")
async def scribble_add(msg):
    if msg.author.dm_channel == None or msg.channel.id != msg.author.dm_channel.id:
        return await failure(msg, "This command only works for direct messages")

    commands = msg.content.split(" ", 1)
    if len(commands) < 1:
        return await failure(msg, "No words found")
    new_words = [word.strip() for word in commands[1].split(",")]
    author_id = str(msg.author.id)

    try:
        with open("words.json") as word_file:
            word_list = json.load(word_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(e)
        word_list = {}

    if author_id not in word_list: #Creating an array if none exists.
        word_list[author_id] = []
    for word in new_words:
        if word not in word_list[author_id]:
            word_list[author_id].append(word.strip().lower())

    with open("words.json", "w") as word_file:
        json.dump(word_list, word_file)

    return await msg.channel.send("Your words were added, thank you. You can use fl!scribble_list to see "
                                  "your word list")

@command("scribble-list")
async def scribble_list(msg):
    if not isinstance(msg.channel, discord.DMChannel):
        return await failure(msg, "This command only works for direct messages")

    try:
        with open("words.json") as word_file:
            word_list = json.load(word_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(e)
        word_list = {}

    author_id = str(msg.author.id)
    result_msg = ""

    commands = msg.content.split(" ")
    if len(commands) > 1:  # Looking for special keywords
        if commands[1] == "users":  # This keyword will send all the users with their word list
            for user_id in word_list:
                result_msg += user_id + ": "
                for i in range(len(word_list[user_id])):
                    result_msg += word_list[user_id][i] + ", "
                result_msg = result_msg[:-2] + "\n\n"
        elif commands[1] == "full":  # This keyword just sends the list word to be used for the game
            word_array = []
            for user_id in word_list:
                for i in range(len(word_list[user_id])):
                    if word_list[user_id][i] not in word_array:
                        word_array.append(word_list[user_id][i])
            for word in word_array:
                result_msg += ", " + word
            result_msg = result_msg[2:]
        elif commands[1] in word_list: # Checks if a user ID was passed, and returns their list
                result_msg += commands[1] + ":\n"
                for i in range(len(word_list[commands[1]])):
                    result_msg += str(i+1) + ". " + word_list[commands[1]][i] + "\n"
        else:
            return await failure(msg, "Oops, something went wrong. Try using fl!scribble-list instead")
        if result_msg == "":
            result_msg = "The list is empty"
        return await msg.channel.send(result_msg)

    if author_id in word_list:  # List with only the author's words
        author_word_list = word_list[author_id]
        if len(author_word_list) == 0:
            result_msg = "Your word list is empty"
            word_list.pop(author_id, None)
        else:
            for i in range(len(author_word_list)):
                result_msg += str(i + 1) + ". " + author_word_list[i] + "\n"
    else:
        result_msg = "Your word list is empty"

    return await msg.channel.send(result_msg.strip())

@command("scribble-remove")
async def scribble_remove(msg):
    if not isinstance(msg.channel, discord.DMChannel):
        return await failure(msg, "This command only works for direct messages")

    try:
        with open("words.json") as word_file:
            word_list = json.load(word_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(e)
        word_list = {}

    author_id = str(msg.author.id)
    commands = msg.content.split(" ", 1)

    if len(commands) < 2:
        return await failure(msg, "Please specify which word to remove with an index given by fl!scribble_list or"
                             " clear your whole list with fl!scribble_remove all")

    result_msg = ""
    try:
        index = int(commands[1]) - 1
        if index < 0 or index >= len(word_list[author_id]):
            return await failure(msg, "There are no words with that index")
        removed_word = word_list[author_id].pop(index)
        if len(word_list) == 0:
            word_list.pop(author_id, None)
        result_msg = "Done! `" + removed_word + "` was removed"
    except ValueError: # Valid index not found, looking for keyword/subcommand
        if commands[1] == "all":
            if word_list.pop(author_id, None) is not None:
                result_msg = "Done! all the words in your list were removed"
            else:
                result_msg = "You don't have a list to remove"
        elif commands[1].startswith("users"):
            global flamingo_channel  # Below we verify the user is an admin of the flamingo server
            try: # fl!scribble-remove users [user_id]/clear [index]/all
                member = await flamingo_channel.fetch_member(msg.author.id)
                if member.guild_permissions.administrator:
                    sub_commands = commands[1].split(" ")
                    if len(sub_commands) < 2:
                        return await failure(msg, "Missing arguments")
                    elif sub_commands[1] == "clear":
                        word_list = {}
                        result_msg = "All the words were removed from the list"
                    elif sub_commands[1] not in word_list:
                            result_msg = "User doesn't have a word list"
                    elif len(sub_commands) < 3:
                        return await failure(msg, "Missing argument")
                    else:
                        try:
                            user_index = int(sub_commands[2]) - 1
                            if user_index < 0 or user_index >= len(word_list[sub_commands[1]]):
                                return await failure(msg, "User: " + sub_commands[1] + " has no words with that index")
                            removed_word = word_list[sub_commands[1]].pop(user_index)
                            if len(word_list[sub_commands[1]]) == 0:
                                word_list.pop(sub_commands[1], None)
                            result_msg = "Done! user: " + sub_commands[1] + "'s `" + removed_word + "` was removed"
                        except ValueError:
                            if sub_commands[2] == "all":
                                word_list.pop(sub_commands[1])
                                result_msg = "All the user: " + sub_commands[1] + "'s words were removed from the list"
                            else:
                                return await failure(msg, "Invalid command")
                else:
                    return await failure(msg, "Only Flamingo's admins can use this command")
            except (discord.Forbidden, discord.HTTPException) as e:
                print(e)
                return await failure(msg, "Error: couldn't find member")
        else:
            return await failure(msg, "Please specify which word to remove with an index given by fl!scribble_list or"
                                      " clear your whole list with fl!scribble_remove all")

    with open("words.json", "w") as word_file:
        json.dump(word_list, word_file)
    return await msg.channel.send(result_msg)

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
    channel = msg.guild.get_channel(settings[gid]["poll_channel"])
    if channel == None:
        return await failure(msg, "invalid channel on record. Please set a new polling channel using `fl!pollchannel`.")

    newmsg = await channel.send(" ".join(msglst[2:]))
    emojis = msglst[1]
    for emoji in emoji_rgx.finditer(emojis):
        try:
            await newmsg.add_reaction(emoji.group(1))
        except discord.HTTPException:
            pass

conch_responses = ["Maybe someday.", "Nothing.", "Neither.", "Follow the seahorse.", "I don't think so. ",\
                   "No.", "Yes.", "Try asking again."]

@command("magic-conch")
async def magic_conch(msg):
    await msg.channel.send("The magic conch says: `{0}`".format(random.choice(conch_responses)))


pos_responses = ["As I see it, yes.", "It is certain.", "It is decidedly so.", "Most likely.", "Outlook good.",\
                 "Signs point to yes.", "Without a doubt.", "Yes.", "Yes - definitely.", "You may rely on it."]

neg_reponses = ["Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",\
                "Very doubtful."]

may_responses = ["Ask again later.", "Better not tell you now.", "Cannot predict now.",\
                 "Concentrate and ask again.", "Reply hazy, try again."]

@command("magic8ball", "magic-8-ball", "eightball")
async def eightball(msg):
    lst = None
    if random.random() < 0.25:
        lst = may_responses
    elif (hash(msg.content) + hash(msg.author.id)) % 2 == 0:
        lst = pos_responses
    else:
        lst = neg_reponses
    
    await msg.channel.send("The magic 8 ball says: `{0}`".format(random.choice(lst)))


@command
async def selection(msg):
    spliteroo = msg.content.split(" ")
    if len(spliteroo) < 3:
        return await failure(msg, "please specify a number and then a comma separated list of options")
    
    num = None
    try:
        num = int(msg.content.split(" ")[1])
    except:
        return await failure(msg, "please specify a valid number.")
    
    options = [x.strip() for x in " ".join(spliteroo[2:]).split(",")]
    await msg.channel.send(", ".join(random.sample(options, num)))

async def failure(msg, error):
    await msg.add_reaction("❌")
    await msg.channel.send("Error: " + error)