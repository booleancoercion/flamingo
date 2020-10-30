import discord.ext.commands as commands
import discord, re, asyncio

from discord.ext.commands.errors import MissingRequiredArgument
import commands_old
import cogs.utils as utils

# Cogs
from cogs.among_us import AmongUs
from cogs.utils import Utils

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="fl!", owner_id=214732126950522880, intents=intents, help_command=None)
#target_channel, flamingos, logch = None, None, None

bot.add_cog(AmongUs(bot))
bot.add_cog(Utils(bot))

@bot.event
async def on_command_error(ctx, error):
    print("encountered error: " + str(error))
    await ctx.message.add_reaction("❌")

    if type(error) == commands.CommandNotFound:
        command = ctx.message.content.split(" ")[0][len("fl!"):]
        old_commands = list(commands_old.reg.keys())
        new_commands = [c.name for c in bot.commands]
        if command in old_commands:
            return
        
        cmds = [*old_commands, *new_commands]
        closest = min(cmds, key=(lambda x: utils.distance_fast(x, command)))
        if utils.distance_fast(closest, command) < 3:
            await ctx.send("Unknown command `{0}`. Please use fl!help for reference. Perhaps you meant `{1}`?".format(command, closest))
        else:
            await ctx.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))
        if ctx.author.id == 346847827978223616:
            await ctx.send("I expected better spelling from you, ghost")
    
    elif "message" in dir(error):
        await ctx.send("Error: " + error.message)
    elif type(error) == commands.MissingRequiredArgument:
        await ctx.send("Error: missing a required argument.")
    elif type(error) == commands.UnexpectedQuoteError:
        await ctx.send("Error: unexpected quote.")
    elif type(error) == commands.ExpectedClosingQuoteError:
        await ctx.send("Error: expected a closing quote, but none was found.")


@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    #global flamingos
    #flamingos = client.get_guild(765157465528336444)
    act = discord.Activity(name="fl!help", type=discord.ActivityType.listening)
    await bot.change_presence(status=discord.Status.online, activity=act)

@bot.event
async def on_disconnect():
    print("Oops! Disconnected...")

#@bot.event
@bot.listen(name="on_message")
async def old_commands(msg):
    if msg.author.bot: # ignore messages by bots
        return

    msglst = msg.content.lower().split(" ")

    if msglst[0].startswith("fl!"):
        command = msglst[0][3:]
        cmds = list(commands_old.reg.keys())
        if command in cmds:
            await commands_old.reg[command](msg)
        elif command in [c.name for c in bot.commands]:
            pass
        #elif command == "channel":
        #    if msg.author.id != 214732126950522880:
        #        return await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))
        #
        #    ch_id = int(msglst[1])
        #    for channel in flamingos.text_channels:
        #        if channel.id != ch_id:
        #            continue
        #        global target_channel
        #        target_channel = channel
        #        break
    
    #matches = sub_reg.finditer(msg.content)
    #await commands.subreddit(msg, matches)

    #if msg.channel.id == 766265768295399424 and msg.author.id == 214732126950522880 and target_channel != None:
    #    async with target_channel.typing():
    #        await asyncio.sleep(0.3)
    #        await target_channel.send(msg.content)

tokenfile = open("./token", "r")
token = tokenfile.readline()
tokenfile.close()
bot.run(token)