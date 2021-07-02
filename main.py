import os
from typing import final
import discord
from discord.embeds import Embed
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

# TO-DO:
# Change 15 min updates to 15 min specific updates
# Add 'general hourly update' that does the old 15 min function but every hour 
# update both so that they send embedded links instead of just post titles
# add a general !check ____ function that looks at the top 10 posts and sees if the provided ____ 
#keyword is there 

RAM_parameters = ['CL16', '2x8GB', '3600 MHz']
GPU_parameters = ['3060 Ti']
SSD_parameters = ['500GB', 'NVMe']


myComponents = ['GPU', 'HDD', 'SSD', 'PSU', 'RAM', 'MOBO']  #general list of components needed
sadFlairs = ['oos', 'expired', 'sold out']  # a lot can happen in 15 min 
postList = []
postListS = []

bot = commands.Bot(command_prefix="!")  # discord command prefix


@bot.event
async def on_ready():
    print("Ready to find pc parts for hopefully not trash prices!")


@bot.command()
async def help(ctx):
    await ctx.send("Hello!\nThe command prefix is '!'\nHere is a list of commands that may be helpful:\nhelp: gives info on commands\ntoplink: returns top post in new\ncheck: searches for posts with a given keyword\nGoodBot: I respond with a :)\n\nNote that I return embedded links\n\nThere are also two background processes that check for selected keywords every hour (a general search) and one every 15 minutes (specific)")  # there is probably a better way to format this


@bot.command()
async def GoodBot(ctx):
    await ctx.send(":)")


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


@bot.command()
async def toplink(ctx):
    subredditT = await reddit.subreddit("bapcsalescanada")
    embeddedLink = discord.Embed()
    async for postT in subredditT.new(limit=1):
        embeddedLink.url = postT.url
        embeddedLink.title = postT.title
        await ctx.send(embed=embeddedLink)


# @bot.command()
# async def check(ctx, arg):
#     subreddit2 = await reddit.subreddit("bapcsalescanada")
#     async for post2 in subreddit2.new(limit=10):  # check the first 10 posts in new with keyword
#         p = post2.title


@tasks.loop(minutes=3)  # every hour do the following
async def Generalgettopfewposts():
    postList.clear()
    subreddit = await reddit.subreddit("bapcsalescanada")
    
    async for post in subreddit.new(limit=10):  # initial list
        valid = True
        f = post.link_flair_text
        if f != None: 
            f.lower()  # make lower case
            print(f)  # for testing 
            for sad in range(len(sadFlairs)):
                if f.find(sadFlairs[sad]) >= 0:  # if the flair indicates the item is no longer available
                    valid = False 
                    break                        # no point in continuing
        if valid == True:
            p = post
            for i in range(len(myComponents)):
                if p.find(myComponents[i]) >= 0:
                    postList.append(str(post.id))  # storing post by id 
                    # print(post.title)

    if len(postList) > 0:
        finalList = list(dict.fromkeys(postList))  # gets rid of accidental duplicates
        for finalPost in range(len(finalList)):
            await bot.wait_until_ready()
            update_channel = bot.get_channel(int(os.getenv("UPDATE_CHANNEL_ID")))
            embeddedPostG = discord.Embed()
            postInf = reddit.submission(id = finalPost)
            embeddedPostG.title = postInf.title
            embeddedPostG.url = postInf.url
            await update_channel.send(embed=embeddedPostG)


# @tasks.loop(minutes=15)  # every 15 do the following
# async def Specificgettopfewposts():
#    postListS.clear()
#    subreddit = await reddit.subreddit("bapcsalescanada")
    
#    async for post in subreddit.new(limit=10):  # initial list
#        valid = True
#        fS = post.link_flair_text
#        if fS != None: 
#            fS.lower()  # make lower case
#            for sad in range(len(sadFlairs)):
#                if fS.find(sadFlairs[sad]) >= 0:  # if the flair indicates the item is no longer available
#                    valid = False 
#                     break                        # no point in continuing
#       if valid == True:
#           p = post.title
#            for i in range(len(myComponents)):
#                if p.find(myComponents[i]) >= 0:
#                    postListS.append(post.title)
                    # print(post.title)

#    if len(postList) > 0:
#        finalListS = list(dict.fromkeys(postListS))  # gets rid of accidental duplicates
#        msgLS = '\n'.join(finalListS)
#        await bot.wait_until_ready()
#        update_channel = bot.get_channel(int(os.getenv("QUARTERLY_CHANNEL_ID")))
#        await update_channel.send(msgLS)


Generalgettopfewposts.start()

bot.run(token)