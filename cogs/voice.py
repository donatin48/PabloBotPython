import discord
from discord.ext import commands 
from discord import FFmpegPCMAudio
import requests
import youtube_dl
import os
import time
import re
async def delete(ctx):
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
            await delete(ctx)
        except:
            pass
        server = ctx.message.guild.voice_client
        await server.disconnect()

    @commands.command(pass_context = True)
    async def join(self,ctx):
        try :
            await delete(ctx)
        except:
            pass

        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send('co toi à un channel 🍪')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

    @commands.command()
    async def stop(self,ctx):
        try :
            await delete(ctx)
        except:
            pass
        voice =  discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()
    
    async def make_list_audio(self,search,number):
        t1 = time.time()
        l = requests.get(f"http://192.168.1.30:8000/api/v1/search/anime/{search}").json()
        t2 = time.time()
        print(f"Time to request {(t2-t1)*1000}ms")
        if l :
            themes = l[0]["themes"]
            print(f"LONGUEUR : {len(themes)}")
            for theme in themes:
                print(theme["type"])
                if re.search(f"OP{number}".upper(),theme["type"]):
                    title = theme["title"]
                    type = theme["type"]
                    link = theme["mirrors"][0]["audio"]
                    print(link)
                    break
            t3 = time.time()
            print(f"Temps pour trouver {(t3-t2)*1000}ms")
            # audio = requests.get(link).json()["audio"]
            audio = requests.get(f"http://192.168.1.30:8000{link[36:]}").json()["audio"]
            print(f"requete audio {time.time()-t3}s")
            return (title,type,audio)

    # @commands.check(is_connected)
    @commands.command()
    async def po(self,ctx,*,msg):
        await delete(ctx)

        await ctx.send(f"Entre le numéro de l'op de {msg}",delete_after=10)
        number = await self.bot.wait_for("message",timeout=30)

        response = await voice.make_list_audio(self,msg,number.content)
        print(response)

        voice_client = ctx.voice_client
        source = FFmpegPCMAudio(response[2])
        voice_client.play(source)

        # channel = ctx.message.author.voice.channel
        # voice_  = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        return

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

    async def make_list(self,search,number=1):
        # l = requests.get(f"https://animethemes-api.herokuapp.com/api/v1/search/anime/{search}").json()
        l = requests.get(f"http://127.0.0.1:8000/api/v1/search/anime/{search}").json()
        if l :
            title = l[0]["themes"][0]["title"]
            type = l[0]["themes"][0]["type"]
            link = l[0]["themes"][0]["mirrors"][0]["mirror"]
            if number != 1:
                themes = l[0]["themes"]
                for theme in themes:
                    print(theme["type"])
                    if re.search(f"OP{number}".upper(),theme["type"]):
                        title = theme["title"]
                        type = theme["type"]
                        link = theme["mirrors"][0]["mirror"]
                        break
                print(link)

            response = (title,type,link,search)
            return response

    async def print_op(self,ctx,response):
        await ctx.send(response[0],delete_after=99.5)
        await ctx.send(response[1],delete_after=99)
        await ctx.send(response[2],delete_after=98.5)
        print(f"[OP] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> {response[1]} | {response[0]} | {response[3]}")

    @commands.command()
    async def op(self,ctx,*,msg):
        '''
        I use https://github.com/LetrixZ/animethemes-api for get data
        '''
        await delete(ctx)
        print(msg)
        response = await voice.make_list(self,msg)
        if not response :
            await ctx.send(f"J'ai pas trouvé {msg} 🍉",delete_after=10)
            return print(f"[OP:Erreur] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> erreur : {str(msg)}")
        print(response)
        return await voice.print_op(self,ctx,response)

    @commands.command()
    async def opn(self,ctx,*,msg):
        await delete(ctx)
        print(msg)
        await ctx.send(f"Entre le numéro de l'op de {msg}",delete_after=10)
        number = await self.bot.wait_for("message",timeout=30)
        response = await voice.make_list(self,msg,number.content)
        if not response :
            await ctx.send(f"J'ai pas trouvé {msg} 🍉",delete_after=10)
            return print(f"[OP:Erreur] [{time.strftime('%H:%M:%S')}] : {ctx.author.name} --> erreur : {str(msg)}")
        print(number.content)
        return await voice.print_op(self,ctx,response)