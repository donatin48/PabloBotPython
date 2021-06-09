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

    async def recup_lien(self,ctx):
        pass

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
            url = await voice.op(self,ctx,url)
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except:
                pass
            # voice = ctx.author.voice.channel
            try:
                # await voice.connect()
                await voice.join("",ctx)
            except:
                pass
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url[2]])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    try :
                        os.rename(file, "song.mp3")
                    except :
                        await voice.stop("",ctx)
                        time.sleep(1)
                        os.remove("song.mp3")
                        os.rename(file, "song.mp3")
            ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
            await ctx.send(f'Play: {url[0]} ({url[1]})',delete_after=5)

    async def make_list(self,search):
        l = requests.get(f"https://animethemes-api.herokuapp.com/api/v1/search/anime/{search}").json()
        if l :
            title = l[0]["themes"][0]["title"]
            type = l[0]["themes"][0]["type"]
            link = l[0]["themes"][0]["mirrors"][0]["mirror"]
            response = (title,type,link,search)
            return response

    async def make_list_mal_id(self,search):
        l = requests.get(f"https://animethemes-api.herokuapp.com/api/v1/anime/{search}").json()
        if l :
            try : 
                title = l[0]["themes"][0]["title"]
                type = l[0]["themes"][0]["type"]
                link = l[0]["themes"][0]["mirrors"][0]["mirror"]
                response = (title,type,link,search)
                return response
            except:
                pass

    async def print_op(self,ctx,response,number=1):
        await ctx.send(response[0],delete_after=99.5)
        await ctx.send(response[1],delete_after=99)
        await ctx.send(response[2],delete_after=98.5)
        print(f"[OP] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {response[1]} | {response[0]} | {response[3]}")

    @commands.command()
    async def op(self,ctx,*,msg):
        print(msg)
        response = await voice.make_list(self,msg)
        if not response :
            await ctx.send("Pas trouvé : 2ème API (erreurs possibles) ",delete_after=10)
            search = mal.AnimeSearch(msg,timeout=10)
            search = search.results[0].mal_id
            if search:
                response = await voice.make_list_mal_id(self,search)
                print(response)
                if response :
                    return await voice.print_op(self,ctx,response)
            await ctx.send(f"J'ai pas trouvé {msg} 🍉",delete_after=10)
            return print(f"[OP:Erreur] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> erreur : {str(msg)}")
        print(response)
        return await voice.print_op(self,ctx,response)

        await delete(self,ctx)
        mm = ""
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
            await ctx.send(titre,delete_after=99.5)
            await ctx.send(op,delete_after=99)
            await ctx.send(reponse,delete_after=98.5)
            print(f"[OP] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {op} | {titre} | {search}")
                # return (titre,op,reponse)

    @commands.command()
    async def opn(self,ctx,*,msg):
        print(msg)
        # response = await voice.make_list(self,msg)
        await ctx.send("Entre le numéro de l'op",delete_after=5)
        number = await self.bot.wait_for("message",timeout=30)
        print(number.content)
        # return await voice.print_op(self,ctx,response)