import os
import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import asyncpraw

token = os.getenv("TOKEN")

reddit = asyncpraw.Reddit(  # reddit authentication stuff
    client_id=os.getenv("r_id"),
    client_secret=os.getenv("r_secret"),
    password=os.getenv("passwd"),
    user_agent=os.getenv("r_name"),
    username=os.getenv("usrname"),
) 

reddit.read_only = True

myComponents = ['GPU', 'HDD', 'SSD', 'PSU', 'RAM', 'NVMe']  # list of components needed
sadFlairs = ['oos', 'expired', 'sold out']  # a lot can happen in 15 min 
postList = []

bot = commands.Bot(command_prefix="!")  # discord command prefix


@bot.event
async def on_ready():
    print("Ready to find pc parts for hopefully not trash prices!")


@bot.command()
async def test(ctx):
    await ctx.send("works")


@bot.command()
async def stop(ctx):
    await bot.close() 


@bot.command()
async def top(ctx):
    subreddit1 = await reddit.subreddit("bapcsalescanada")
    async for post1 in subreddit1.new(limit=1):
        await ctx.send(post1.title)


@tasks.loop(minutes=15)  # every 15 min do the following
async def gettopfewposts():
    postList.clear()
    subreddit = await reddit.subreddit("bapcsalescanada")
    
    async for post in subreddit.new(limit=10):  # initial list
        valid = True
        f = post.link_flair_text
        if len(f) > 0: 
            f.lower()  # make lower case
            for sad in range(len(sadFlairs)):
                if f.find(sadFlairs[sad]) >= 0:  # if the flair indicates the item is no longer available
                    valid = False 
                    break                        # no point in continuing
        if valid == True:
            p = post.title
            for i in range(len(myComponents)):
                if p.find(myComponents[i]) >= 0:
                    postList.append(post.title)
                    # print(post.title)

    if len(postList) > 0:
        finalList = list(dict.fromkeys(postList))  # gets rid of accidental duplicates
        msgL = '\n'.join(finalList)
        await bot.wait_until_ready()
        update_channel = bot.get_channel(int(os.getenv("UPDATE_CHANNEL_ID")))
        await update_channel.send(msgL)


gettopfewposts.start()

bot.run(token)