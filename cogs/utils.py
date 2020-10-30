import discord, re, asyncio
from discord.ext import commands

SUB_REG = re.compile(r"(?<!reddit\.com)(?:[^A-Za-z0-9]|\A)(r\/[A-Za-z0-9][A-Za-z0-9_]{2,20})(?:[^A-Za-z0-9]|\Z)")

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="on_message")
    async def logger(self, msg):
        logch = self.bot.get_channel(768464621031653497)

        if msg.channel.id != logch.id:
            content = discord.utils.escape_mentions(msg.content)
            try:
                if msg.channel.id != msg.author.dm_channel.id:
                    await logch.send("`{0}#{1} -> #{2} ({3})`: ".format(msg.author.name, msg.author.discriminator,\
                                    msg.channel.name, msg.guild.name) + content)
                else:
                    await logch.send("`{0}#{1}`: ".format(msg.author.name, msg.author.discriminator) + content)
            except:
                await logch.send("`{0}#{1} -> #{2} ({3})`: ".format(msg.author.name, msg.author.discriminator,\
                                msg.channel.name, msg.guild.name) + content)
    
    @commands.Cog.listener(name="on_message")
    async def subreddits(self, msg):
        if msg.content.startswith("fl!"):
            return
        matches = SUB_REG.finditer(msg.content)

        desc = "**Subreddits I found in your message:**"
        matches = set(map(lambda x: x.group(1), matches))
        if len(matches) == 0:
            return
        for match in matches:
            desc += "\n[{0}](https://reddit.com/{0})".format(match)

        embed = discord.Embed(description=desc)
        await msg.channel.send(embed=embed)

    @commands.command(name="help")
    async def helpmsg(ctx):
        embed = discord.Embed(title="Available commands:", description= \
        """`fl!help` - Displays this message.
`fl!game <code> <server> [map] [imps] [confirm] [visual]` - Displays a custom formatted message according to the game info. \
Default settings are: skeld, 2, off, off.
`fl!gamedel` - Same as fl!game, except it deletes your own message.
`fl!repost` - Reposts the last advertised game from this server, provided it's not too old.
`fl!poll <emojis, no spaces> <message>` - Creates a poll in the polling channel.
`fl!pollchannel` - Sets the polling channel. Caller must have sufficient server permissions.
`fl!codenames-teams <list of user @mentions>` - Separates players into red and blue teams.
`fl!codenames-over` - Removes spy roles from everyone.
`fl!cat` - Displays a random cat picture. Only works in spam channels.
`fl!dog` - Displays a random dog picture. Only works in spam channels.
`fl!inspire` - Generate inspiring imagery. Only works in spam channels.
`fl!scribble-add <word1>, <word2>, ...` - Adds custom words to the server's scribble word list (Only works in DM)
`fl!scribble-list` - Shows the scribble words you've added to the server's list (Only works in DM)
`fl!scribble-remove <index>/all` - Command to remove one of your custom words. Using the `fl!scribble-list` command you 
know what's the word's index value. Or you can use `fl!scribble-remove all` to remove all your words.
`fl!mayo` - naret.
`fl!eightball [query]` - Asks the almighty magic eight ball a yes or no question.
`fl!magic-conch [query]` - Asks the even more powerful magic conch a question.""")

        await ctx.send(embed=embed)

def distance_fast(s1, s2):
    memory = {}
    return distance_mem(s1, s2, 0, 0, memory)

def distance_mem(s1, s2, a, b, memory):
    if (a, b) not in memory:
        if len(s1) - a == 0 or len(s2) - b == 0:
            memory[(a, b)] = max(len(s1) - a, len(s2) - b)
            return memory[(a, b)]

        if s1[a] == s2[b]:
            memory[(a, b)] = distance_mem(s1, s2, a + 1, b + 1, memory)
            return memory[(a, b)]

        add_to_first = 1 + distance_mem(s1, s2, a, b + 1, memory)

        replace_first = 1 + distance_mem(s1, s2, a + 1, b + 1, memory)

        if len(s1) - a > 1 and s1[a + 1] == s2[b]:
            remove_first = 1 + distance_mem(s1, s2, a + 2, b + 1, memory)
            memory[(a, b)] = min(add_to_first, replace_first, remove_first)
            return memory[(a, b)]
        else:
            memory[(a, b)] = min(add_to_first, replace_first)
            return memory[(a, b)]
    else:
        return memory[(a, b)]
