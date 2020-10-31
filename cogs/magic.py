from discord.ext import commands
import discord, random

CONCH = ["Maybe someday.", "Nothing.", "Neither.", "Follow the seahorse.", "I don't think so. ",\
                   "No.", "Yes.", "Try asking again."]

POSITIVE = ["As I see it, yes.", "It is certain.", "It is decidedly so.", "Most likely.", "Outlook good.",\
                 "Signs point to yes.", "Without a doubt.", "Yes.", "Yes - definitely.", "You may rely on it."]

NEGATIVE = ["Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",\
                "Very doubtful."]

MAYBE = ["Ask again later.", "Better not tell you now.", "Cannot predict now.",\
                 "Concentrate and ask again.", "Reply hazy, try again."]

class Magic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("magic-conch")
    async def magic_conch(self, ctx):
        await ctx.send("The magic conch says: `{0}`".format(random.choice(CONCH)))

    @commands.command(name="eightball", aliases=["magic8ball", "magic-8-ball"])
    async def eightball(self, ctx):
        msg = ctx.message

        lst = None
        if random.random() < 0.25:
            lst = MAYBE
        elif hash(msg.content + str(msg.author.id)) % 2 == 0:
            lst = POSITIVE
        else:
            lst = NEGATIVE
        
        await ctx.send("The magic 8 ball says: `{0}`".format(random.choice(lst)))