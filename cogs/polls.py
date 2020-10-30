from discord.ext import commands
import discord, re, json

EMOJI_REGEX = re.compile(r"(<:\w{2,}:\d{,20}>|[\U00002702-\U000027B0\U0001F1E0-\U0001FAFF])")

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./settings.json", "r") as sfile:
            self.settings = json.load(sfile)
    
    @commands.command()
    async def pollchannel(self, ctx):
        msg = ctx.message

        gid = str(msg.guild.id)
        perms = msg.author.guild_permissions
        if not (perms.manage_channels or perms.manage_guild):
            raise commands.CommandError("you don't have the necessary permissions!")

        if len(msg.channel_mentions) == 0:
            raise commands.CommandError("no channel mentioned.")

        if gid not in self.settings:
            self.settings[gid] = {}
        self.settings[gid]["poll_channel"] = msg.channel_mentions[0].id
        with open("./settings.json", "r+") as sfile:
            json.dump(self.settings, sfile)

        return await msg.add_reaction("✔")

    @commands.command()
    async def poll(self, ctx):
        msg = ctx.message

        msglst = msg.content.split(" ")
        if len(msglst) < 3:
            raise commands.CommandError("please specify at least 2 emojies and a message.")
        gid = str(msg.guild.id)
        if gid not in self.settings:
            raise commands.CommandError("no polling channel set. Please set one using `fl!pollchannel`.")
        channel = msg.guild.get_channel(self.settings[gid]["poll_channel"])
        if channel == None:
            raise commands.CommandError("invalid channel on record. Please set a new polling channel using `fl!pollchannel`.")

        newmsg = await channel.send(" ".join(msglst[2:]))
        emojis = msglst[1]
        for emoji in EMOJI_REGEX.finditer(emojis):
            try:
                await newmsg.add_reaction(emoji.group(1))
            except discord.HTTPException:
                pass