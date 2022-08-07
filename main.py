

from http import client

from lib2to3.pgen2.token import AWAIT

from multiprocessing.connection import answer_challenge
from pydoc import describe
from turtle import title
from unicodedata import name

import discord
from discord.ext import commands

from discord.utils import get
from discord import FFmpegAudio
from youtube_dl import YoutubeDL

#client = discord.Client()

# // ประกาศตัวแปล Command 
bot = commands.Bot(command_prefix='//',help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# คำสั่ง Help 

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Turtorial Bot help",description="All available bot commands",color=0xE041A0)
    embed.add_field(name="//help", value="Get help command.",inline=False)
    embed.add_field(name="//test", value="Respond message that your send.",inline=False)
    embed.add_field(name="//play", value="play music form youtube.",inline=False)
    embed.add_field(name="//stop", value="stop the music.",inline=False)
    embed.add_field(name="//pause", value="pause the music.",inline=False)
    embed.add_field(name="//resume", value="resume the music.",inline=False)
    embed.add_field(name="//leave", value="leave the bot.",inline=False)
    embed.add_field(name="Don't follow your deam just follow Fayaht.", value="twitch.tv/fayaht" ,inline=False) 
    embed.set_thumbnail(url='https://scontent.fbkk13-2.fna.fbcdn.net/v/t39.30808-6/249233951_427467669010204_40482199689350937_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeFJHa9iAln4k8wcdcgcu8R3YBO_m3tNO1xgE7-be007XAoz6rNRk6n9EIIoDAY3rKN0BSFYMFvZvmr1frkRTTP1&_nc_ohc=orZ25YD3lJIAX-vTQMx&_nc_zt=23&_nc_ht=scontent.fbkk13-2.fna&oh=00_AT98nm4Rz8tyHBnj0gQH07CuBuUf3jbKirWB0lOikZGllA&oe=62F0DF7F')
    embed.set_footer(text='Fayaht', icon_url='https://scontent.fbkk13-2.fna.fbcdn.net/v/t39.30808-6/249233951_427467669010204_40482199689350937_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeFJHa9iAln4k8wcdcgcu8R3YBO_m3tNO1xgE7-be007XAoz6rNRk6n9EIIoDAY3rKN0BSFYMFvZvmr1frkRTTP1&_nc_ohc=orZ25YD3lJIAX-vTQMx&_nc_zt=23&_nc_ht=scontent.fbkk13-2.fna&oh=00_AT98nm4Rz8tyHBnj0gQH07CuBuUf3jbKirWB0lOikZGllA&oe=62F0DF7F')
    await ctx.channel.send(embed=embed)


@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice_clinet = get(bot.voice_clients, guild=ctx.guild)
    urlreadline = ctx.author.channel()

    if voice_clinet == None:
        print("Joined!") 
        await channel.connect()
        voice_clinet = get(bot.voice_clients, guild=ctx.guild)
        embed = discord.Embed(title='Play', descriptinon="test",color=0xE041A0)
        embed.insert_field_at({0},urlreadline , value='Now playing', inline=True)
        embed.add_field(name='stop music',value='use :arrow_forward: to stop music',inline=False)
        await ctx.channel.send(embed=embed)
        
                
    VDL_opl =  {'format' : 'bestaudio', 'noplaylist' : 'True'} 
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if not voice_clinet.is_playing():
        with YoutubeDL(VDL_opl) as ydl:
          info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice_clinet.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS))
        voice_clinet.is_playing()
    else :
        await ctx.channel.send("Already playing song")
        return    


@bot.command()
async def stop(ctx):
    voice_clinet = get(bot.voice_clients, guild=ctx.guild)
    if voice_clinet == None:
        await ctx.channel.send("Bot is not connected to vc")
        return

    if voice_clinet.channel != ctx.author.voice.channel:
        await ctx.channel.send("The bot is currentiy connected to {0}".format(voice_clinet.channel))
        return
    
    voice_clinet.stop()        


@bot.command()
async def pause(ctx):
    voice_clinet = get(bot.voice_clients, guild=ctx.guild)
    if voice_clinet == None:
        await ctx.channel.send("Bot is not connected to vc")
        return

    if voice_clinet.channel != ctx.author.voice.channel:
        await ctx.channel.send("The bot is currentiy connected to {0}".format(voice_clinet.channel))
        return
    
    voice_clinet.pause()        


@bot.command()
async def resume(ctx):
    voice_clinet = get(bot.voice_clients, guild=ctx.guild)
    if voice_clinet == None:
        await ctx.channel.send("Bot is not connected to vc")
        return

    if voice_clinet.channel != ctx.author.voice.channel:
        await ctx.channel.send("The bot is currentiy connected to {0}".format(voice_clinet.channel))
        return
    
    voice_clinet.resume()    

 
 # message ปกติ + str 

@bot.event #async/await
async def on_message(message):

    if message.content == "Logout":
        print(message.channel)
        await message.channel.send('Bye Bye')
        await bot.logout()

@bot.command()
async def dc(ctx):
    await ctx.voice_client.disconnect()



#---------------------------------------------------------------
#bot = commands.bot(commands_prefix = '!')

#@bot.event
#async def pause(ctx):
    #await play()
    #embed = discord.Embed(title='Test', descriptinon="All available bot commands",color=0xE041A0)
    #embed.add_field(name='Play music',value='use ▶ to play music')

    #msg = await ctx.send(embed=embed)

    #await msg.add_reaction


#@bot.command
#async def on_reaction_add(reaction,user):

#---------------------------------------------------------------


bot.run('')
