# Gelişmiş Araç Scraper - Filtreleme Özellikli

Bu proje, sahibinden.com sitesinden araç detaylarını çeken ve belirli filtreleme kriterlerine göre sonuçları listeleyen gelişmiş bir web scraper'dır.

## Özellikler

- ✅ **Marka ve Model Filtreleme**: İstediğiniz marka ve model araçları arayın
- ✅ **Vites Tipi Filtreleme**: Otomatik veya manuel vites seçimi
- ✅ **Hasar Durumu Filtreleme**: Ağır hasarlı araçları dahil etme veya hariç tutma
- ✅ **Özel Hasar Filtreleme**: Kaput değişen ve boyalı araçları hariç tutma
- ✅ **Detaylı Bilgi Çıkarma**: Fiyat, konum, teknik özellikler
- ✅ **Çoklu Çıktı Formatı**: CSV ve JSON formatında kaydetme
- ✅ **Link Kaydetme**: Her aracın sahibinden.com linkini kaydetme

## Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

### Gerekli Kütüphaneler
- `requests`: Web istekleri için
- `beautifulsoup4`: HTML parsing için
- `argparse`: Komut satırı argümanları için

## Kullanım

### Temel Kullanım
```bash
python advanced_car_scraper.py [MARKA] [MODEL]
```

### Örnekler

#### 1. Tüm Ford Focus araçları
```bash
python advanced_car_scraper.py ford focus
```

#### 2. Sadece otomatik vites Ford Focus
```bash
python advanced_car_scraper.py ford focus --transmission otomatik
```

#### 3. Sadece manuel vites, ağır hasarlı olmayan Ford Focus
```bash
python advanced_car_scraper.py ford focus --transmission manuel --heavy-damage hayır
```

#### 4. Kaput değişen ve boyalı olmayan araçlar
```bash
python advanced_car_scraper.py ford focus --exclude-damage
```

#### 5. Tüm filtreleri birlikte kullanma
```bash
python advanced_car_scraper.py ford focus --transmission otomatik --heavy-damage hayır --exclude-damage
```

#### 6. Sadece CSV formatında kaydetme
```bash
python advanced_car_scraper.py ford focus --output-format csv
```

#### 7. Sadece JSON formatında kaydetme
```bash
python advanced_car_scraper.py ford focus --output-format json
```

#### 8. Maksimum sayfa sayısını sınırlama
```bash
python advanced_car_scraper.py ford focus --max-pages 5
```

## Filtreleme Seçenekleri

### Vites Tipi (`--transmission`)
- `otomatik`: Sadece otomatik vites araçlar
- `manuel`: Sadece manuel vites araçlar

### Ağır Hasarlı (`--heavy-damage`)
- `evet`: Sadece ağır hasarlı araçlar
- `hayır`: Sadece ağır hasarlı olmayan araçlar

### Hasar Hariç Tutma (`--exclude-damage`)
- Kaput değişen araçları hariç tutar
- Boyalı araçları hariç tutar

### Çıktı Formatı (`--output-format`)
- `csv`: Sadece CSV dosyası
- `json`: Sadece JSON dosyası
- `both`: Her iki format (varsayılan)

### Maksimum Sayfa (`--max-pages`)
- Arama yapılacak maksimum sayfa sayısı (varsayılan: 10)

## Çıktı Dosyaları

### CSV Dosyası (`filtered_cars.csv`)
Şu sütunları içerir:
- `price`: Fiyat (TL)
- `year`: Model yılı
- `brand`: Marka
- `model`: Model
- `fuel`: Yakıt tipi
- `transmission`: Vites tipi
- `km`: Kilometre
- `type`: Araç tipi
- `hp`: Beygir gücü
- `cc`: Motor hacmi
- `color`: Renk
- `damage`: Hasar bilgisi
- `heavy_damage`: Ağır hasarlı durumu
- `city`: Şehir
- `county`: İlçe
- `neighborhood`: Mahalle
- `url`: Sahibinden.com linki

### JSON Dosyası (`filtered_cars.json`)
Tüm araç bilgilerini JSON formatında saklar.

## Örnek Çıktı

```
Searching for ford focus with filters: {'transmission': 'otomatik', 'heavy_damage': False}
Checking page 1: https://www.sahibinden.com/ford-focus?pagingOffset=0&a4_transmission=1&a4_heavy_damage=2
Found 15 cars on page 1
✓ Found matching car: 125.000 TL - 2018 ford focus
✓ Found matching car: 98.500 TL - 2016 ford focus

================================================================================
FOUND 2 MATCHING CARS
================================================================================

1. 2018 ford focus
   Price: 125.000 TL
   Transmission: Otomatik
   Fuel: Benzin
   KM: 45.000
   Location: İstanbul, Kadıköy
   URL: https://www.sahibinden.com/ilan/...
   Heavy Damage: Hayır
   Damage Info: Hasarsız

2. 2016 ford focus
   Price: 98.500 TL
   Transmission: Otomatik
   Fuel: Dizel
   KM: 78.000
   Location: Ankara, Çankaya
   URL: https://www.sahibinden.com/ilan/...
   Heavy Damage: Hayır
   Damage Info: Hasarsız

Saved 2 cars to filtered_cars.csv
Saved 2 cars to filtered_cars.json
```

## Önemli Notlar

⚠️ **Sorumlu Kullanım**: 
- Web scraping yaparken sitenin kullanım şartlarına uygun hareket edin
- Çok hızlı istekler göndermemeye dikkat edin
- Rate limiting uygulayın

⚠️ **Veri Güncelliği**: 
- Sahibinden.com'daki veriler sürekli güncellenir
- Sonuçlar çalıştırma anındaki verileri yansıtır

⚠️ **Hata Durumları**: 
- İnternet bağlantısı sorunları
- Site yapısı değişiklikleri
- Captcha veya erişim engellemeleri

## Sorun Giderme

### "No cars found" Hatası
- Marka/model adını kontrol edin
- Filtreleri çok kısıtlayıcı olabilir
- `--max-pages` değerini artırın

### Bağlantı Hataları
- İnternet bağlantınızı kontrol edin
- Sahibinden.com erişilebilir mi kontrol edin
- Birkaç dakika bekleyip tekrar deneyin

### Veri Eksikliği
- Site yapısı değişmiş olabilir
- Kod güncellemesi gerekebilir

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Sorumlu kullanım için lütfen sahibinden.com'un kullanım şartlarına uyun.
