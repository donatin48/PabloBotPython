from cogs.commandsPablo import CogCommand
import discord
from discord.ext import commands 
import requests
import youtube_dl
import mal
import os
import time

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
}]
}

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            