import discord
from discord import app_commands
from discord.ext import commands

# Replace with actual values
STAFF_ROLE_ID = 1340726866352537600
LOG_CHANNEL_ID = 1385712673542377634

class PromotionIssue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="promotion_issue", description="Promote a user")
    @app_commands.describe(
        target="User you want to promote",
        role="Role the user is getting promoted to",
        reason="Reason for the promotion",
        notes="Any additional notes for the promotion"
    )
    async def promotion_issue(self, interaction: discord.Interaction, target: discord.User, role: discord.Role, reason: str, notes: str):
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not any(r.id == STAFF_ROLE_ID for r in member.roles):
            return await interaction.response.send_message("❌ You do not have permission to issue promotions.", ephemeral=True)

        embed = discord.Embed(title="📈 Staff Promotion", color=discord.Color.green())
        embed.add_field(name="User", value=f"<@{target.id}> ({target.id})", inline=False)
        embed.add_field(name="Role", value=role.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Notes", value=notes or "None", inline=False)
        embed.set_footer(text=f"Issued by {interaction.user}", icon_url=interaction.user.display_avatar.url)

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        await interaction.response.send_message(f"✅ Promotion issued for {target.mention} to {role.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PromotionIssue(bot))
