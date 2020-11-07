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
            
        if num > 1000:
            raise commands.CommandError("Number too high.")
        
        options = [x.strip() for x in " ".join(spliteroo[2:]).split(",")]
        choices = ", ".join(random.sample(options, num))
        embed = discord.Embed(
            title="Selected {0} out of {1} options:".format(
                num,
                len(options)
            ),
            description=choices
        )
        embed.set_footer(
            text="{0}#{1} | Yes liv, I'm a party pooper.".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)
    
    @commands.command(brief="Rolls dice.", help="Rolls dice, given in D&D notation. \
For example, to roll 2 dice of 12 sides, do fl!roll 2d12")
    async def roll(self, ctx, roll: str = "1d6"):
        sploot = roll.split("d")
        if len(sploot) != 2:
            raise commands.CommandError("Invalid input.")
        
        num = int(sploot[0])
        die = int(sploot[1])

        if num > 1000 or die > 1000:
            raise commands.CommandError("Numbers too high.")

        result = sum(random.choices(range(1, die+1), k=num))

        await ctx.send("Rolled {0}: `{1}`".format(roll, result))