import os
import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import praw

token = os.getenv("TOKEN")

reddit = praw.Reddit(  # reddit authentication stuff
    client_id='r_id',
    client_secret='r_secret',
    user_agent='<r_name:1.0>'
)


def gettopost():
    for post1 in subreddit.new(limit=10):
        return post1.title


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
    topPost = gettopost()
    await ctx.send(topPost)


@tasks.loop(minutes=15)  # every 15 min do the following
async def gettopfewposts():
    postList.clear()
    for post in subreddit.new(limit=10):  # initial list
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