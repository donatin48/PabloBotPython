import time
t1 = time.time()
import discord
from discord.ext import commands
from cogs import commandsPablo 
import datetime 
bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
@bot.event
async def on_ready():
    tmps = time.time() - t1
    print('---------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(f"connecté à {len(bot.guilds)} server(s) ")
    print(f"Démarré en {round(tmps,3)} s")
    print('---------------------')
    today = datetime.datetime.now()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{today} 🐧"))
    general = bot.get_channel(764558994881904662)
    await general.connect()

@bot.event
async def on_command_error(ctx,error, user : discord.Member):
    print(f"[Error] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {error}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour faire cette commande. 🤖",delete_after=10)
        await commandsPablo.delete("",ctx)
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument. 🤖",delete_after=10)
        await commandsPablo.delete("",ctx)
    else :
        await ctx.send(f"{user.mention} ooff ça bogue :/ ({error}) ",delete_after=10)

cogs = [
    commandsPablo.CogCommand(bot),
    # level.Levels(bot)
]
for cog in cogs :
    bot.add_cog(cog)

with open("db/config.ini","r",encoding="UTF-8") as r:
    key = r.read()
    r.close
bot.run(key)
