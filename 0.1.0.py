# bot.py
import os
import random
from discord.utils import get
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='test')
async def test(ctx):
    await ctx.send('WTF')

channel_names = ["discussion-1","discussion-2","discussion-3"]

channel_disc = {}
reactions = ["👍", "👎"]
discussion_channels = {1:True,2:True,3:True}

@bot.event # Modify this to look better!
async def on_ready():
    id = 757250530551660585
    guild = bot.get_guild(id)
    print(guild.name)
    for channel in guild.channels:
        if channel.name == "discussion-1":
            channel_disc[channel.id]  = True
        if channel.name == "discussion-2":
             channel_disc[channel.id] = True
        if channel.name == "discussion-3":
             channel_disc[channel.id] = True
    print(channel_disc)

@bot.command(name='thread')
async def create_thread(ctx):
    await ctx.message.add_reaction("👍")

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '👍'
    try:
        await bot.wait_for('reaction_add',check=check,timeout=120.0)
    
    except asyncio.TimeoutError:
        await ctx.send('👎') 

    else:
        for channel_id,val in channel_disc.items():
            if val == True:
                print(channel_id)
                channel = bot.get_channel(channel_id)
                channel_disc[channel_id] = False
                break

        response = ctx.message.content[7:]
        user = ctx.message.author
        try:
            image = ctx.message.attachments[0].url
            url = ctx.message.jump_url
            cross = await channel.send("This is the start of the discussion in regards to the question by {user} - **{response}** \n {url}".format(response=response,url=url,user=user.mention))
            await channel.send(image)
            url_cross = cross.jump_url
            await ctx.send("The discussion regarding this question has been started in <#{channelID}> \n {link}".format(name=channel.id,link=url_cross))

        except IndexError:
            url = ctx.message.jump_url
            cross = await channel.send("This is the start of the discussion in regards to the question, by {user} - **{response}** \n {url}".format(response=response,url=url,user=user.mention))
            url_cross = cross.jump_url
            await ctx.send(f"The discussion regarding this question has been started in <#{channel.id}> \n {url_cross}")



@bot.command('end')
async def end_thread(ctx):
    def channel_check(message):
        return channel_disc[message.channel.id] == True
    if channel_check(ctx.message) == False :  
        await ctx.message.add_reaction("👍")
    else:
        await ctx.send("There is no ongoing discussion in this channel")
        return 

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '👍'
    try:
        await bot.wait_for('reaction_add',check=check,timeout=60.0)
    
    except asyncio.TimeoutError:
        await ctx.send('👎') 
    else:
        await ctx.send("**This is the end of the discussion in this channel!**")
        channel = ctx.message.channel
        channel_disc[channel.id] = True


bot.run(TOKEN)