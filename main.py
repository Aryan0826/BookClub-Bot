import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()  # reads .env into os.environ


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "$", intents = intents)

verificationCodes = {} # Store verification codes: user_id -> verification code

#we are creating certain functions for discord bot to respond to 
# these function names are actually from the discord.py library 
# it is looking specifically for these function names

# This is an event executed as soon as the bot is ready and working
@bot.event
async def on_ready(): 
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    welcomeChannelID = int(os.getenv("WELCOME_CHANNEL_ID",0))
    if welcomeChannelID:
        welcomeChannel = bot.get_channel(welcomeChannelID)
        if welcomeChannel:
            await welcomeChannel.send(f"Welcome {member.mention}! To access the server, please verify yourself by typing "
                f"`$verify` in this channel. I'll send you a direct message with instructions.")

@bot.command(name = "hello")
async def hello(ctx):
    await ctx.send("Hello!")    

# to run the bot 
# we need to pass the token to the run command
# token is stored in the env file
token = os.getenv("TOKEN")
if not token:
    raise RuntimeError("Missing TOKEN environment variable")
bot.run(token)
