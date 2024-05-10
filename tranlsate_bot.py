import os
from dotenv import load_dotenv
import discord
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.members = True

translator = Translator()
class CustomClient(discord.Client):
    def __init__(self, intents):
        super(CustomClient, self).__init__(intents=intents)
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    async def on_message(self, message):
        if message.content.startswith("!id"):
            await self.find_id(message)
        if message.content.startswith("!translate"):
            try:
                #print(message.content)
                #print(message.content.split(), message.content.split()[1], message.content.split()[2])
                await self.translate(message)
            except (IndexError, ValueError):
                await message.reply(embed = discord.Embed(title = "WRONG STRUCTURE", description="The right way to write the command:"+"\n"+"`!translate <word or sentence> <language code>`", colour=discord.Colour.blue()))
                await self.show_list(message)
        if message.content.startswith("!lang-list"):
            await self.show_list(message)        
        if message.content.startswith("!help"):
            await self.help(message)
                
    async def translate(self, message):
        result = message.content.split()
        result.pop(0)
        lang = result[len(result) - 1]
        result.pop(len(result)-1)
        translate = " ".join(result)
        #print(lang, "\n", translate)
        word = translator.translate(translate, dest=lang.lower())
        await message.reply(embed=discord.Embed(description=translate + " (" + word.src + ")"+ "-" +"***" + word.text + "***"+ "(" + word.dest + ")", colour=discord.Colour.orange()))
    async def show_list(self, message):
        await message.reply(embed = discord.Embed(description = "*You can find all the language codes below:*" + "\n",colour = discord.Colour.red()))#File where all the language codes are shown
        await message.channel.send(file=discord.File("langs.txt"))
    async def help(self, message):
        await message.channel.send(embed = discord.Embed(title="***COMMANDS***", description="`!translate <word or sentence> <language code>`" + "\n" + "Translates a word or a sentence to a specific language" + "\n" + "`!lang-list`" + "\n" + "Shows all the language codes that are used in `!translate`", colour = discord.Colour.green()))
    async def find_id(self, message):
        print(message.content.split()[1])
        await message.channel.send(message.content.split()[1][2:-1])
client = CustomClient(intents=intents)
client.run(TOKEN)#My discord bot's token is stored in a sepparate file
