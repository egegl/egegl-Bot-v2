import requests
from bs4 import BeautifulSoup

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'referer': 'https://www.google.com/'
}


def dolar_webscrape():
    global dolar_kur, dolar_artis, dolar_tarih
    r = requests.get("https://www.bloomberght.com/doviz/dolar", headers=header)
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        dolar_kur = soup.find('span', attrs={'class': 'upGreen'}).get_text(strip=True)
    except:
        dolar_kur = soup.find('span', attrs={'class': 'downRed'}).get_text(strip=True)
    dolar_artis = soup.find('span', attrs={'class': 'bulk'}).get_text(strip=True)
    dolar_tarih = soup.find('span', attrs={'class': 'date'}).get_text(strip=True)


def euro_webscrape():
    global euro_kur, euro_artis
    r = requests.get("https://www.bloomberght.com/doviz/euro", headers=header)
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        euro_kur = soup.find('span', attrs={'class': 'upGreen'}).get_text(strip=True)
    except:
        euro_kur = soup.find('span', attrs={'class': 'downRed'}).get_text(strip=True)
    euro_artis = soup.find('span', attrs={'class': 'bulk'}).get_text(strip=True)


def osu_webscrape():
    global osu_table, osu_image
    with open("data/osulink.txt", "r") as f:
        f.seek(0)
        osu_link_sliced = str(f.read()[25:])
        osu_full_link = "https://ameobea.me/osutrack/user/" + osu_link_sliced
    r = requests.get(osu_full_link, headers=header)
    soup = BeautifulSoup(r.content, 'lxml')
    osu_table = soup.find('table', attrs={'class': 'quickstat'}).get_text()
    osu_image_html = soup.find('img', attrs={'class': 'img-rounded'})
    osu_image = osu_image_html['src']


user_emirbot = "elvodqa bot#2318"
user_egegl = "egegl#8414"
kys_emoji = "<:kys:834684488692924507>"
osu_link = 'https://osu.ppy.sh/users/'
a = 0

meme_subs = ["dankmemes", "memes", "comedyheaven"]
text_channels = ["memes", "reddit"]

langerror_desc = "**❌  Hata: İstenilen dil bulunamadı. Wiki'nin desteklediği dillerin listesi için [bu sayfaya göz atabilirsiniz.](https://en.wikipedia.org/wiki/List_of_Wikipedias#Editions_overview) (İstediğiniz dilin WP kodunu girin)**"

memes_channels_list = []

wikipedia_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/155px-Wikipedia-logo-v2.svg.png"

reddit_upvote = "https://i.ibb.co/myHx28s/toppng-com-reddit-clipart-icon-reddit-upvote-transparent-1024x1049.png"

help_message_title = "**egegl v2 Bot'un şu anda 9️⃣ komutu vardır:**"

help_message_1 = "**▶ !help:**  Bu mesajı gönderir.\n\n **▶ !osu <kullanıcı adı>:** Kullanıcı adı girilen osu! oyuncusunun profilini gönderir.\n\n **▶ !kur:**  Güncel Dolar ve Euro/TL kur verilerini gönderir (Bloomberg HT'nin sitesinden alınan veriler birkaç dakikada bir kendini günceller.)\n\n **▶ !megalul:**  Minecraft 1.17.1 SMP Sunucumuzu tanıtır :)\n\n **▶ !wiki <konu>:**  Girdiğiniz bir konu (örn !wiki Mission Impossible) hakkında size 4 tane seçebileceğiniz başlık sunar. Seçtiğiniz başlık üzerine size bilgi verir. (Wikipedia API'ı kullanılarak yapıldı.)\n\n **▶ !wikilang <en/tr/fr/de... etc.>:** Varsayılan dili İngilizce olan Wikipedia API'ının dilini değiştirir.\n\n **▶ !initmemes:** Komutun gönderildiği kanalın adı memes ise kanala her 15 dakikada bir Reddit'ten rastgele bir meme gönderir.\n\n \u200b"

help_message_2 = "**▶ !p <şarkı ismi>:** Bulunduğunuz ses kanalına katılır ve ismini girdiğiniz şarkıyı çalar. (Eğer başka bir şarkı çalınıyorsa istenilen şarkıyı sıraya ekler.)\n\n **▶ !queue:** Şarkı sırasını gönderir. (Sıraya şarkı eklemek için !p komutunu kullanın.)\n\n **▶ !skip:** Çalınan şarkıyı geçer, eğer sırada şarkı varsa onu çalar.\n\n **▶ !dc:** Bulunduğunuz ses kanalından çıkar,  şarkı sırasını sıfırlar.\n\n \u200b"

welcome_message = "▶ **Merhaba! Ben egegl Bot v2.** Beni Discord sunucunuza eklediğiniz için teşekkürler!\n\n▶ **!help** komutu ile işlevlerim hakkında bilgi edinebilirsiniz :)"
