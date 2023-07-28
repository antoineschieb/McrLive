from discord.ext import tasks, commands
import discord
from discord.ext import tasks
from private import TOKEN


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

cogs=[]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        c = MyCog()
        cogs.append(c)
    
    if message.content.startswith('$bye'):
        await message.channel.send('Bye!')
        for c in cogs:
            c.cog_unload()
        


class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=20.0)
    async def rec_wait_stop_pred_stop(self):
        print(self.index)
        self.index += 1

client.run(TOKEN)