import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

STAFF_ROLE_ID = 1335778270871945286
LOG_CHANNEL_ID = 1335226744126308476

class InfractionIssue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="infraction-issue", description="Issue an infraction to a user.")
    @app_commands.describe(
        target="User to infract",
        reason="Reason for the infraction",
        type="Select the infraction type",
        expires="Expiration time in days (optional)"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="Notice", value="Notice"),
        app_commands.Choice(name="Warning", value="Warning"),
        app_commands.Choice(name="Strike", value="Strike"),
        app_commands.Choice(name="Suspension", value="Suspension"),
        app_commands.Choice(name="Termination", value="Termination")
    ])
    async def infraction_issue(self, interaction: discord.Interaction, target: discord.User, reason: str, type: app_commands.Choice[str], expires: int = None):

        if not any(role.id == STAFF_ROLE_ID for role in interaction.user.roles):
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
            return

        expiration_date = datetime.utcnow() + timedelta(days=expires) if expires else None


        embed = discord.Embed(
            title="Staff Infraction",
            color=discord.Color.from_rgb(255, 255, 255),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="**User**", value=f"<@{target.id}> ({target.id})", inline=False)
        embed.add_field(name="**Type**", value=type.value, inline=False)
        embed.add_field(name="**Reason**", value=reason, inline=False)
        embed.set_footer(text=f"Issued By: {interaction.user}", icon_url=interaction.user.display_avatar.url)

        if expiration_date:
            embed.add_field(
                name="**Expires**",
                value=f"<t:{int(expiration_date.timestamp())}:R>",
                inline=False
            )

        # 🔔 Log channel
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(content=f"<@{target.id}>", embed=embed)

        # 📩 DM the user
        try:
            dm_embed = discord.Embed(
                title=f"⚠️ You’ve received an infraction in {interaction.guild.name}",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            dm_embed.add_field(name="Type", value=type.value, inline=False)
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            dm_embed.add_field(name="Issued By", value=f"<@{interaction.user.id}>", inline=False)

            if expiration_date:
                dm_embed.add_field(
                    name="Expires",
                    value=f"<t:{int(expiration_date.timestamp())}:R>",
                    inline=False
                )

            await target.send(embed=dm_embed)
        except Exception as e:
            print(f"Could not DM {target}: {e}")

        # ✅ Confirm
        await interaction.response.send_message(
            content=f"<:whitecheck:1407773605642764389> <@{target.id}> has successfully been infracted!",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(InfractionIssue(bot))