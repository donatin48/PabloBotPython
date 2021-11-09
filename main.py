import time
from discord.ext.commands.errors import CommandNotFound
t1 = time.time()
import discord
from discord.ext import commands ,tasks
from discord_slash import SlashCommand
import datetime 
import requests
from cogs import commandsPablo 
from cogs import voice
from cogs import admin
today = datetime.datetime.now()
today = today.strftime("%d/%m/%Y %H:%M:%S")
bot = commands.Bot(command_prefix="!", help_command=None)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

from datetime import datetime
from bs4 import BeautifulSoup

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
    printer.start()

@tasks.loop(minutes=2)
async def printer():
    reponse = requests.get("http://api.openweathermap.org/data/2.5/weather?q=andresy&appid=0dc100d22eac5b733265582d1b360ba6")
    meteo = reponse.json()
    c = meteo["main"]["temp"]
    c = round(c - 273.15,2)
    e = meteo["weather"][0]["main"]
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{c}°C | {e} | {today} 🐧"))

async def salebot():
    chan = bot.get_channel(303520736553992192)
    url = "https://0781845g.index-education.net/pronote/"
    send = False
    msg = "Le site n'est pas disponible."
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    i = 0
    try : 
        for div in soup.find_all(class_="texte"):
            i += 1
            if div.text != msg and i==2:
                send = True
                print("cbon")
                await chan.send("CBON <@228937896818638860>")
                break
    except:
        send = True
    if not send :
        print(f"ya r {datetime.now()} ")
        
@bot.command()
async def ent():
    await salebot()

@bot.event
async def on_command_error(ctx,error):
    print(f"[Error] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {error}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour faire cette commande. 🤖",delete_after=10)
        await commandsPablo.delete("",ctx)
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument. 🤖",delete_after=10)
        await commandsPablo.delete("",ctx)
    elif CommandNotFound():
        pass
    else :
        await ctx.send(f"ooff ça bogue :/ ({error}) ",delete_after=10)

cogs = [
    commandsPablo.CogCommand(bot),
    voice.voice(bot)
    # admin.Admin(bot)
]
for cog in cogs :
    print(f"Cog : {cog.qualified_name} imported")
    bot.add_cog(cog)

with open("db/config.ini","r",encoding="UTF-8") as r:
    key = r.read()
    r.close
bot.run(key)
