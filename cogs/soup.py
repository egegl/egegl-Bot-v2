import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class SoupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'
        }

        @bot.command()
        async def kur(ctx):

            r = requests.get("https://www.bloomberght.com/doviz/dolar", headers=header)
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                dolar_kur = soup.find('span', attrs={'class': 'upGreen'}).get_text(strip=True)
            except:
                dolar_kur = soup.find('span', attrs={'class': 'downRed'}).get_text(strip=True)
            dolar_artis = soup.find('span', attrs={'class': 'bulk'}).get_text(strip=True)
            tarih = soup.find('span', attrs={'class': 'date'}).get_text(strip=True)

            dolar_embed = discord.Embed(color=discord.Color.green())
            dolar_embed.add_field(name="Dolar:", value=dolar_kur + " ₺", inline=True)
            dolar_embed.add_field(name="Günlük Değişim:", value=dolar_artis, inline=True)

            r = requests.get("https://www.bloomberght.com/doviz/euro", headers=header)
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                euro_kur = soup.find('span', attrs={'class': 'upGreen'}).get_text(strip=True)
            except:
                euro_kur = soup.find('span', attrs={'class': 'downRed'}).get_text(strip=True)
            euro_artis = soup.find('span', attrs={'class': 'bulk'}).get_text(strip=True)

            euro_embed = discord.Embed(color=discord.Color.green())
            euro_embed.add_field(name="Euro:", value=euro_kur + " ₺", inline=True)
            euro_embed.add_field(name="Günlük Değişim:", value=euro_artis, inline=True)
            await ctx.send("**Güncel Dolar ve Euro Kuru 💸** \n ➤ Tarih: " + tarih)
            await ctx.send(embed=dolar_embed)
            await ctx.send(embed=euro_embed)

        @bot.command()
        async def osu(ctx, arg):
            osu_full_link = "https://ameobea.me/osutrack/user/" + arg
            r = requests.get(osu_full_link, headers=header)
            soup = BeautifulSoup(r.content, 'lxml')
            osu_table = soup.find('table', attrs={'class': 'quickstat'}).get_text()
            osu_image_html = soup.find('img', attrs={'class': 'img-rounded'})
            osu_image = osu_image_html['src']
            osu_embed = discord.Embed(title=arg + " Adlı Kullanıcının osu! Profili", url=osu_full_link,
                                      description=osu_table, color=discord.Color.from_rgb(255, 20, 147))
            osu_embed.set_thumbnail(url=osu_image)
            await ctx.send(embed=osu_embed)


def setup(bot):
    bot.add_cog(SoupCog(bot))
