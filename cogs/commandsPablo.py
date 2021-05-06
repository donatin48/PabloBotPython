import discord
from discord.ext import commands , tasks
import random
import time
import os
from discord.ext.commands import bot
from langdetect import detect 
from translate import Translator
import requests
import youtube_dl
import mal

async def delete(self,ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        pass
    else :
        await ctx.message.delete() 

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '512',
}],
}
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

    @commands.command()
    async def watt(self,ctx,i : float):
        await delete(self,ctx)
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

    @commands.command(pass_context = True)
    async def leave(self,ctx):
        try :
            await delete("",ctx)
        except:
            pass
        server = ctx.message.guild.voice_client
        await server.disconnect()

    @commands.command(pass_context = True)
    async def join(self,ctx):
        try :
            await delete("",ctx)
        except:
            pass
        if ctx.voice_client is not None :
            return await ctx.voice_client.move_to(ctx.author.voice.channel)        
        voice = ctx.author.voice.channel
        await voice.connect()

    @commands.command()
    async def stop(self,ctx):
        try :
            await delete("",ctx)
        except:
            pass
        voice =  discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command()
    async def po(self,ctx,*url):
        await delete(self,ctx)
        url = " ".join(url)
        if not ctx.message.author.voice:
            await ctx.send('co toi à un channel 🍪')
            return
        else:
            url = await CogCommand.op(self,ctx,url,b=True)
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except:
                pass
            # voice = ctx.author.voice.channel
            try:
                # await voice.connect()
                await CogCommand.join("",ctx)
            except:
                pass
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url[2]])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    try :
                        os.rename(file, "song.mp3")
                    except :
                        await CogCommand.stop("",ctx)
                        time.sleep(1)
                        os.remove("song.mp3")
                        os.rename(file, "song.mp3")
            ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
            await ctx.send(f'Play: {url[0]} ({url[1]})',delete_after=5)

    @commands.command()
    async def op(self,ctx,*msg,b: bool = False):
        if b == False:
             await delete(self,ctx)
        # elif b == True :
        #     print(msg[0])
        #     msg = eval(msg[0])
        #     print(msg)
        mm = ""
        print(msg)
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
        print(msgg)
        if is_integer(msgg) :
            search = int(msgg)
        else :
            search = mal.AnimeSearch(msgg,timeout=10)
            search = search.results[0].mal_id
        print(search)
        reponse = requests.get(f"https://animethemes-api.herokuapp.com/api/v1/anime/{search}")
        reponse = reponse.json()
        r = reponse
        try:
            reponse = reponse["themes"][0]["mirrors"][0]
        except :
            await ctx.send(f"J'ai pas trouvé {str(msg)[2:-2:]} 🍉",delete_after=10)
            return print(f"[OP:Erreur] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> erreur : {str(msg)[2:-2:]}")
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
            if b == False:
                await ctx.send(titre,delete_after=99.5)
                await ctx.send(op,delete_after=99)
                await ctx.send(reponse,delete_after=98.5)
                print(f"[OP] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {op} | {titre} | {search}")
            else :
                print("oui")
                return (titre,op,reponse)
    
    @commands.command()
    async def covid(self,ctx):
        await delete(self,ctx)



        print("test")