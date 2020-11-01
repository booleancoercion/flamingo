from discord.ext import commands
import discord, random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def mayo(self, ctx):
        if ctx.author.id != 311715723489705986:
            raise commands.CommandError("you're not naret.")

        await ctx.send("<:Naret:765627711778848851>")

    @commands.command()
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