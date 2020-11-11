from discord.ext import commands
import discord

class PesterBee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.beecounter = 0
    

    @commands.Cog.listener(name="on_message")
    async def on_message(self, msg):
        if msg.author.id == 648864666780696576:
            self.beecounter += 1
        
        if self.beecounter >= 10:
            self.beecounter = 0
            await msg.channel.send("<@648864666780696576> go study <:duckstab:766230691209674752>")