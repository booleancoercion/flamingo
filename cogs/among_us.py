import discord.ext.commands as commands
from discord.ext.commands import CommandError
import discord

from .utils import distance_fast

images = {"The Skeld": "https://i.imgur.com/1DrQQAC.png",
          "Mira HQ": "https://i.imgur.com/HiDaCnp.png",
          "Polus": "https://i.imgur.com/449xJFg.png"}

class AmongUs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reposts = dict()
    
    @commands.command()
    async def game(self, ctx, code, server, mapname="skeld", imps=2, confirm="off", visual="off"):
        msg = ctx.message

        if len(code) != 6:
            raise CommandError("invalid game code(1): " + code)
        if not set(code.lower()).issubset(set("abcdefghijklmnopqrstuvwxyz")):
            raise CommandError("invalid game code(2): " + code)

        # Format the server
        server = server.lower()
        if server in ["na", "america", "northamerica", "north", "murica", "freedom", "freedomland", "guns", \
                    "rootytootypointandshooty", "an", "ns", "nq", "nz", "ma", "ba", "ja", "boba"]:
            server = "North America"
        elif server in ["eu", "europe", "eur", "euro", "baguettes", "pasta", "impasta", "sweden", "italy", "ue", \
                        "germany", "france", "tea", "norway", "buttertea", "wu", "ru", "du", "ei", "ey", "ej", "nimrob"]:
            server = "Europe"
        elif server in ["as", "asia", "nobodyusesthisserver", "rice", "oranges", "sa"]:
            server = "Asia"
        else:
            raise CommandError("invalid server: " + server)

        # Format the map
        mapname = mapname.lower()
        if distance_fast(mapname, "skeld") < 3 or mapname == "s":
            mapname = "The Skeld"
        elif distance_fast(mapname, "mira") < 3 or mapname == "m":
            mapname = "Mira HQ"
        elif distance_fast(mapname, "polus") < 3 or mapname == "p":
            mapname = "Polus"
        else:
            raise CommandError("invalid map name: " + mapname)

        icon = images[mapname]

        def format_on_off(string):
            out = string.lower()
            if out in ["off", "no", "false", "0", "negative", "null", "nada", "nah", "ew"]:
                out = "Off"
            elif out in ["on", "yes", "true", "1", "positive", "affirmative", "yos", "mhm"]:
                out = "On"
            else:
                out = "fail"

            return out

        if imps not in [1, 2, 3]:
            raise CommandError("invalid number of impostors: " + str(imps))

        confirm = format_on_off(confirm)
        if confirm == "fail":
            raise CommandError("incalid confirm state: " + confirm)
        visual = format_on_off(visual)
        if visual == "fail":
            raise CommandError("incalid visual state: " + confirm)

        embed = discord.Embed(title="{0} - {1}".format(code.upper(), server)) \
            .add_field(name="Confirm Ejects", value=confirm) \
            .add_field(name="Visual Tasks", value=visual) \
            .set_author(name="{0} | {1} Impostor{2}".format(mapname, imps, "" if imps == 1 else "s"), \
                        icon_url=icon)

        await ctx.send(embed=embed)
        self.reposts[msg.guild.id] = (embed, msg.created_at)
        return True
    
    @commands.command()
    async def gamedel(self, ctx, *args):
        output = await self.game(ctx, *args)
        if output:
            await ctx.message.delete()
    
    @commands.command()
    async def repost(self, ctx):
        msg = ctx.message

        gid = msg.guild.id
        if gid in self.reposts:
            embed, time = self.reposts[gid]
            elapsed = (msg.created_at - time).total_seconds()

            if elapsed > 18000:  # 5 hours
                raise CommandError("last game ad was too long ago!")

            await ctx.send(embed=embed)
            self.reposts[gid] = (embed, msg.created_at)
        else:
            raise CommandError("no previous game on record.")
    

    