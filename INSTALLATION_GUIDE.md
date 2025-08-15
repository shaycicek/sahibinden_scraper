# Kurulum Rehberi - Gelişmiş Araç Scraper

Bu rehber, gelişmiş araç scraper'ını çalıştırmak için gerekli adımları içerir.

## 1. Python Kurulumu

### Windows için:
1. **Python'u İndirin**: https://www.python.org/downloads/
2. **Kurulum Sırasında**: "Add Python to PATH" seçeneğini işaretleyin
3. **Kurulumu Tamamlayın**: Tüm varsayılan ayarları kabul edin

### Kurulumu Doğrulayın:
```bash
python --version
# veya
py --version
```

## 2. Gerekli Kütüphaneleri Yükleyin

Proje klasörüne gidin ve şu komutu çalıştırın:
```bash
pip install -r requirements.txt
```

### Manuel Kurulum:
```bash
pip install requests beautifulsoup4
```

## 3. Test Edin

### Basit Test:
```bash
python simple_test.py
```

### Gelişmiş Test:
```bash
python test_scraper.py
```

## 4. Scraper'ı Kullanın

### Temel Kullanım:
```bash
python advanced_car_scraper_fixed.py ford focus
```

### Filtreleme ile:
```bash
# Sadece otomatik vites
python advanced_car_scraper_fixed.py ford focus --transmission otomatik

# Ağır hasarlı olmayan
python advanced_car_scraper_fixed.py ford focus --heavy-damage hayır

# Kaput değişen ve boyalı olmayan
python advanced_car_scraper_fixed.py ford focus --exclude-damage

# Tüm filtreleri birlikte
python advanced_car_scraper_fixed.py ford focus --transmission otomatik --heavy-damage hayır --exclude-damage
```

## 5. Sorun Giderme

### Python Bulunamadı Hatası:
- Python'u PATH'e eklediğinizden emin olun
- Komut istemini yeniden başlatın
- `py` komutunu deneyin: `py --version`

### Kütüphane Kurulum Hatası:
```bash
# Pip'i güncelleyin
python -m pip install --upgrade pip

# Kütüphaneleri tek tek kurun
pip install requests
pip install beautifulsoup4
```

### İnternet Bağlantı Hatası:
- İnternet bağlantınızı kontrol edin
- Sahibinden.com erişilebilir mi kontrol edin
- Proxy kullanıyorsanız ayarları kontrol edin

### Site Yapısı Değişikliği:
- Kod güncellemesi gerekebilir
- `advanced_car_scraper_fixed.py` dosyasını kullanın

## 6. Çıktı Dosyaları

Scraper çalıştıktan sonra şu dosyalar oluşur:
- `filtered_cars.csv`: CSV formatında araç listesi
- `filtered_cars.json`: JSON formatında araç listesi

## 7. Önemli Notlar

⚠️ **Sorumlu Kullanım**:
- Çok hızlı istekler göndermeyin
- Rate limiting uygulayın
- Sahibinden.com'un kullanım şartlarına uyun

⚠️ **Veri Güncelliği**:
- Sonuçlar çalıştırma anındaki verileri yansıtır
- Veriler sürekli güncellenir

## 8. Destek

Sorun yaşarsanız:
1. `simple_test.py` scriptini çalıştırın
2. Hata mesajlarını kontrol edin
3. Python ve kütüphane versiyonlarını kontrol edin
4. İnternet bağlantınızı test edin
