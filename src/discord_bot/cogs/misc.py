from typing import Literal, Optional

import re

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks

from ..log_setup import logger
from ..utils import utils as ut
from ..environment import CHANNEL_ID


### @package misc
#
# Collection of miscellaneous helpers.
#

class Misc(commands.Cog):
    """
    Various useful Commands for everyone
    """

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.emoji_up: str = "⬆"
        self.emoji_down: str = "⬇"

    # a chat based command
    @commands.command(name='ping', help="Check if Bot available")
    async def ping(self, ctx):
        """!
        ping to check if the bot is available

        @param ctx Context of the message
        """
        logger.info(f"ping: {round(self.bot.latency * 1000)}")

        await ctx.send(
            embed=ut.make_embed(
                name='Bot is available',
                value=f'`{round(self.bot.latency * 1000)}ms`')
        )

    @app_commands.command(name="ping", description="Ping as a slash command")
    # @app_commands.guild_only
    async def ping_slash(self,
                         interaction: discord.Interaction,
                         mode: Optional[Literal["silent", "loud"]]):
        """
        Ping command implementing the same functionality as "chat"-command
        But with extra option to be silent
        """
        logger.info(f"ping: {round(self.bot.latency * 1000)}")
        # decide whether this message shall be silent
        ephemeral = True if mode and mode == "silent" else False

        await interaction.response.send_message(
            embed=ut.make_embed(
                name='Bot is available',
                value=f'`{round(self.bot.latency * 1000)}ms`'),
            ephemeral=ephemeral
        )

    def check_zeichen(self, msg: str) -> bool:
        zeichen = ["'", '"', "“"]

        if "@" in msg:
            for z in zeichen:
                if z in msg:
                    return True
        
        return False
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Ignore bot reactions
        if user.bot:
            return
        
        logger.info("catched")
        if reaction.emoji == self.emoji_up:
            logger.info("up")
        elif reaction.emoji == self.emoji_down:
            logger.info("down")

        logger.info(reaction.message.content)
        logger.info(reaction.message.id)

    # Example for an event listener
    # This one will be called on each message the bot receives
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ch = message.channel
        if ch.id == int(CHANNEL_ID):
            #messages = ch.history(limit=10000)

            #async for msg in messages:
                # Check if msg is a Zitat
            if self.check_zeichen(message.content):
                zitat_result = re.findall(r'"(.*)"', message.content)
                mention_result = re.findall(r'<@(.*)>', message.content)
                if len(zitat_result) != 0 or len(mention_result) != 0:
                    zitat = zitat_result[0]
                    mention = mention_result[0]
                    logger.info(f"[{message.id}] {zitat} ({mention})")
                    await message.add_reaction(self.emoji_up)
                    await message.add_reaction(self.emoji_down)


    # Example for a task
    # It can be started using self.my_task.start() e.g. from this cogs __init__
    @tasks.loop(seconds=10)
    async def my_task(self):
        pass

async def setup(bot):
    await bot.add_cog(Misc(bot))
