from typing import Literal, Optional
from discord import app_commands, Object, Interaction, HTTPException
from discord.ext import commands


class MainCog(commands.GroupCog, name="set"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="channel", description="It will set the main channel for the bot to which it will send new deals")
    async def channel(self, interaction: Interaction) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            sql = "UPDATE guild set channel_id = (%s) where id = (%s)"
            values = (interaction.channel.id, interaction.guild.id)
            self.bot.webtrh.database.query(sql, values, commit=True)
            await interaction.response.send_message("Channel has been set", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MainCog(bot))

    @bot.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
      ctx: commands.Context, guilds: commands.Greedy[Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")





