from discord.ext import commands
import discord
import random
import requests

MSG_LIMIT = 10_000
BESTOF_ID = 775000958110400572
BESTOF_PREDICT_ID = 779752031551356948

MOVIES_ID = 792173893372215326
MOVIES_BLACKLIST = [648864666780696576, 143455480096882689]

def is_spam_channel(ch):
    return type(ch) == discord.DMChannel or ch.name.find("spam") != -1


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<num> <list... separated by commas>",
                      brief="Makes selections from a given list",
                      help="Makes a specified number of selections from a given list. Selections do not repeat.")
    async def selection(self, ctx):
        msg = ctx.message

        spliteroo = msg.content.split(" ")
        if len(spliteroo) < 3:
            raise commands.CommandError(
                "please specify a number and then a comma separated list of options")

        num = None
        try:
            num = int(msg.content.split(" ")[1])
        except:
            raise commands.CommandError("please specify a valid number.")

        if num > 1000:
            raise commands.CommandError("Number too high.")

        options = [x.strip() for x in " ".join(spliteroo[2:]).split(",")]
        choices = ", ".join(random.sample(options, num))
        embed = discord.Embed(
            title="Selected {0} out of {1} options:".format(
                num,
                len(options)
            ),
            description=choices
        )
        embed.set_footer(
            text="{0}#{1} | Yes liv, I'm a party pooper.".format(
                ctx.author.name,
                ctx.author.discriminator
            ),
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command(brief="Rolls dice.", help="Rolls dice, given in D&D notation. \
For example, to roll 2 dice of 12 sides, do fl!roll 2d12")
    async def roll(self, ctx, roll: str = "1d6"):
        sploot = roll.split("d")
        if len(sploot) != 2:
            raise commands.CommandError("Invalid input.")

        num = int(sploot[0])
        die = int(sploot[1])

        if num > 1000 or die > 1000:
            raise commands.CommandError("Numbers too high.")

        result = sum(random.choices(range(1, die+1), k=num))

        await ctx.send("Rolled {0}: `{1}`".format(roll, result))

    @commands.command(brief="Fun facts.", help="Retrieves a random fun fact from the internet.")
    async def funfact(self, ctx):
        if not is_spam_channel(ctx.channel):
            raise commands.CommandError("not a spam channel.")
        r = requests.get(
            "https://uselessfacts.jsph.pl/random.json?language=en")
        text = r.json()["text"]
        await ctx.send("Fun Fact: {0}".format(text))

    @commands.command()
    @commands.is_owner()
    async def analyze(self, ctx):
        channel = ctx.message.channel_mentions[0]
        counters = dict()

        a_msg = await ctx.send(
            "Analyzing the last (at most) {0:,} messages in <#{1}>: 0 read".format(
                MSG_LIMIT, channel.id)
        )

        i = 0
        async for msg in channel.history(limit=MSG_LIMIT):
            if i % (MSG_LIMIT//25) == 0:
                await a_msg.edit(
                    content="Analyzing the last (at most) {0:,} messages in <#{1}>: {2:,} read".format(
                        MSG_LIMIT,
                        channel.id,
                        i
                    )
                )

            id = msg.author.id
            if id not in counters:
                counters[id] = 0
            counters[id] += 1

            i += 1

        leaderboard = list(map(lambda x: (x, counters[x]), counters))
        leaderboard.sort(key=lambda x: x[1], reverse=True)

        s = i

        content = "Top 10 message senders in <#{0}> according to the last (at most) {1:,} messages:\n"\
            .format(channel.id, MSG_LIMIT)
        for i, u in enumerate(leaderboard):
            if i >= 10:
                break

            content += "{0}. <@{1}>: {2:,} messages. ({3:,.2f}%)\n".format(
                i+1,
                u[0],
                u[1],
                100*u[1]/s
            )

        embed = discord.Embed()
        embed.description = content

        await a_msg.delete()
        await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def starboard(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        msg: discord.Message = await channel.fetch_message(payload.message_id)
        reaction = None

        for r in msg.reactions:
            if r.emoji == "⭐":
                reaction = r
                break
        else:
            return

        if reaction.count < 1:
            return
        elif (msg.channel.id == BESTOF_ID or msg.channel.id == BESTOF_PREDICT_ID) and msg.author.id == self.bot.user.id:
            return

        async for user in reaction.users():
            if user.id == self.bot.user.id:
                return

        await msg.add_reaction("⭐")

        embed = discord.Embed()
        embed.add_field(
            name="Source",
            value="[Jump!]({0})".format(msg.jump_url)
        )
        if msg.author.id == 728859615898632193:  # predictabot
            prediction = msg.embeds[0]
            embed.set_author(
                name=prediction.author.name,
                icon_url=prediction.author.icon_url
            ).set_footer(
                text="This is a prediction from PredictaBot!",
                icon_url=msg.author.avatar_url
            )
            embed.description = prediction.description

            bestof = self.bot.get_channel(
                BESTOF_PREDICT_ID)  # best of predictabot
            await bestof.send(embed=embed)
        else:
            embed.set_author(
                name=msg.author.name,
                icon_url=msg.author.avatar_url
            ).set_footer(
                text="Originally posted in #{0}".format(msg.channel.name)
            )
            if len(msg.attachments) > 0:
                embed.set_image(
                    url=msg.attachments[0].url
                )
            embed.description = msg.content

            bestof = self.bot.get_channel(BESTOF_ID)  # best of flamingo
            await bestof.send(embed=embed)

    @commands.Cog.listener(name="on_message")
    async def stop_bool_mayo(self, msg: discord.Message):
        c = msg.content.lower()
        if ("bool" in c or "bewl" in c or "bol" in c) and ("mayo" in c or "moya" in c or "meyo" in c) and msg.author.id == 716584088030543972:
            await msg.delete()

    @commands.Cog.listener(name="on_message")
    async def echo(self, msg: discord.Message):
        content: str = msg.content.lower()
        words = content.split(' ')
        word_set = set(words)
        if len(word_set) == 1 and "echo" in word_set:
            echo_count = len(words)
            new_content = "<:NotLikeThis:806903084542197811>" * echo_count
            await msg.channel.send(new_content)

    @commands.Cog.listener(name="on_message")
    async def poker(self, msg: discord.Message):
        c: str = msg.content
        if c.startswith("👀"):
            if msg.author.id == 214732126950522880:  # me
                await msg.add_reaction("🛡️")
            else:
                await msg.add_reaction("✌️")
