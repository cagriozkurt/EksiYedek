# EksiYedek

Sözlük, yazara sadece kendi girdilerini yedekleme fırsatı sunmakta. Bu script, herhangi bir sözlük yazarının tüm girdilerini orijinal yedek dosyasına yakın bir biçimde yedeklemeye çalışır.

Elde edilen XML dosyası https://github.com/altunenes/EksiKelime scriptinden geçirilirse ilginç veriler elde edilebilir.

    git clone https://github.com/cagriozkurt/EksiYedek.git
    cd EksiYedek
    pip install requests bs4
    # 11. satırdaki nick değeri istenilen nick ile değiştirildikten sonra...
    python eksiyedek.py
    
Notlar:
* Girdi içindeki URL'ler dosyaya tarayıcıda görüldüğü gibi yazılmakta. Örneğin https://www.tandfonline.com/doi/abs/10.1080/00224540903365554 şeklindeki bir URL https://www.tandfonline.com/…1080/00224540903365554 şeklinde.
* Girdi tarihleri orijinal XML dosyası içerisinde saniye kısmını da içerse de kullanıcıların o bilgiye erişimi olmadığı için saniye yerine 00 yazılmakta. Örneğin 2021-07-15T11:25:18 ise 2021-07-15T11:25:00.
