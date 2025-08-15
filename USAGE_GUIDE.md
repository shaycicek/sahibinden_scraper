# Güncellenmiş Araç Scraper - Kullanım Kılavuzu

Bu kılavuz, gerçek sahibinden.com URL yapısına göre güncellenmiş scraper'ın nasıl kullanılacağını açıklar.

## 🎯 Örnek URL Analizi

Verdiğiniz URL: `https://www.sahibinden.com/renault-clio-1.3-tce/otomatik?a116445=1263354&a4_max=150000`

**URL Yapısı:**
- **Marka**: renault
- **Model**: clio
- **Alt Model**: 1.3-tce
- **Vites**: otomatik (URL path'inde)
- **Kilometre**: Maksimum 150.000 (a4_max=150000)
- **Ağır Hasar**: Hayır (a116445=1263354)

## 🚀 Kullanım Örnekleri

### 1. Temel Kullanım
```bash
python updated_car_scraper.py renault clio
```

### 2. Alt Model ile
```bash
python updated_car_scraper.py renault clio --submodel 1.3-tce
```

### 3. Vites Filtresi
```bash
python updated_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik
```

### 4. Kilometre Filtresi
```bash
python updated_car_scraper.py renault clio --max-km 150000
```

### 5. Ağır Hasar Filtresi
```bash
python updated_car_scraper.py renault clio --heavy-damage hayır
```

### 6. Yıl Aralığı
```bash
python updated_car_scraper.py renault clio --min-year 2020 --max-year 2023
```

### 7. Fiyat Aralığı
```bash
python updated_car_scraper.py renault clio --min-price 200000 --max-price 500000
```

### 8. Tüm Filtreleri Birlikte (Örnek URL'ye Uygun)
```bash
python updated_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır
```

## 📋 Tüm Filtre Seçenekleri

### Temel Parametreler
- `brand`: Araç markası (zorunlu)
- `model`: Araç modeli (zorunlu)
- `--submodel`: Alt model (opsiyonel)

### Filtreler
- `--transmission`: Vites tipi (`otomatik` veya `manuel`)
- `--heavy-damage`: Ağır hasar durumu (`evet` veya `hayır`)
- `--exclude-damage`: Kaput değişen ve boyalı araçları hariç tut
- `--max-km`: Maksimum kilometre
- `--min-km`: Minimum kilometre
- `--max-year`: Maksimum model yılı
- `--min-year`: Minimum model yılı
- `--max-price`: Maksimum fiyat (TL)
- `--min-price`: Minimum fiyat (TL)

### Diğer Seçenekler
- `--max-pages`: Maksimum sayfa sayısı (varsayılan: 5)
- `--output-format`: Çıktı formatı (`csv`, `json`, `both`)

## 🔧 URL Yapısı

Scraper şu URL yapısını kullanır:
```
https://www.sahibinden.com/{marka}-{model}-{alt-model}/{vites}?{parametreler}
```

### Örnek URL'ler:
```
# Temel arama
https://www.sahibinden.com/renault-clio

# Alt model ile
https://www.sahibinden.com/renault-clio-1.3-tce

# Vites ile
https://www.sahibinden.com/renault-clio-1.3-tce/otomatik

# Filtreler ile
https://www.sahibinden.com/renault-clio-1.3-tce/otomatik?a4_max=150000&a116445=1263354
```

## 📊 Çıktı Formatları

### CSV Dosyası (`filtered_cars.csv`)
- Fiyat, model yılı, marka, model
- Vites tipi, yakıt, kilometre
- Hasar durumu, konum bilgileri
- Sahibinden.com linki

### JSON Dosyası (`filtered_cars.json`)
- Tüm detayları JSON formatında
- Programatik kullanım için ideal

## 🧪 Test Örnekleri

### Test 1: Renault Clio 1.3 TCe Otomatik
```bash
python updated_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 2
```

### Test 2: Ford Focus Manuel
```bash
python updated_car_scraper.py ford focus --transmission manuel --min-year 2018 --max-pages 2
```

### Test 3: Volkswagen Golf
```bash
python updated_car_scraper.py volkswagen golf --max-price 300000 --min-year 2020 --max-pages 2
```

## ⚠️ Önemli Notlar

1. **Sorumlu Kullanım**: Rate limiting uygulanır (1-3 saniye bekleme)
2. **URL Yapısı**: Gerçek sahibinden.com URL yapısına uygun
3. **Filtre Parametreleri**: Gerçek site parametreleri kullanılır
4. **Hata Yönetimi**: Çoklu HTML selector desteği
5. **Session Yönetimi**: Verimli bağlantı yönetimi

## 🔍 Sorun Giderme

### "No cars found" Hatası
- Marka/model adını kontrol edin
- Alt model adını doğru yazdığınızdan emin olun
- Filtreleri çok kısıtlayıcı olabilir

### URL Hatası
- Marka ve model adlarını küçük harfle yazın
- Alt model adında tire (-) kullanın
- Özel karakterlerden kaçının

### Bağlantı Hatası
- İnternet bağlantınızı kontrol edin
- Sahibinden.com erişilebilir mi kontrol edin
- Proxy kullanıyorsanız ayarları kontrol edin

## 📈 Performans İpuçları

1. **Sayfa Sayısını Sınırlayın**: `--max-pages 3` ile test edin
2. **Filtreleri Kademeli Ekleyin**: Önce temel arama, sonra filtreler
3. **Çıktı Formatını Seçin**: Sadece CSV için `--output-format csv`
4. **Hata Durumunda**: Birkaç dakika bekleyip tekrar deneyin
