from discord.ext import commands
import discord


def is_owner_check(message):
    return message.author.id == 228937896818638860

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @is_owner()
    async def load(self, ctx, *, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}',delete_after=10)
            await ctx.send('{}: {}'.format(type(e).__name__, e),delete_after=10)
        else:
            await ctx.send('\N{OK HAND SIGN}',delete_after=10)

    @commands.command(hidden=True)
    @is_owner()
    async def unload(self, ctx, *, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}',delete_after=10)
            await ctx.send('{}: {}'.format(type(e).__name__, e),delete_after=10)
        else:
            await ctx.send('\N{OK HAND SIGN}',delete_after=10)

    @commands.command(name='reload', hidden=True)
    @is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}',delete_after=10)
            await ctx.send('{}: {}'.format(type(e).__name__, e),delete_after=10)
        else:
            await ctx.send('\N{OK HAND SIGN}',delete_after=10)