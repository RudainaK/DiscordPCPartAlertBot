# About this bot 

So, at the time of making, the GPU shortage hadn't gotten any better. As someone who's wanted a PC for a while, it was a bit frustrating to see either stuff go out of stock in like 2 minutes or be completely out of budget. So, out of frustration I programmed this bot. It looks at some of the newest posts in the subreddit /r/bapcsalescanada, and every 15 minutes sends me a message on discord with posts that have certain keywords I'm interested in (for example, GPU). It still isn't perfect, but it does a decent job. It's hosted on heroku so I don't have to run it locally, although that is also an option.

## Commands 

In addition to the every 15 minutes notification, there are a few other commands (not all are that relevant)So, all commands need to start with the '!' character. 

| Command | With proper formatting | What it does                                                     |
|---------|------------------------|------------------------------------------------------------------|
|toplink  |!toplink                |sends the current top post in the new section                     |
|GoodBot  |!GoodBot                |sends ':)' to the channel                                         |
|test     |!test                   |sends 'works' to the channel. Used to test if the bot is connected|
|stop     |!stop                   |Technically supposed to take the bot offline when updating on heroku, otherwise it crashes after restarting before starting up again due to a previously unclosed connection. Still doesn't work perfectly|

## Using the bot

If you are somewhat interested in using this bot, I recommend going over [Cameron Rodriguez's wiki](https://github.com/cam-rod/XKCDAltTextBot/wiki) for his twitter bot. Overall the process is similar with just a a few differences. I will write up a more thorough guide later. 

Note that this bot can be run locally, just replace any of the environmental variables with the actual ids/secrets/tokens and press run. 