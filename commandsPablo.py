import discord
from discord.ext import commands
import random
import time
from langdetect import detect , DetectorFactory
from translate import Translator

async def delete(self,ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        pass
    else :
        await ctx.message.delete() 

class CogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        livre = ""
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for c in range(int(nbr)) :
            livre =  livre + random.choice(alpha)
            c = c
        await delete(self,ctx)
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
        await ctx.send(embed=embed, delete_after=10)
        print(f"[Help] [{time.strftime('%H:%M:%S')}] : {ctx.author.name}")
        
    @commands.command()
    async def trad(self,ctx, arg1 :str, arg2 : str):
        DetectorFactory.seed = 0
        await delete(self,ctx)
        trad = " ".join(arg2)
        det = detect(trad)
        gs = Translator(to_lang=arg1,from_lang=det)
        traduction = gs.translate(trad)
        await ctx.send(traduction, delete_after=15)
        print(f"[Traduction] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ({det} --> {arg1}) : {trad} --> {traduction} ")

        