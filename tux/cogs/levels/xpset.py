import discord
from discord.ext import commands

from tux.bot import Tux
from tux.database.controllers.levels import LevelsController
from tux.ui.embeds import EmbedCreator, EmbedType
from tux.utils import checks
from tux.utils.flags import generate_usage
from tux.utils.functions import valid_xplevel_input


class XPSet(commands.Cog):
    def __init__(self, bot: Tux) -> None:
        self.bot = bot
        self.levels_controller = LevelsController()
        self.xp_set.usage = generate_usage(self.xp_set)

    @commands.guild_only()
    @checks.has_pl(2)
    @commands.hybrid_command(name="xpset")
    async def xp_set(self, ctx: commands.Context[Tux], user: discord.User, xp_amount: int) -> None:
        """
        Sets the xp of a user.

        Parameters
        ----------
        ctx : commands.Context[Tux]
            The context object for the command.

        member : discord.Member
            The member to set the XP for.
        """
        if ctx.guild is None:
            await ctx.send("This command can only be executed within a guild.")
            return

        embed_result: discord.Embed | None = valid_xplevel_input(xp_amount) or discord.Embed()
        if embed_result:
            await ctx.send(embed=embed_result)
            return

        guild_id = ctx.guild.id
        user_id = user.id
        old_level = await self.levels_controller.get_level(user_id, guild_id)
        xp = await self.levels_controller.get_xp(user_id, guild_id)

        member = ctx.guild.get_member(user.id)
        if member is None:
            await ctx.send("User is not a member of this guild.")
            return

        await self.levels_controller.set_xp(user_id, guild_id, xp_amount, member, ctx.guild)

        new_level: int = await self.levels_controller.calculate_level(user_id, guild_id, member, ctx.guild)

        embed: discord.Embed = EmbedCreator.create_embed(
            embed_type=EmbedType.INFO,
            title=f"XP Set - {user}",
            description=f"{user}'s XP has been updated from **{xp}** to **{xp_amount}**\nTheir level has been updated from **{old_level}** to **{new_level}**",
            custom_color=discord.Color.blurple(),
        )

        await ctx.send(embed=embed)


async def setup(bot: Tux) -> None:
    await bot.add_cog(XPSet(bot))
