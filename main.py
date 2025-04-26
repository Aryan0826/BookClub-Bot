import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import string
import asyncio

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

@bot.command(name = "verify")
async def verify(ctx):
    # checking if command is sent in right channel or via DM
    welcomeChannelID = int(os.getenv("WELCOME_CHANNEL_ID",0))
    if ctx.channel.id != welcomeChannelID and not isinstance(ctx.channel, discord.DMChannel):
        return
    
    user = ctx.author

    try:
        # generate a random code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        verificationCodes[user.id] = code

        # send verfification instructions via DM
        await user.send( f"Hello {user.name}! To verify yourself on the server, please reply to this message with: "
            f"`$code {code}`")
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.message.add_reaction("✅")
            await ctx.send(f"{user.mention}, I've sent you verification instructions via DM. Please check your messages!")

        # Set timeout for verification code (delete code after 5 mins)
        await asyncio.sleep(300)  # 5 minutes
        if user.id in verificationCodes:
            del verificationCodes[user.id]
            try:
                await user.send("Your verification code has expired. Please type `$verify` again to get a new code.")
            except discord.errors.Forbidden:
                pass  # Can't send DM    

    except discord.errors.Forbidden:
        await ctx.send( f"{user.mention}, I couldn't send you a direct message. Please enable DMs from server members "
            f"in your privacy settings and try again.")    

@bot.command(name = "code")
async def codeVerify(ctx, verificationCode: str = None):
    user = ctx.author

    # only progress if sendt in dm
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.message.delete() # delete for privacy
        await ctx.send(f"{user.mention}, please send the verification code in a direct message to me, not in the server!")
        return
    
    if not verificationCode:
        await ctx.send("Please provide your verification code: `$code YOUR_CODE_HERE`")
        return

    # checking if code didnt expire
    if user.id not in verificationCodes:
        await ctx.send("You don't have an active verification session. Please type `$verify` to start verification.")
        return
    
    # Check if the code is correct
    if verificationCodes[user.id] != verificationCode:
        await ctx.send("Incorrect verification code. Please try again or type `$verify` to get a new code.")
        return
    
    # Code is correct, give the verified role
    del verificationCodes[user.id]  # Remove the code

    serverID = int(os.getenv("GUILD_ID",0))
    roleID = int(os.getenv("VERIFIED_ROLE_ID",0))

    if serverID and roleID:
        server = bot.get_guild(serverID)
        if server:
            member = server.get_member(user.id)
            if member:
                role = server.get_role(roleID)
                if role:
                    await member.add_roles(role)
                    await ctx.send(f"Verification successful! You now have access to the server. Welcome!")

                     # Announce in welcome channel
                    welcome_channel_id = int(os.getenv("WELCOME_CHANNEL_ID", 0))
                    if welcome_channel_id:
                        welcome_channel = bot.get_channel(welcome_channel_id)
                        if welcome_channel:
                            await welcome_channel.send(f"{member.mention} has been verified and can now access the server. Welcome!")
                else:
                    await ctx.send("Verification role not found. Please contact a server administrator.")
            else:
                await ctx.send("Couldn't find your membership in the server. Are you still a member?")
        else:
            await ctx.send("Error finding the server. Please contact an administrator.")
    else:
        await ctx.send("Server setup incomplete. Please contact an administrator.")

# to run the bot 
# we need to pass the token to the run command
# token is stored in the env file
token = os.getenv("TOKEN")
if not token:
    raise RuntimeError("Missing TOKEN environment variable")
bot.run(token)
