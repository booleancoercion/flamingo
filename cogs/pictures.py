from discord.ext import commands
import discord, requests

def is_spam_channel(ch):
    return type(ch) == discord.DMChannel or ch.name.find("spam") != -1

class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cat", aliases=["kitten", "catto", "meow"])
    async def cat(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get("http://aws.random.cat/meow")
        link = r.json()["file"]
        embed = discord.Embed().set_image(url=link)
        await ctx.send(embed=embed)

    @commands.command(name="dog", aliases=["doggo", "puppy", "woof"])
    async def dog(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get("https://random.dog/woof.json?include=jpg,jpeg,png,gif")
        link = r.json()["url"]
        embed = discord.Embed().set_image(url=link)
        await ctx.send(embed=embed)

    @commands.command()
    async def inspire(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get("https://inspirobot.me/api?generate=true")
        link = r.text
        embed = discord.Embed().set_image(url=link)
        await ctx.send(embed=embed)