import discord
import asyncio

client = discord.Client()
tokenfile = open("./token", "r")
token = tokenfile.readline()
tokenfile.close()

loop = asyncio.get_event_loop()

channel = None


@client.event
async def on_ready():
    global channel
    print("Ready!")
    while True:
        inp = input()
        splut = inp.split(" ")
        if splut[0].startswith("/"):
            command = splut[0][1:]
            if command == "channel":
                channel = client.get_channel(int(splut[1]))
                if channel is None:
                    print("Invalid channel.")
                else:
                    print("Set channel to #{0} in guild {1}".format(
                        channel.name, channel.guild.name))
            elif command == "stop":
                await client.logout()
                break
            else:
                print("Invalid command.")
        else:
            if channel is None:
                print("No channel to send to!")
            else:
                await channel.send(inp)


client.run(token)
