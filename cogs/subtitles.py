from discord.ext import commands
import discord

class Subtitles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="on_message")
    async def subtitles(self, msg: discord.Message):
        if msg.author.bot or msg.content.startswith("fl!"):
            return
        
        subtitle = ""
        words = msg.content.split(" ")
        if "owt" in words:
            subtitle = "owt = anything"
        
        if len(subtitle) > 0:
            await msg.channel.send("```css\n[{0}]\n```".format(subtitle))