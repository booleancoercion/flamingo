import discord.ext.commands as commands
import discord, re, asyncio
import commands_old

# Cogs
from cogs.among_us import AmongUs

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="fl!", intents=intents)
#target_channel, flamingos, logch = None, None, None

bot.add_cog(AmongUs(bot))
bot.add_cog()

@bot.event
async def on_command_error(ctx, error):
    await ctx.message.add_reaction("❌")
    await ctx.send("Error: " + error.message)

@bot.event
async def on_ready():
    print("Logged in as", bot.user)
    #global flamingos, logch
    #flamingos = client.get_guild(765157465528336444)
    #logch = client.get_channel(768464621031653497)
    
    act = discord.Activity(name="fl!help", type=discord.ActivityType.listening)
    await bot.change_presence(status=discord.Status.online, activity=act)

@bot.event
async def on_disconnect():
    print("Oops! Disconnected...")

@bot.event
async def on_message(msg):
    if msg.author.bot: # ignore messages by bots
        return

    msglst = msg.content.lower().split(" ")

    if msglst[0].startswith("fl!"):
        command = msglst[0][3:]
        cmds = list(commands_old.reg.keys())
        if command in cmds:
            await commands_old.reg[command](msg)
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
        else:
            closest = min(cmds, key=(lambda x: commands_old.distance_fast(x, command)))
            if commands_old.distance_fast(closest, command) < 3:
                await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference. Perhaps you meant `{1}`?".format(command, closest))
            else:
                await msg.channel.send("Unknown command `{0}`. Please use fl!help for reference.".format(command))
            if msg.author.id == 346847827978223616:
                await msg.channel.send("I expected better spelling from you, ghost")
        return
    
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