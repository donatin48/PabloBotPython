import discord
from discord.ext import commands 
import random
import time
import os
from discord.ext.commands.cog import Cog
from langdetect import detect 
from translate import Translator
from discord_slash import cog_ext, SlashContext
import requests

async def delete(self,ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) or not ctx.message :
        pass
    else :
        await ctx.message.delete() 

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)
    
class CogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def val(self,ctx):
        await delete(self,ctx)
        path = r"/home/pi/valheim/ftp"
        map = newest(path)
        await ctx.send(f"la dernière version de la map est {map[21:-4]}")
        await ctx.send(file=discord.File(map))
        print(f"[Valheim] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ({map[21:]})")

    @commands.command()
    async def cal(self,ctx,c :str):
        p = ""
        await delete(self,ctx)
        i = str(eval(c))
        for y in i :
            if y == '"' :
                p = p
            else :
                p = p + y
        if len(p) > 2000 :
            await ctx.send(">2000 🐷", delete_after=5)
        else:
            await ctx.send(p,delete_after=5)
        print(f"[Python] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} {c} --> {p}")
        
    @commands.command(name="random")
    async def randomm(self,ctx, nbr : int):
        rand =  random.randint(0,nbr)
        await delete(self,ctx)
        await ctx.send(f"{rand}", delete_after=5)
        print(f"[Random] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} {nbr} --> {rand} ")

    @commands.command()
    async def book(self,ctx, nbr: int):
        await delete(self,ctx)
        if nbr > 2000 :
            await ctx.send(">2000 🐷", delete_after=5)
            pass
        else :
            livre = ""
            alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            for c in range(int(nbr)) :
                livre =  livre + random.choice(alpha)
                c = c
            await ctx.send(f"{livre}", delete_after=5)
            print(f"[Book] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {nbr} ")

    @commands.command()
    async def help(self,ctx):
        await delete(self,ctx)

        embed = discord.Embed(colour = discord.Colour.red()) 
        embed.set_author(name="Liste des commandes 🐧")
        embed.set_thumbnail(url="https://www.wildrepublic.com/wp-content/uploads/2018/11/Penguin-Walking-xl-1-600x404.jpg")
        embed.add_field(name="!random",value="!random + un entier --> Nombre entre 0 et ...",inline=False)
        embed.add_field(name="!book",value="!book + un entier --> Chaine de caractère(s) entre 0 et ...",inline=False)
        embed.add_field(name="!cal",value="!cal + ? --> Fait une opération python",inline=False)
        embed.add_field(name="!trad",value="!trad + en,de,... + chaine à traduire --> Traduit ",inline=False)
        embed.add_field(name="!fox",value="!fox --> Donne un renard aléatoire ",inline=False)
        embed.add_field(name="!dog",value="!dog --> Donne un chien aléatoire ",inline=False)
        embed.add_field(name="!lyr",value="!lyr + artiste + titre --> Donne les lyrics ",inline=False)
        embed.add_field(name="!meteo",value="!meteo + ville + J+? --> Donne la méteo ",inline=False)
        embed.add_field(name="!op",value="!op + nom --> Donne l'opening ",inline=False)
        
        await ctx.send(embed=embed, delete_after=10)
        print(f"[Help] [{time.strftime('%H:%M:%S')}] : {ctx.author.name}")
 
    @commands.command()
    async def trad(self,ctx, arg1 :str, *arg2 : str):
        await delete(self,ctx)
        trad = " ".join(arg2)
        det = detect(trad)
        gs = Translator(to_lang=arg1,from_lang=det)
        traduction = gs.translate(trad)
        await ctx.send(traduction, delete_after=15)
        print(f"[Traduction] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ({det} --> {arg1}) : {trad} --> {traduction} ")

    @commands.command()
    async def fox(self,ctx):
        await delete(self,ctx)
        reponse = requests.get("https://randomfox.ca/floof/")
        fox = reponse.json()
        embed = discord.Embed(colour = discord.Colour.dark_blue())
        embed.set_image(url=fox['image'])
        await ctx.send(embed=embed,delete_after=10)
        print(f"[Fox] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ")
    
    @commands.command()
    async def dog(self,ctx):
        await delete(self,ctx)
        reponse = requests.get("https://random.dog/woof.json")
        dog = reponse.json()
        embed = discord.Embed(colour = discord.Colour.dark_orange())
        embed.set_image(url=dog['url'])
        await ctx.send(embed=embed,delete_after=10)
        print(f"[Dog] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ")

    @commands.command()
    async def watt(self,ctx,i : float):
        await delete(self,ctx)
        i = float(i)
        watt = ""
        for c in range(1,24):
            wh = i*c/1000
            watt += f"Pour {c} heures : {wh}Wh donc {round(wh*0.16,3)}€\n "
        watt += "\n"
        watt += f"Pour 1 jour : {i*24/1000}Wh donc {round((i*24/1000)*0.16,3)}€\n "
        watt += f"Pour 7 jours : {i*24*7/1000}Wh donc {round((i*24*7/1000)*0.16,3)}€\n "
        watt += f"Pour 1 mois : {i*24*30.45/1000}Wh donc {round((i*24*30.45/1000)*0.16,3)}€\n "
        watt += f"Pour 1 an : {i*24*365.25/1000}Wh donc {round((i*24*365.25/1000)*0.16,3)}€\n "
        watt += f"Pour 10 ans : {i*24*365.25*10/1000}Wh donc {round((i*24*365.25*10/1000)*0.16,3)}€\n "
        await ctx.send(watt,delete_after=20)
        print(f"[Watt] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ({i}) ")

    @commands.command()
    async def sak(self,ctx,search=None):
        await delete(self,ctx)
        if search :
            # i = random.randint(0,5000)
            res = requests.get(f"https://www.sakugabooru.com/post.json?tags={search}").json()
        else:

            i = random.randint(0,5000)
            res = requests.get(f"https://www.sakugabooru.com/post.json?page={i}").json()
            
        l = random.randint(0,len(res))
        url = res[l]
        times = time.ctime(int(url["created_at"]))
        times = time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime(int(url["created_at"]))) 

        await ctx.send(times,delete_after=30)
        await ctx.send(url["tags"],delete_after=30)
        await ctx.send(url["file_url"],delete_after=30)

        print(f"[Sak] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} {url['file_url']} {url['tags']} {search} ")

    @cog_ext.cog_slash(name="watt")
    async def watts(self,ctx,valeur : float):
        await CogCommand.watt(self,ctx,valeur)

    @cog_ext.cog_slash(name="test")
    async def test(self, ctx: SlashContext):
        print("test")
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])

    @cog_ext.cog_slash(name="ping")
    async def ping(self,ctx):
        print("test")
        await ctx.send(f"Pong {round(self.bot.latency*1000)}ms")
