from discord.ext import commands
import discord, re, asyncio, random

SUB_REG = re.compile(r"(?<!reddit\.com)(?:[^A-Za-z0-9]|\A)(r\/[A-Za-z0-9][A-Za-z0-9_]{2,20})(?:[^A-Za-z0-9]|\Z)")
BOTSAY_ALLOWED = [214732126950522880, 642071692037980212]

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = None
    
    @commands.Cog.listener(name="on_message")
    async def logger(self, msg):
        logch = self.bot.get_channel(768464621031653497)

        if msg.channel.id != logch.id:
            content = discord.utils.escape_mentions(msg.content)

            if type(msg.channel) != discord.DMChannel:
                await logch.send("`{0}#{1} -> #{2} ({3})`: ".format(msg.author.name, msg.author.discriminator,\
                                msg.channel.name, msg.guild.name) + content)
            else:
                await logch.send("`{0}#{1}`: ".format(msg.author.name, msg.author.discriminator) + content)

    
    @commands.Cog.listener(name="on_message")
    async def subreddits(self, msg): # if this is changed, consider ignoring the bot
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
    
    @commands.Cog.listener(name="on_message")
    async def botsay(self, msg):
        if msg.channel.id == 766265768295399424 and msg.author.id in BOTSAY_ALLOWED and self.target_channel is not None:
            async with self.target_channel.typing():
                await asyncio.sleep(0.3)
                await self.target_channel.send(msg.content)
    
    @commands.command(hidden=True)
    async def channel(self, ctx, ch_id: int):
        if ctx.author.id not in BOTSAY_ALLOWED:
            return await ctx.send("Unknown command `{0}`. Please use fl!help for reference.".format(ctx.command.name))

        flamingos = self.bot.get_guild(765157465528336444)
        for channel in flamingos.text_channels:
            if channel.id != ch_id:
                continue
            self.target_channel = channel
            break
    
    @commands.command(brief="Rolls dice.", help="Rolls dice, given in D&D notation. \
For example, to roll 2 dice of 12 sides, do fl!roll 2d12")
    async def roll(self, ctx, roll: str = "1d6"):
        sploot = roll.split("d")
        if len(sploot) != 2:
            raise commands.CommandError("Invalid input.")
        
        num = int(sploot[0])
        die = int(sploot[1])

        result = sum(random.choices(range(1, die+1), k=num))

        await ctx.send("Rolled {0}: `{1}`".format(roll, result))

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
