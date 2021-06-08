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
postList = []

bot = commands.Bot(command_prefix="!")  # discord command prefix


@bot.event
async def on_ready():
    print("Ready to find pc parts for hopefully not trash prices!")

while True: 
    @bot.command()
    async def test(ctx):
        await ctx.send("works")


    @bot.command()
    async def stop(ctx):
        await bot.close()
        break


    @bot.command()
    async def top(ctx):
        subreddit1 = await reddit.subreddit("bapcsalescanada")
        async for post1 in subreddit1.new(limit=1):
            print(post1.title)
            await ctx.send("ha")
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
            bot.wait_until_ready()
            print("test, id: ", int(os.getenv("UPDATE_CHANNEL_ID")))
            print("id before cast is of type: ", type(os.getenv("UPDATE_CHANNEL_ID")))
            print("id before cast is of type: ", type(int(os.getenv("UPDATE_CHANNEL_ID"))))
            update_channel = bot.get_channel(int(os.getenv("UPDATE_CHANNEL_ID")))
            print("update channel is type: ", type(update_channel))
            await update_channel.send(msgL)


    gettopfewposts.start()

    bot.run(token)