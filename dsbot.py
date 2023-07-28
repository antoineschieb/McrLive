import random
import string
import asyncio
import datetime
import discord
import pandas as pd
import tempfile
import os
from os import listdir
from os.path import isfile, join
import logging

from private import GUILD_IDS, LOGS_CHANNEL_ID, TOKEN
logging.basicConfig(level=logging.INFO)

from discord.ext import tasks, commands
from discord.sinks.errors import RecordingException

from uncorrupt import convert_folder
from compute import send_text_asap_from_onlyfiles
from create_pp import get_pic


intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    
    if message.content.startswith('$ping'):
        await message.channel.send('pong')


class MyCog(commands.Cog):
    def __init__(self, ctx, language):
        self.index = 0
        self.ctx = ctx
        self.language = language
        self.ticker.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=9.0)
    async def ticker(self):
        await rec(self.ctx, self.language)


async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):  # Our voice client already passes these in.
    
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    
    tmpdirname = args[0]
    ctx = args[1]
    language = args[2]
    dt = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    os.mkdir(tmpdirname)
    # write corrupted files
    for user_id, audio in sink.audio_data.items():
        with open(f"{tmpdirname}/{dt}_{user_id}.{sink.encoding}", 'wb') as f:
            f.write(audio.file.read())
    
    
    try:
        print(datetime.datetime.now())
        # uncorrupt them
        convert_folder(tmpdirname)
        
        
    except Exception as e:
        print('couldnt uncorrupt dir :::')
        raise(e)
    
    # onlyfiles = [f for f in listdir(tmpdirname) if isfile(join(tmpdirname, f) and f.startswith('unc_'))]
    onlyfiles = listdir(tmpdirname)
    print(f"onlyfiles: {onlyfiles}")

    audio_chunks_dir = tmpdirname+'/audio_chunks_dir'
    os.mkdir(audio_chunks_dir)

    long_task = asyncio.create_task(send_text_asap_from_onlyfiles(onlyfiles, audio_chunks_dir, tmpdirname, language, bot, channel, ctx))
    await long_task
    


connections = {}
c = None

@bot.slash_command(GUILD_IDS)
async def join_voc(ctx, language='fr-FR'):  # If you're using commands.Bot, this will also work.
    global c
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("pas dans un voc", delete_after=3)
    else:
        await ctx.respond(f"Connexion au voc {voice.channel.name}", delete_after=3)
        vc = await voice.channel.connect()  # Connect to the voice channel the author is in.
        connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.
        c = MyCog(ctx, language)


@bot.slash_command(GUILD_IDS)
async def pp_tier_list(ctx):  # If you're using commands.Bot, this will also work.
    global c
    await ctx.respond(f"aaa", delete_after=3)
    members = ctx.guild.members
    
    for member in members:
        try:
            n = member.name
            url = member.avatar
            get_pic(url, n)
            await ctx.channel.send(file=discord.File('./pp/'+n+'.png'))
        except:
            print(f"Failed for {member}")
            await ctx.respond(f"Failed for {member}")
    
    # vc = await voice.channel.connect()  # Connect to the voice channel the author is in.
    # connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.
    # c = MyCog(ctx, language)




async def rec(ctx, language):     
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        try:
            vc.start_recording(
                discord.sinks.WaveSink(),  # The sink type to use.
                once_done,  # What to do once done.
                ctx.channel,  # The channel to disconnect from.
                '/tmp/'+''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                ctx,
                language,
            )
        except Exception as e:
            pass

        await asyncio.sleep(8)

        try:
            vc.stop_recording()  # Stop recording, and call the callback (once_done).
            print('stopped.')
        except RecordingException as e:
            print(e)
        # del connections[ctx.guild.id]  # Remove the guild from the cache.
        # await ctx.delete()  # And delete.
        # await ctx.respond("yep I confirm it was successful. Recording once again!")
        # await rec(ctx, first_time=False)
    else:
        await ctx.respond("pas en train de rec", delete_after=3)  # Respond with this if we aren't recording.



@bot.slash_command(GUILD_IDS)
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        # del connections[ctx.guild.id]  # Remove the guild from the cache.
        # await ctx.delete()  # And delete.
        await ctx.respond("successfully stopped recording.", delete_after=3)
    else:
        await ctx.respond("not recording here", delete_after=3)  # Respond with this if we aren't recording.


@bot.slash_command(GUILD_IDS)
async def get_logs_text(ctx):  # If you're using commands.Bot, this will also work.
    global c


    chan_logs = bot.get_channel(LOGS_CHANNEL_ID)

    print("start")
    df = pd.DataFrame(columns=["timestamp","author","content"])
    messages = await chan_logs.history(limit=63000).flatten()
    for m in messages:
        emb = m.embeds
        if len(emb)!=1:
            continue
        txt_content = emb[0].to_dict()['description']
        if "voice channel" in txt_content:
            timestmp = emb[0].timestamp
            author_name = emb[0].to_dict()['author']['name']
            df.loc[len(df), :] = [timestmp, author_name, txt_content]
            
    print(df)
    print("done")
    df.to_csv("tilio_full.csv")


@bot.slash_command(GUILD_IDS)
async def get_uuid_list(ctx):  # If you're using commands.Bot, this will also work.
    L = []
    for member in ctx.guild.members:
        L.append(member.id)
    print(L)

bot.run(TOKEN)
