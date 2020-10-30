from discord.ext import commands
import discord, json


def get_word_list():
    try:
        with open("words.json") as word_file:
            word_list = json.load(word_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(e)
        word_list = {}
    
    return word_list

def save_word_list(word_list):
    with open("words.json", "w") as word_file:
        json.dump(word_list, word_file)


class Scribble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="scribble-add")
    @commands.dm_only()
    async def scribble_add(self, ctx):
        msg = ctx.message

        if msg.author.dm_channel is None or msg.channel.id != msg.author.dm_channel.id:
            raise commands.CommandError("this command only works for direct messages")

        cmds = msg.content.split(" ", 1)
        if len(cmds) < 2:
            raise commands.CommandError("no words found")
        new_words = [word.strip() for word in cmds[1].split(",")]
        author_id = str(msg.author.id)

        word_list = get_word_list()

        if author_id not in word_list: #Creating an array if none exists.
            word_list[author_id] = []
        
        for word in new_words:
            word = word.strip().lower()
            if word not in word_list[author_id]:
                word_list[author_id].append(word)

        save_word_list(word_list)

        return await ctx.send("Your words were added, thank you. You can use fl!scribble-list to see "
                                    "your word list")

    @commands.group(name="scribble-list", invoke_without_subcommand=True)
    @commands.dm_only()
    async def scribble_list(self, ctx, second=None):
        for command in eval("self.scribble_list.commands"): # to suppress the wrong error......
            if command.name == second:
                return await command(ctx)

        msg = ctx.message

        if not isinstance(msg.channel, discord.DMChannel):
            raise commands.CommandError("this command only works for direct messages")

        word_list = get_word_list()

        author_id = str(msg.author.id)
        result_msg = ""

        if second is not None:
            if second in word_list: # Checks if a user ID was passed, and returns their list
                result_msg += second + ":\n"
                for i in range(len(word_list[second])):
                    result_msg += str(i+1) + ". " + word_list[second][i] + "\n"
            
            else:
                raise commands.CommandError("something went wrong. Try using `fl!scribble-list` instead")

            result_msg = result_msg if result_msg != "" else "The list is empty"
            return await ctx.send(result_msg)

        if author_id in word_list:  # List with only the author's words
            author_word_list = word_list[author_id]
            if len(author_word_list) == 0:
                result_msg = "Your word list is empty"
                word_list.pop(author_id, None)
            else:
                for i in range(len(author_word_list)):
                    result_msg += str(i + 1) + ". " + author_word_list[i] + "\n"
        else:
            result_msg = "Your word list is empty"

        return await ctx.send(result_msg.strip())

    @scribble_list.command()
    async def users(self, ctx):
        word_list = get_word_list()
        
        result_msg = ""
        for user_id in word_list:
            result_msg += user_id + ": "
            for i in range(len(word_list[user_id])):
                result_msg += word_list[user_id][i] + ", "
            result_msg = result_msg[:-2] + "\n\n"
        
        await ctx.send(result_msg.strip()) # TODO: make this send in chunks
    
    @scribble_list.command(name="full")
    async def scribble_list_full(self, ctx):
        word_list = get_word_list()
        word_array = []

        result_msg = ""
        for user_id in word_list:
            for i in range(len(word_list[user_id])):
                if word_list[user_id][i] not in word_array:
                    word_array.append(word_list[user_id][i])
        for word in word_array:
            result_msg += ", " + word
        result_msg = result_msg[2:]

        await ctx.send(result_msg.strip()) # TODO: make this send in chunks
        


    @commands.command(name="scribble-remove")
    async def scribble_remove(self, ctx):
        msg = ctx.message

        if not isinstance(msg.channel, discord.DMChannel):
            raise commands.CommandError("This command only works for direct messages")

        word_list = get_word_list()

        author_id = str(msg.author.id)
        cmds = msg.content.split(" ", 1)

        if len(cmds) < 2:
            raise commands.CommandError("Please specify which word to remove with an index given by fl!scribble_list or"
                                        " clear your whole list with fl!scribble_remove all")

        result_msg = ""
        if author_id in word_list:
            index = int(cmds[1]) - 1
            if index < 0 or index >= len(word_list[author_id]):
                raise commands.CommandError("there are no words with that index")
            removed_word = word_list[author_id].pop(index)
            if len(word_list) == 0:
                word_list.pop(author_id, None)
            result_msg = "Done! `" + removed_word + "` was removed"
        
        else: # Valid index not found, looking for keyword/subcommand
            if cmds[1] == "all":
                if word_list.pop(author_id, None) is not None:
                    result_msg = "Done! all the words in your list were removed"
                else:
                    result_msg = "You don't have a list to remove"
            elif cmds[1].startswith("users"):
                flamingos = self.bot.get_guild(765157465528336444)  # Below we verify the user is an admin of the flamingo server
                try: # fl!scribble-remove users [user_id]/clear [index]/all
                    member = flamingos.get_member(msg.author.id)
                    if member.guild_permissions.administrator:
                        sub_commands = cmds[1].split(" ")
                        if len(sub_commands) < 2:
                            raise commands.CommandError("missing arguments")
                        elif sub_commands[1] == "clear":
                            word_list = {}
                            result_msg = "All the words were removed from the list"
                        elif sub_commands[1] not in word_list:
                                result_msg = "User doesn't have a word list"
                        elif len(sub_commands) < 3:
                            raise commands.CommandError("missing argument")
                        else:
                            try:
                                user_index = int(sub_commands[2]) - 1
                                if user_index < 0 or user_index >= len(word_list[sub_commands[1]]):
                                    raise commands.CommandError("User: " + sub_commands[1] + " has no words with that index")
                                removed_word = word_list[sub_commands[1]].pop(user_index)
                                if len(word_list[sub_commands[1]]) == 0:
                                    word_list.pop(sub_commands[1], None)
                                result_msg = "Done! user: " + sub_commands[1] + "'s `" + removed_word + "` was removed"
                            except ValueError:
                                if sub_commands[2] == "all":
                                    word_list.pop(sub_commands[1])
                                    result_msg = "All the user: " + sub_commands[1] + "'s words were removed from the list"
                                else:
                                    raise commands.CommandError("invalid command")
                    else:
                        raise commands.CommandError("only Flamingo's admins can use this command")
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(e)
                    raise commands.CommandError("couldn't find member")
            else:
                raise commands.CommandError("please specify which word to remove with an index given by fl!scribble-list or"
                                        " clear your whole list with fl!scribble-remove all")

        save_word_list(word_list)
        return await ctx.send(result_msg)