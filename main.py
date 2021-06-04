import os
import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import asyncpraw

token = os.getenv("TOKEN")

reddit = asyncpraw.Reddit(  # reddit authentication stuff
    client_id='r_id',
    client_secret='r_secret',
    user_agent='<r_name:1.0>',
    password='passwd',
    username='bot_name'
)


myComponents = ['GPU', 'HDD', 'SSD', 'PSU', 'RAM', 'NVMe']  # list of components needed
subreddit = reddit.subreddit("bapcsalescanada")
postList = []

bot = commands.Bot(command_prefix="-")  # discord command prefix

timeStart = datetime.datetime.now()
currTime = datetime.datetime.now()
newPost = False


@bot.event
async def on_ready():
    print("Ready to find pc parts for hopefully not trash prices!")


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
        p = post.title
        for i in range(len(myComponents)):
            if p.find(myComponents[i]) >= 0:
                postList.append(post.title)
                # print(post.title)

    if len(postList) > 0:
        finalList = list(dict.fromkeys(postList))  # gets rid of accidental duplicates
        msgL = '\n'.join(finalList)
        update_channel = bot.get_channel(UPDATE_CHANNEL_ID)
        await update_channel.send(msgL)

gettopfewposts()

bot.run(token)