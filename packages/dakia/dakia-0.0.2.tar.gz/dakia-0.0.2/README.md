Drop dead simple alerts and updates for every project on any platfrom!
This package lets your code send messages to you about its status.
As of now, the best option is using Telegram (other platforms will be added in the future).

Drop this into your code:


## Installation
```python
pip install dakia
```

## Usage
```python
from dakia import Dakia

tbot = Dakia(token='secret1', chatId='something2', 'StockBot')
rbot = Dakia(token='secret1', chatId='something2', 'RenderBot')

genbot = Dakia(token='secret3', chatId='something3')

# Multiple messengers for seprate tasks / projects
if win:
    tbot.dak('-alert brrr')
else:
    tbot.dak('-warning oof')

if renderComplete:
    rbot.dak('-alert 3d render is complete)

genbot.dak(f"🔥 #new-user-signup {username}")
genbot.dak(f"💵 #sale {amount}")
genbot.dak(f"🌟 #project-{projectName} deployed successfully")


genbot.dak('-warning #project-quotes-crawler : Memory usage > 80%')

```

# License
MIT License



## Extended Tutorial


## How to setup Dakia bot

There are two parts to setting up the Dakia bot
1 - The Telegram bot
2 - The python package

My goals is to keep this tutorial very brief and lean. 
For any step that may have tutorials online, I will not explain them here and instead link to YouTube or blogs that do a better job.


### The Telegram part
This is a one time setup activity. Once sorted, you dont have to bother with it ever again.
You can use the same bot for multiple projects.

Here we seek jus two things,
- The `bot token` (messages sent via this bot)
- The `chat id` (messages sent to this user/channel)

**Steps:**
#### Creating the bot
- Install, then open telegram on your phone
- Search for @BotFather, then type `/newbot`
- Select a name for your bot, in this example we use `YourAlertsBot`
- Get the token and keep it aside
#### Initializing the bot
- Search for the bot, press `Start` and message it with `hi`
- Select the 'hi' message and forward it to another bot named @jsondumpbot

Now you have two items with you, The `chat id` and the `bot token`.
With this, head over to the Python side.


### The Python part
We begin with installing package, importing the module and finally send the test message.
`pip install dakia`
Inside our code file--
```
from dakia import Dakia
BOT_TOKEN = '<your bot token>'
CHAT_ID = '<your chat id>'
PROJECT = '<your project name>'
pm = Dakia(BOT_TOKEN, CHAT_ID, PROJECT)


pm.dak('-update Its Alive!')
```

That's it. Now for any number of alerts, simply type `pm.dak('-someFlag hi mom!')` and the message is sent to you.


