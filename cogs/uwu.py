from discord.ext import commands
import random
from random import randint as rand

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

PICK_LIST = [
    419153182095179796, # bitter
    541045275310030848, # abby
]

class UwU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @staticmethod
    def convert_word(word): # Taken from https://github.com/WahidBawa/UwU-Translator
        converted = ""
        doubleT = doubleT_Presence = th_Presence = False

        for i in range(len(word)):
            if doubleT or th_Presence:
                doubleT = th_Presence = False
                continue
            elif (word[i].lower() == "l" and not doubleT_Presence) or (word[i].lower() == "r"):
                converted += "W" if word[i].isupper() else "w"
            elif (word[i].lower() == "t") and ((word[i + (1 if i + 1 < len(word) else 0)].lower() == "t")):
                converted += (("D" if word[i].isupper() else "d") + ("D" if word[i + 1].isupper() else "d")) if i + 1 < len(word) else "t"
                doubleT = doubleT_Presence = True if i + 1 < len(word) else False
            elif (word[i].lower() == "t") and ((word[i + (1 if i + 1 < len(word) else 0)].lower() == "h")):
                converted += ("F" if word[i].isupper() else "f") if i + 2 == len(word) else "t"
                th_Presence = True if i + 2 == len(word) else False
            else:
                converted += word[i]
        if len(word) > 0 and (word[0] != ":" or word[-1] != ":"):
            return ((converted[0] + "-" + converted[0:]) if (rand(1, 10) == 1 and converted[0] in ALPHABET) else converted)
        else:
            return word
    
    @staticmethod
    def convert_sentence(string):
        words = string.split(' ')
        output = ""
        for word in words:
            output += UwU.convert_word(word) + " "
        
        return output[:-1] # strip the last space
    
    @commands.Cog.listener(name="on_message")
    async def uwuify(self, msg):
        if msg.author.id == self.bot.user.id or len(msg.content) < 10:
            return

        if msg.author.id in PICK_LIST:
            if random.random() < 0.005: # about every 200 messages:
                converted = UwU.convert_sentence(msg.content)
                if converted != msg.content:
                    await msg.channel.send(converted)
        if random.random() < 0.001: # about every 1000 messages
            await msg.channel.send(UwU.convert_sentence(msg.content))

