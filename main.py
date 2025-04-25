import discord
import os
from dotenv import load_dotenv
load_dotenv()  # reads .env into os.environ


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# client =  discord.Client()

#we are creating certain functions for discord bot to respond to 
# these function names are actually from the discord.py library 
# it is looking specifically for these function names

# This is an event executed as soon as the bot is ready and working
@client.event
async def on_ready(): 
    print("We have logged in as {0.user}".format(client))


#event triggered if it senses a message in the discord server
# args: message
@client.event
async def on_message(message):
# this on mesage eveent triggers each time a message is recieved
# we dont want our bot to trigger it for its own messages
    if message.author == client.user:
        return
    
    # if message starts with a command thats being sent to our bot
    # we can make up commads for our bot
    # lets say for our bot all commands start with $
    if message.content.startswith("$hello"):
        # to return a message back to discord
        await message.channel.send("Hello!")

# to run the bot 
# we need to pass the token to the run command
# token is stored in the env file
token = os.getenv("TOKEN")
if not token:
    raise RuntimeError("Missing TOKEN environment variable")
client.run(token)
