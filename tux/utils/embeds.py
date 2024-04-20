from datetime import datetime

import discord
from discord.ext import commands

from tux.utils.constants import Constants as CONST

# TODO: Refactor this to reduce code duplication


class EmbedCreator:
    @staticmethod
    def get_timestamp(
        ctx: commands.Context[commands.Bot] | None, interaction: discord.Interaction | None
    ) -> datetime:
        if ctx and ctx.message:
            return ctx.message.created_at
        return interaction.created_at if interaction else discord.utils.utcnow()

    @staticmethod
    def get_footer(
        ctx: commands.Context[commands.Bot] | None, interaction: discord.Interaction | None
    ) -> tuple[str, str | None]:
        user: discord.User | discord.Member | None = None
        latency = None

        if ctx:
            user = ctx.author
            latency = round(ctx.bot.latency * 1000, 2)
        elif interaction:
            user = interaction.user
            latency = round(interaction.client.latency * 1000, 2)

        if isinstance(user, discord.User | discord.Member):
            return (
                f"{user.name}@atl $ ∕tux {latency}ms",  # noqa: RUF001
                str(user.avatar.url) if user.avatar else None,
            )

        return ("", None)

    @staticmethod
    def add_field(embed: discord.Embed, name: str, value: str, inline: bool = True) -> None:
        embed.add_field(name=name, value=value, inline=inline)

    @staticmethod
    def base_embed(
        ctx: commands.Context[commands.Bot] | None,
        interaction: discord.Interaction | None,
        state: str,
    ) -> discord.Embed:
        footer: tuple[str, str | None] = EmbedCreator.get_footer(ctx, interaction)
        timestamp: datetime = EmbedCreator.get_timestamp(ctx, interaction)

        embed = discord.Embed()

        embed.color = CONST.EMBED_STATE_COLORS[state]

        embed.set_author(
            name=state.capitalize() if state else "Info",
            icon_url=CONST.EMBED_STATE_ICONS[state]
            if state
            else CONST.EMBED_STATE_ICONS["DEFAULT"],
        )

        embed.set_footer(text=footer[0], icon_url=footer[1])

        embed.timestamp = timestamp

        return embed

    @classmethod
    def create_embed(
        cls,
        ctx: commands.Context[commands.Bot] | None,
        interaction: discord.Interaction | None,
        state: str,
        title: str,
        description: str = "",
    ) -> discord.Embed:
        embed = cls.base_embed(ctx, interaction, state)
        embed.title = title
        embed.description = description

        return embed

    @classmethod
    def create_default_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "DEFAULT", title, description)

    @classmethod
    def create_info_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "INFO", title, description)

    @classmethod
    def create_error_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "ERROR", title, description)

    @classmethod
    def create_warning_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "WARNING", title, description)

    @classmethod
    def create_success_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "SUCCESS", title, description)

    @classmethod
    def create_poll_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "POLL", title, description)

    @classmethod
    def create_log_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "LOG", title, description)

    @classmethod
    def create_infraction_embed(
        cls,
        title: str,
        description: str,
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
    ) -> discord.Embed:
        return cls.create_embed(ctx, interaction, "INFRACTION", title, description)
