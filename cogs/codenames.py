from discord.ext import commands
import discord, random

def find_role(lst, role_name):
    role_name = role_name.lower()
    for role in lst:
        if role.name.lower().find(role_name) != -1:
            return role

def remove_duplicate_snowflakes(lst):
    ids = set()
    def func(x):
        if x.id in ids:
            return False
        ids.add(x.id)
        return True
    return list(filter(func, lst))

class Codenames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.codenames_timeout = None
    
    @commands.command(name="codenames-teams")
    async def codenames(self, ctx, members=None):
        msg = ctx.message

        if self.codenames_timeout != None:
            if (msg.created_at - self.codenames_timeout).total_seconds() < 60:
                pass
        self.codenames_timeout = msg.created_at

        roles = msg.guild.roles
        red_spy = find_role(roles, "red spy")
        blue_spy = find_role(roles, "blue spy")

        if type(members) != list:
            members = list()
        
        members.extend(msg.mentions)

        first_space = msg.content.find(" ")
        if first_space != -1:
            names = msg.content[first_space+1:].split(",")
            for name in names:
                result = msg.guild.get_member_named(name.strip())
                if result != None:
                    members.append(result)
        
        members = remove_duplicate_snowflakes(members)
        random.shuffle(members)

        midpoint = len(members)//2
        red_team = members[:midpoint]
        blue_team = members[midpoint:]

        output_red = "**Red Team:**"
        for member in red_team:
            if member in blue_spy.members:
                await member.remove_roles(blue_spy, reason="Codenames teaming")
            await member.add_roles(red_spy, reason="Codenames teaming")
            output_red += "\n<@{}>".format(member.id)
        
        output_blue = "**Blue Team:**"
        for member in blue_team:
            if member in red_spy.members:
                await member.remove_roles(red_spy, reason="Codenames teaming")
            await member.add_roles(blue_spy, reason="Codenames teaming")
            output_blue += "\n<@{}>".format(member.id)
        
        await ctx.send(output_red)
        await ctx.send(output_blue)
        
    @commands.command(name="codenames-over")
    async def codenames_over(self, ctx):
        msg = ctx.message

        roles = msg.guild.roles
        red_spy = find_role(roles, "red spy")
        blue_spy = find_role(roles, "blue spy")

        for member in red_spy.members:
            await member.remove_roles(red_spy, reason="Codenames over")
        
        for member in blue_spy.members:
            await member.remove_roles(blue_spy, reason="Codenames over")
        
        await msg.add_reaction("✅")

    @commands.command(name="codenames-shuffle")
    async def codenames_shuffle(self, ctx):
        roles = ctx.guild.roles
        red_spy = find_role(roles, "red spy")
        blue_spy = find_role(roles, "blue spy")
        members = red_spy.members + blue_spy.members

        return await self.codenames(ctx, members=members)