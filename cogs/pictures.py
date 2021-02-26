from discord.ext import commands
import discord
import requests


def is_spam_channel(ch):
    return type(ch) == discord.DMChannel or ch.name.find("spam") != -1


class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cat", aliases=["kitten", "catto", "meow"],
                      brief="Displays a random cat picture.",
                      help="Displays a random cat picture. Only works in spam channels.")
    async def cat(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get("http://aws.random.cat/meow")
        link = r.json()["file"]
        await ctx.send(link)

    @commands.command(name="dog", aliases=["doggo", "puppy", "woof"],
                      brief="Displays a random dog picture.",
                      help="Displays a random dog picture. Only works in spam channels.")
    async def dog(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get(
            "https://random.dog/woof.json?include=jpg,jpeg,png,gif")
        link = r.json()["url"]
        await ctx.send(link)

    @commands.command(brief="Generate inspiring imagery.",
                      help="Generate inspiring imagery. Only works in spam channels.")
    async def inspire(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get("https://inspirobot.me/api?generate=true")
        link = r.text
        await ctx.send(link)
