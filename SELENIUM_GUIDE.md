# 🚗 Selenium Tabanlı Araç Scraper - Kullanım Kılavuzu

Bu kılavuz, bot korumasını aşmak için Selenium WebDriver kullanan gelişmiş araç scraper'ının nasıl kurulacağını ve kullanılacağını açıklar.

## 🎯 Neden Selenium?

### ❌ Requests Kütüphanesi Sorunları
- 403 Forbidden hatası
- Bot koruması tarafından engellenme
- IP tabanlı kısıtlamalar

### ✅ Selenium Avantajları
- Gerçek tarayıcı simülasyonu
- JavaScript desteği
- Bot korumasını aşma
- İnsan davranışı simülasyonu

## 📋 Gereksinimler

### 1. Python Kütüphaneleri
```bash
pip install selenium==4.15.2
pip install beautifulsoup4
pip install requests
```

### 2. Chrome WebDriver
Chrome tarayıcısının yüklü olması gerekiyor. WebDriver otomatik olarak indirilecek.

## 🚀 Kurulum

### 1. Kütüphaneleri Yükle
```bash
pip install -r requirements.txt
```

### 2. Chrome Tarayıcısı
- Google Chrome'un yüklü olduğundan emin olun
- WebDriver otomatik olarak yönetilecek

## 🎮 Kullanım Örnekleri

### 1. Temel Kullanım
```bash
python selenium_car_scraper.py renault clio
```

### 2. Alt Model ile
```bash
python selenium_car_scraper.py renault clio --submodel 1.3-tce
```

### 3. Vites Filtresi
```bash
python selenium_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik
```

### 4. Kilometre Filtresi
```bash
python selenium_car_scraper.py renault clio --max-km 150000
```

### 5. Ağır Hasar Filtresi
```bash
python selenium_car_scraper.py renault clio --heavy-damage hayır
```

### 6. Yıl Aralığı
```bash
python selenium_car_scraper.py renault clio --min-year 2020 --max-year 2023
```

### 7. Fiyat Aralığı
```bash
python selenium_car_scraper.py renault clio --min-price 200000 --max-price 500000
```

### 8. Tüm Filtreleri Birlikte
```bash
python selenium_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 2
```

### 9. Görünmez Mod (Headless)
```bash
python selenium_car_scraper.py renault clio --headless
```

## 📋 Tüm Parametreler

### Zorunlu Parametreler
- `brand`: Araç markası (örn: renault, ford, volkswagen)
- `model`: Araç modeli (örn: clio, focus, golf)

### Opsiyonel Parametreler
- `--submodel`: Alt model (örn: 1.3-tce, 1.6-tdi)
- `--transmission`: Vites tipi (`otomatik` veya `manuel`)
- `--heavy-damage`: Ağır hasar durumu (`evet` veya `hayır`)
- `--exclude-damage`: Kaput değişen ve boyalı araçları hariç tut
- `--max-km`: Maksimum kilometre
- `--min-km`: Minimum kilometre
- `--max-year`: Maksimum model yılı
- `--min-year`: Minimum model yılı
- `--max-price`: Maksimum fiyat (TL)
- `--min-price`: Minimum fiyat (TL)
- `--max-pages`: Maksimum sayfa sayısı (varsayılan: 3)
- `--output-format`: Çıktı formatı (`csv`, `json`, `both`)
- `--headless`: Tarayıcıyı görünmez modda çalıştır

## 🔧 Özellikler

### 1. İnsan Davranışı Simülasyonu
- Rastgele bekleme süreleri (2-5 saniye)
- Sayfa yükleme bekleme
- Gerçekçi tarayıcı ayarları

### 2. Bot Koruması Aşma
- WebDriver özelliğini gizleme
- Gerçekçi User-Agent
- Otomasyon belirtilerini kaldırma

### 3. Hata Yönetimi
- Sayfa yükleme zaman aşımı
- Element bulunamama durumu
- Bağlantı hataları

### 4. Çoklu Selector Desteği
- Farklı HTML yapıları için alternatif selector'lar
- Dinamik içerik desteği
- Site değişikliklerine karşı dayanıklılık

## 📊 Çıktı Dosyaları

### CSV Dosyası (`selenium_filtered_cars.csv`)
```
price,year,brand,model,fuel,transmission,km,type,hp,cc,color,damage,heavy_damage,city,county,neighborhood,url
450000,2020,renault,clio,benzin,otomatik,75000,hatchback,130,1333,beyaz,hasarsız,hayır,istanbul,kadıköy,moda,https://...
```

### JSON Dosyası (`selenium_filtered_cars.json`)
```json
[
  {
    "price": "450000",
    "year": "2020",
    "brand": "renault",
    "model": "clio",
    "fuel": "benzin",
    "transmission": "otomatik",
    "km": "75000",
    "url": "https://www.sahibinden.com/..."
  }
]
```

## 🧪 Test Senaryoları

### Test 1: Basit Arama
```bash
python selenium_car_scraper.py renault clio --max-pages 1
```

### Test 2: Filtreli Arama
```bash
python selenium_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 1
```

### Test 3: Görünmez Mod
```bash
python selenium_car_scraper.py ford focus --headless --max-pages 1
```

## ⚠️ Önemli Notlar

### 1. Performans
- Selenium, requests'ten daha yavaştır
- Her sayfa için 2-5 saniye bekleme
- Gerçek tarayıcı açılır

### 2. Sistem Gereksinimleri
- Chrome tarayıcısı gerekli
- Yeterli RAM (en az 2GB)
- İnternet bağlantısı

### 3. Sorumlu Kullanım
- Rate limiting uygulanır
- Sunucuya saygılı davranın
- Çok fazla istek göndermeyin

## 🔍 Sorun Giderme

### Chrome WebDriver Hatası
```
✗ WebDriver başlatılamadı: Message: unknown error: cannot find Chrome binary
```
**Çözüm**: Chrome tarayıcısını yükleyin

### Sayfa Yükleme Hatası
```
❌ Sayfa yüklenemedi, durduruluyor...
```
**Çözüm**: İnternet bağlantınızı kontrol edin

### Element Bulunamama
```
❌ Araç işlenirken hata: NoSuchElementException
```
**Çözüm**: Site yapısı değişmiş olabilir, selector'ları güncelleyin

### Bellek Hatası
```
❌ Beklenmeyen hata: OutOfMemoryError
```
**Çözüm**: Sayfa sayısını azaltın (`--max-pages 1`)

## 📈 Performans İpuçları

### 1. Sayfa Sayısını Sınırlayın
```bash
--max-pages 2  # Sadece 2 sayfa tara
```

### 2. Görünmez Mod Kullanın
```bash
--headless  # Tarayıcı penceresi açılmaz
```

### 3. Çıktı Formatını Seçin
```bash
--output-format csv  # Sadece CSV çıktısı
```

### 4. Filtreleri Kullanın
```bash
--max-km 100000  # Daha az sonuç, daha hızlı işlem
```

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: Renault Clio 1.3 TCe Otomatik
```bash
python selenium_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 2
```

### Senaryo 2: Ford Focus Manuel 2018+
```bash
python selenium_car_scraper.py ford focus --transmission manuel --min-year 2018 --max-pages 2
```

### Senaryo 3: Volkswagen Golf 300K TL Altı
```bash
python selenium_car_scraper.py volkswagen golf --max-price 300000 --min-year 2020 --max-pages 2
```

## 🔒 Güvenlik ve Yasal Uyarılar

1. **Sorumlu Kullanım**: Site kurallarına uyun
2. **Rate Limiting**: Çok hızlı istek göndermeyin
3. **Yasal Sorumluluk**: Kullanıcı sorumluluğundadır
4. **Veri Kullanımı**: Kişisel kullanım için tasarlanmıştır

## 📞 Destek

Sorun yaşarsanız:
1. Chrome tarayıcısının yüklü olduğundan emin olun
2. İnternet bağlantınızı kontrol edin
3. Sayfa sayısını azaltın
4. Filtreleri basitleştirin

---

**Not**: Bu scraper eğitim amaçlıdır ve sorumlu kullanım gerektirir.
