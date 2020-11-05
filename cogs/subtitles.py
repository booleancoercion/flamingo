from discord.ext import commands
import discord

class Subtitles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="on_message")
    async def subtitles(self, msg: discord.Message):
        if msg.author.bot or msg.content.startswith("fl!"):
            return
        
        subtitles = []
        words = msg.content.split(" ")
        if "owt" in words:
            subtitles.append("owt = anything")
        elif "twat" in words:
            subtitles.append("twat = really fucking annoying")
        elif "wanker" in words:
            subtitles.append("wanker = idiot or fool")
        elif "nip out" in msg.content:
            subtitles.append("nip out = going out")
        elif "tapped" in words:
            subtitles.append("tapped = crazy and/or insane")
        
        if len(subtitles) > 0:
            await msg.channel.send("```css\n[{0}]\n```".format("]\n[".join(subtitles)))