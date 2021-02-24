from discord.ext import commands
import discord
import string


class Subtitles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def subtitles(self, msg: discord.Message):
        if msg.author.bot or msg.content.startswith("fl!"):
            return

        subtitles = []
        words = msg.content.translate(str.maketrans(
            '', '', string.punctuation)).lower().split(" ")
        content = msg.content.lower()

        if "owt" in words:
            subtitles.append("owt = anything")
        if "twat" in words:
            subtitles.append("twat = just stupid")
        if "wanker" in words:
            subtitles.append("wanker = idiot or fool")
        if "nip out" in content or "nipping out" in content:
            subtitles.append("nip out = going out")
        if "tapped" in words:
            subtitles.append("tapped = crazy and/or insane")

        if len(subtitles) > 0:
            await msg.channel.send("```css\n[{0}]\n```".format("]\n[".join(subtitles)))
