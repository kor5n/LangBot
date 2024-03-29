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
        if message.content.startswith("!translate"):
            try:
                print(message.content)
                print(message.content.split(), message.content.split()[1], message.content.split()[2])
                await self.translate(message)
            except (IndexError, ValueError):
                await message.channel.send(embed = discord.Embed(title = "WRONG STRUCTURE", description="The right way to write the command:"+"\n"+"**!translate <word or sentence> <language code>**", colour=discord.Colour.blue())
                                            )
                await message.channel.send(embed = discord.Embed(description = "*Here you can find all the language codes:*" + "\n",colour = discord.Colour.red()))#File where all the language codes are shown
                await message.channel.send(file=discord.File("langs.txt"))                            
                
                
    async def translate(self, message):
        result = message.content.split()
        result.pop(0)
        lang = result[len(result) - 1]
        result.pop(len(result)-1)
        translate = " ".join(result)
        print(lang, "\n", translate)
        word = translator.translate(translate, dest=lang.lower())
        await message.channel.send(embed=discord.Embed(description=translate + " (" + word.src + ") - " + word.text + " (" + word.dest + ")", colour=discord.Colour.orange()))

client = CustomClient(intents=intents)
client.run(TOKEN)#My discord bot's token is stored in a sepparate file