import discord
from discord.ext import commands

class PrefixPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check the bot's latency.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000) 
        await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

async def setup(bot):
    await bot.add_cog(PrefixPing(bot))
