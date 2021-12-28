import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        help_message_1 = "**▶ !help:**  Bu mesajı gönderir.\n\n **▶ !osu <kullanıcı adı>:** Kullanıcı adı girilen osu! " \
                         "oyuncusunun profilini gönderir.\n\n **▶ !kur:**  Güncel Dolar ve Euro/TL kur verilerini gönderir (" \
                         "Bloomberg HT'nin sitesinden alınan veriler birkaç dakikada bir kendini günceller.) \n\n **▶ !wiki " \
                         "<konu>:**  Girdiğiniz bir " \
                         "konu (örn !wiki Mission Impossible) hakkında size 4 tane seçebileceğiniz başlık sunar. Seçtiğiniz " \
                         "başlık üzerine size bilgi verir. (Wikipedia API'ı kullanılarak yapıldı.)\n\n **▶ !wikilang " \
                         "<en/tr/fr/de... etc.>:** Varsayılan dili İngilizce olan Wikipedia API'ının dilini değiştirir.\n\n " \
                         "**▶ !initmemes:** Komutun gönderildiği kanalın adı memes ise kanala her 15 dakikada bir Reddit'ten " \
                         "rastgele bir meme gönderir.\n\n \u200b "

        help_message_2 = "**▶ !p <şarkı ismi>:** Bulunduğunuz ses kanalına katılır ve ismini girdiğiniz şarkıyı çalar. (Eğer " \
                         "başka bir şarkı çalınıyorsa istenilen şarkıyı sıraya ekler.)\n\n **▶ !queue:** Şarkı sırasını " \
                         "gönderir. (Sıraya şarkı eklemek için !p komutunu kullanın.)\n\n **▶ !skip:** Çalınan şarkıyı geçer, " \
                         "eğer sırada şarkı varsa onu çalar.\n\n **▶ !dc:** Bulunduğunuz ses kanalından çıkar,  " \
                         "şarkı sırasını sıfırlar.\n\n \u200b "

        @bot.command()
        async def help(ctx):
            help_embed = discord.Embed(color=discord.Color.blue())
            help_embed.add_field(name="**▶️▶️ Genel Komutlar ◀️◀️**\n \u200b", value=help_message_1, inline=False)
            help_embed.add_field(name="**▶️▶️ Müzik Komutları ◀️◀️**\n \u200b", value=help_message_2, inline=False)
            help_embed.set_footer(icon_url="https://cdn.betterttv.net/emote/61526df6b63cc97ee6d3ab49/3x",
                                  text="@egegl#8414 tarafından kodlandı.")
            await ctx.send(embed=help_embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))
