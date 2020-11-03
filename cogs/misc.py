from discord.ext import commands
import discord, random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief="Naret.", help="Naret.")
    async def mayo(self, ctx):
        if ctx.author.id != 311715723489705986:
            raise commands.CommandError("you're not naret.")

        await ctx.send("<:Naret:765627711778848851>")

    @commands.command(usage="<num> <list... separated by commas>",
        brief="Makes selections from a given list",
        help="Makes a specified number of selections from a given list. Selections do not repeat.")
    async def selection(self, ctx):
        msg = ctx.message

        spliteroo = msg.content.split(" ")
        if len(spliteroo) < 3:
            raise commands.CommandError("please specify a number and then a comma separated list of options")
        
        num = None
        try:
            num = int(msg.content.split(" ")[1])
        except:
            raise commands.CommandError("please specify a valid number.")
        
        options = [x.strip() for x in " ".join(spliteroo[2:]).split(",")]
        await ctx.send(", ".join(random.sample(options, num)))