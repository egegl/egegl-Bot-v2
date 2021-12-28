import re
import discord
import youtube_dl
from asyncio import sleep, run
from discord.ext import commands
from urllib.request import Request, urlopen
from __main__ import env


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        async def p(ctx, *args):
            global queue_list, vc, video_ids, FFMPEG_OPTIONS, YDL_OPTIONS
            queue_list = []
            search_term = ('{}'.format("+".join(args)))
            request = Request("https://www.youtube.com/results?search_query=" + search_term)
            request.add_header(env["BOT_TOKEN"], "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                                                 "KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
            response = urlopen(request)
            video_ids = re.findall(r"watch\?v=(\S{11})", response.read().decode())
            queue_list.append("https://www.youtube.com/watch?v=" + video_ids[0])
            if len(queue_list) > 1:
                queue_embed = discord.Embed(
                    description="**✅  Şarkı sıraya eklendi, şu an çalan şarkıyı geçmek için !skip yazın.**",
                    color=discord.Color.red())
                await ctx.send(embed=queue_embed)
            voiceclient = ctx.guild.voice_client
            if not voiceclient:
                try:
                    await ctx.author.voice.channel.connect()
                except:
                    novoice_embed = discord.Embed(
                        description="**❌  Bu komutu kullanmak için bir ses kanalına bağlanın.**",
                        color=discord.Color.red())
                    await ctx.send(embed=novoice_embed)
            vc = ctx.voice_client
            FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                              "options": "-vn"}
            YDL_OPTIONS = {"format": "bestaudio"}
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url=queue_list[0], download=False)
                url_2 = info["formats"][0]["url"]
                audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
                if len(queue_list) == 1:
                    ctx.voice_client.play(source=audio_source, after=lambda e: run(skip(ctx)))
                    await ctx.send("**Çalınan Parça: **" + " " + queue_list[0])

        @bot.command()
        async def dc(ctx):
            try:
                queue_list.clear()
                await ctx.voice_client.disconnect()
            except:
                return

        @bot.command()
        async def skip(ctx):
            skip_embed = discord.Embed(description="**✅  Şarkı geçildi.**", color=discord.Color.red())
            try:
                del queue_list[0]
            except:
                return
            if len(queue_list) >= 1:
                vc.stop()
                connected = False
                while not connected:
                    try:
                        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(url=queue_list[0], download=False)
                            url_2 = info["formats"][0]["url"]
                            audio_source = await discord.FFmpegOpusAudio.from_probe(url_2, **FFMPEG_OPTIONS)
                            connected = True
                            await sleep(1)
                    except:
                        pass
                vc.play(source=audio_source, after=lambda e: run(skip(ctx)))
                await ctx.send(embed=skip_embed)
                await ctx.send("**Çalınan Parça: **https://www.youtube.com/watch?v=" + video_ids[0])
            elif len(queue_list) == 0:
                await ctx.send(embed=sıra_boş_embed)
                await ctx.send(embed=skip_embed)
                await sleep(30)
                await ctx.voice_client.disconnect()
                return

        @bot.command()
        async def queue(ctx):
            global sıra_boş_embed
            sıra_boş_embed = discord.Embed(description="**▶️  Şarkı sırası boş.**", color=discord.Color.red())
            try:
                if len(queue_list) > 0:
                    sıra_embed = discord.Embed(title="**Şarkı Sırası:**", color=discord.Color.red())
                    await ctx.send(embed=sıra_embed)
                    for i in range(len(queue_list)):
                        await ctx.send("**" + str(i+1) + ")** " + queue_list[i])
                else:
                    await ctx.send(embed=sıra_boş_embed)
            except:
                return


def setup(bot):
    bot.add_cog(MusicCog(bot))
