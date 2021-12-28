import discord
import wikipedia
from discord.ext import commands


class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        wikipedia.set_lang("en")

        @bot.command()
        async def wikilang(ctx, arg):
            global wikidil_str
            if arg in wikipedia.languages():
                langsuccess_embed = discord.Embed(description="**✅  Wiki dili değiştirildi.**",
                                                  color=discord.Color.blue())
                await ctx.send(embed=langsuccess_embed)
                wikidil_str = str(arg)
                wikipedia.set_lang(wikidil_str)
            else:
                langerror_embed = discord.Embed(
                    description="**❌  Hata: İstenilen dil bulunamadı. Wiki'nin desteklediği dillerin listesi için [bu "
                                "sayfaya göz atabilirsiniz.]("
                                "https://en.wikipedia.org/wiki/List_of_Wikipedias#Editions_overview) (İstediğiniz "
                                "dilin WP kodunu girin)** ", color=discord.Color.blue())
                await ctx.send(embed=langerror_embed)

        @bot.command()
        async def wiki(ctx, *args):
            try:
                global wikidil_str
                print(wikidil_str)
            except NameError:
                wikidil_str = "en"
            arg = ('{}'.format(" ".join(args)))
            search_list = wikipedia.search(arg, 4, suggestion=False)
            search_embed = discord.Embed(title="Girilen Terim: *" + arg + "*",
                                         description="➤ Bu sayfalardan hangisini arıyorsunuz?\n➤ Cevabınızın "
                                                     "yanındaki **numarayı** girin: \n",
                                         color=discord.Color.blue())
            search_embed.set_footer(text="(Wiki dili: " + wikidil_str.upper() + ")")
            await ctx.send(embed=search_embed)
            for i in range(len(search_list)):
                await ctx.send("**" + str(i+1) + ") **" + search_list[i] + "\n")

            def check(m):
                return m.content is not None and m.channel == ctx.channel and any(i.isdigit() for i in str(m.content))

            message = await bot.wait_for('message', check=check)
            if message.author == ctx.author:
                topic_final_name = search_list[int(message.content) - 1]
                try:
                    topic_final = wikipedia.page(topic_final_name, auto_suggest=False)
                except wikipedia.exceptions.DisambiguationError as e:
                    s = e.options[0]
                    topic_final = wikipedia.page(s, auto_suggest=False)
                topic_final_title = topic_final.title
                topic_final_summary = wikipedia.summary(topic_final_title, auto_suggest=False)
                if len(topic_final_summary) > 4096:
                    long_embed = discord.Embed(
                        description="**❌  Hata: İstenilen sayfa bir mesaja sığmayacak kadar uzun. Başka bir sayfa "
                                    "deneyin.**",
                        color=discord.Color.red())
                    await ctx.send(embed=long_embed)
                    return
                else:
                    wiki_embed = discord.Embed(title=topic_final_title, url=topic_final.url,
                                               description=topic_final_summary,
                                               color=discord.Color.blue())
                    wiki_embed.set_author(name="Wikipedia " + wikidil_str.upper(), icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/155px-Wikipedia-logo-v2.svg.png")
                    wiki_embed.set_footer(text="(Wikipedia API'ının dilini değiştirmek için !wikilang)")
                    if len(topic_final.images) > 0:
                        wiki_embed.set_image(url=topic_final.images[0])
                    await ctx.send(embed=wiki_embed)


def setup(bot):
    bot.add_cog(WikiCog(bot))
