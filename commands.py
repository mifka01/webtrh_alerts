from typing import Literal, Optional

from discord import HTTPException, Interaction, Object, app_commands
from discord.ext import commands

from config import AVAILABLE_CATEGORIES


class ChannelCog(commands.GroupCog, name="channel"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="set", description="It will set the main channel for the bot to which it will send new deals")
    async def set(self, interaction: Interaction) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            sql = "UPDATE guild set channel_id = (%s) where id = (%s)"
            values = (interaction.channel.id, interaction.guild.id)
            self.bot.webtrh.database.query(sql, values, commit=True)
            await interaction.response.send_message("Channel has been set", ephemeral=True)


class CategoryCog(commands.GroupCog, name="category"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="add", description="Add category to scrape from for current guild")
    async def add(self, interaction: Interaction, code: str) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
        elif code not in AVAILABLE_CATEGORIES.keys():
            categories = ""
            for key, val in AVAILABLE_CATEGORIES.items():
                if len(key) == 3:
                    categories += f"{key}  - {val}\n"
                else:
                    categories += f"{key} - {val}\n"
            message = f"""Category with code `{code}` is not available.\nYou can choose one from these:
            ```{categories}```"""
            await interaction.response.send_message(message, ephemeral=True)
        else:
            await interaction.response.send_message(f"Category `{code}` added", ephemeral=True)
            sql = "SELECT ID from category where code = %(code)s"
            category_id = self.bot.webtrh.database.query(
                sql, {"code": code}, fetchone=True)
            if category_id is None:
                sql = "INSERT INTO category (id, code) values (%s, %s)"
                self.bot.webtrh.database.query(
                    sql, (None, code), commit=True)
                sql = "SELECT ID from category where code = %(code)s"
                category_id = self.bot.webtrh.database.query(
                    sql, {"code": code}, fetchone=True)
            category_id = category_id['ID']
            sql = "SELECT ID from guild_categories where guild_id = %s and category_id = %s"
            guild_categories = self.bot.webtrh.database.query(
                sql, (interaction.guild.id, category_id), fetchone=True)
            if guild_categories is None:
                sql = "INSERT INTO guild_categories (id, guild_id, category_id) values (%s, %s, %s)"
                values = (None, interaction.guild.id, category_id)
                self.bot.webtrh.database.query(sql, values, commit=True)

    @app_commands.command(name="remove", description="Remove category to scrape from this guild")
    async def remove(self, interaction: Interaction, code: str) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            sql = "SELECT ID from category where code = %(code)s"
            category_id = self.bot.webtrh.database.query(
                sql, {"code": code}, fetchone=True)

            if category_id is None:
                await interaction.response.send_message("Category not found", ephemeral=True)
            await interaction.response.send_message("Category has been removed", ephemeral=True)
            category_id = category_id["ID"]

            sql = "DELETE from guild_categories where category_id = %s and guild_id = %s"
            values = (category_id, interaction.guild.id)
            self.bot.webtrh.database.query(sql, values, commit=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChannelCog(bot))
    await bot.add_cog(CategoryCog(bot))

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
