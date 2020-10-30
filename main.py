from discord.ext import commands
import discord

import cogs.utils as utils

# Cogs
from cogs.among_us import AmongUs
from cogs.codenames import Codenames
from cogs.magic import Magic
from cogs.misc import Misc
from cogs.pictures import Pictures
from cogs.polls import Polls
from cogs.scribble import Scribble
from cogs.utils import Utils

cogs = [AmongUs, Codenames, Magic, Misc, Pictures, Polls, Scribble, Utils]

intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand()
bot = commands.Bot(command_prefix=["fl!", "Fl!", "fL!", "FL!"], owner_id=214732126950522880, intents=intents, help_command=help_command)
#target_channel, flamingos, logch = None, None, None

for Cog in cogs:
    bot.add_cog(Cog(bot))

@bot.event
async def on_command_error(ctx, error):
    print("encountered error: " + str(error))
    await ctx.message.add_reaction("❌")

    if type(error) == commands.CommandNotFound:
        command = ctx.message.content.split(" ")[0][len("fl!"):]
        if command == "channel":
            return
        cmds = [c.name for c in bot.commands if not c.hidden]

        closest = min(cmds, key=(lambda x: utils.distance_fast(x, command)))
        if utils.distance_fast(closest, command) < 3:
            await ctx.send("Unknown command `{0}`. Please use fl!help for reference. Perhaps you meant `{1}`?".format(command, closest))
        else:
            await ctx.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))
        if ctx.author.id == 346847827978223616:
            await ctx.send("I expected better spelling from you, ghost")
    
    elif hasattr(error, "message") and error.message != "" and error.message is not None:
        await ctx.send("Error: " + error.message)
    elif type(error) == commands.MissingRequiredArgument:
        await ctx.send("Error: missing a required argument.")
    elif type(error) == commands.UnexpectedQuoteError:
        await ctx.send("Error: unexpected quote.")
    elif type(error) == commands.ExpectedClosingQuoteError:
        await ctx.send("Error: expected a closing quote, but none was found.")
    else:
        await ctx.send("Error: " + str(error))


@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    act = discord.Activity(name="fl!help", type=discord.ActivityType.listening)
    await bot.change_presence(status=discord.Status.online, activity=act)

@bot.event
async def on_disconnect():
    print("Oops! Disconnected...")

tokenfile = open("./token", "r")
token = tokenfile.readline()
tokenfile.close()
bot.run(token)