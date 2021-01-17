import discord
from discord.ext import commands
import random
import time
from langdetect import detect 
from translate import Translator
import requests
# import youtube_dl
import os
import mal

async def delete(self,ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        pass
    else :
        await ctx.message.delete() 

def endSong(self,guild, path):
    os.remove(path)    

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

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
        embed.add_field(name="!op",value="!op + nom (ou id my anime list) --> Donne l'opening ",inline=False)
        
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
    async def lyr(self,ctx,artist : str, *title):
        await delete(self,ctx)
        title = " ".join(title)
        print(artist,title)
        reponse = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{title}")
        lyrics = reponse.json()
        await ctx.send(lyrics['lyrics'],delete_after=15)
        print(f"[Lyrics] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} ")

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
    async def meteo(self,ctx,ville ="andresy",jour =0):
        await delete(self,ctx)
        reponse = f"https://www.prevision-meteo.ch/uploads/widget/{ville}_{jour}.png "
        await ctx.send(reponse,delete_after=10)
        print(f"[Meteo] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} {ville} & {jour} ")

    # @commands.command(pass_context=True)
    # async def p(self,ctx,*url):
    #     await delete(self,ctx)
    #     if not ctx.message.author.voice:
    #         await ctx.send('you are not connected to a voice channel')
    #         return
    #     else:
    #         channel = ctx.message.author.voice.channel
    #         voice_client = await channel.connect()
    #         guild = ctx.message.guild
    #         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #             file = ydl.download(url)
    #         path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    #         voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x="")
    #         voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    #         await ctx.send(f'**Music: **{url}')

    @commands.command()
    async def op(self,ctx,*msg ):
        await delete(self,ctx)
        mm = ""
        if len(msg) >= 2 :
            try :
                int(msg[-1])
            except :
                pass
            else :
                mm = msg
                ls_msg = list(msg)
                del ls_msg[-1]
                msg = tuple(ls_msg)
        msgg = " ".join(msg)
        if is_integer(msgg) :
            search = int(msgg)
        else :
            search = mal.AnimeSearch(msgg)
            search = search.results[0].mal_id
        print(search)
        reponse = requests.get(f"https://animethemes-api.herokuapp.com/api/v1/anime/{search}")
        reponse = reponse.json()
        r = reponse
        try:
            reponse = reponse["themes"][0]["mirrors"][0]
        except :
            await ctx.send(f"J'ai pas trouvé {str(msg)[2:-2:]} 🍉",delete_after=10)
            print(f"[OP:Erreur] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> erreur : {str(msg)[2:-2:]}")
        else:
            for c , v in reponse.items() :
                if c == "mirror" :
                    reponse = v
                    break
            if len(mm) >= 2 :
                try :
                    int(mm[-1])
                except :
                    pass
                else :
                    intt = int(mm[-1])
                    r = reponse[0:-6:]
                    rr = reponse[-5::]
                    reponse = r + str(intt) + rr
            try :
                titre = reponse[30:-9:]
                op = reponse[-8:-5:]
            except :
                titre = ""
                op = ""
            await ctx.send(titre,delete_after=99.5)
            await ctx.send(op,delete_after=99)
            await ctx.send(reponse,delete_after=98.5)
            print(f"[OP] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {op} | {titre} | {search}")