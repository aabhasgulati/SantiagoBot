# bot.py
import os
import random
from discord.utils import get
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#define a ssubclass and work with the subclass?

bot = commands.Bot(command_prefix='!')

allguild_status = {}
reactions = ["👍", "👎"]

@bot.event # Modify this to look better!
async def on_ready():
    for guild in bot.guilds:
        temp  = {}
        for channel in guild.channels:
            if channel.name == "discussion-1":
                temp[channel.id]  = True
            if channel.name == "discussion-2":
                temp[channel.id] = True
            if channel.name == "discussion-3":
                temp[channel.id] = True
        allguild_status[guild.id] = temp
    print(allguild_status)


@bot.command(name='thread')
async def create_thread(ctx):
    guild = ctx.message.guild
    guild_status = allguild_status[guild.id] 
    await ctx.message.add_reaction("👍")

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '👍'
    try:
        await bot.wait_for('reaction_add',check=check,timeout=120.0)
    
    except asyncio.TimeoutError:
        await ctx.send('👎') 

    else:
        for channel_id,val in guild_status.items():
            if val == True:
                print(channel_id)
                channel = bot.get_channel(channel_id)
                guild_status[channel_id] = False
                break

        response = ctx.message.content[7:]
        user = ctx.message.author
        try:
            image = ctx.message.attachments[0].url
            url = ctx.message.jump_url
            cross = await channel.send("This is the starting point of the discussion for the this awesome question by {user} - **{response}** \n {url}".format(response=response,url=url,user=user.mention))
            await channel.send(image)
            url_cross = cross.jump_url
            await ctx.send("The discussion for this question has been initiated in <#{channelID}> \n {link}".format(name=channel.id,link=url_cross))

        except IndexError:
            url = ctx.message.jump_url
            cross = await channel.send("This is the starting point of the discussion for the this awesome question by {user} - **{response}** \n {url}".format(response=response,url=url,user=user.mention))
            url_cross = cross.jump_url
            await ctx.send(f"The discussion for this question has been started in <#{channel.id}> \n {url_cross}")



@bot.command('end')
async def end_thread(ctx):
    guild = ctx.message.guild
    guild_status = allguild_status[guild.id] 
    def channel_check(message):
        return guild_status[message.channel.id] == True
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
        await ctx.send("**This thread of discussion ends here! You all can take a break now! **")
        channel = ctx.message.channel
        guild_status[channel.id] = True


bot.run(TOKEN)