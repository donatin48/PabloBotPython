import discord
from discord.ext import commands
import json
import os

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.chdir(r"db")
        # with open(r"db.json", "r") as f:
        #     self.users = json.load(f)

        self.bot.loop.create_task(self.save_users())
    async def save_users(self):
        await self.bot.wait_until_ready()
        with open(r"db.json", "w") as f:
            json.dump(self.users, f)    
