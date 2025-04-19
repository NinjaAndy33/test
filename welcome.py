import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Required to detect member joins

bot = commands.Bot(command_prefix="!", intents=intents)

# When the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Event: Member joins
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')  # change 'general' to your channel name
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

# Command: Manual welcome
@bot.command()
async def welcome(ctx, member: discord.Member):
    await ctx.send(f"Welcome to the server, {member.mention}! Glad to have you here.")

# Run the bot
bot.run('BOT_TOKEN')
