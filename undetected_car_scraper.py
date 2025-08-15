#!/usr/bin/env python
"""
Undetected ChromeDriver-based Car Scraper for Sahibinden.com
Uses undetected-chromedriver to bypass Cloudflare protection
"""

import sys
import csv
import json
import argparse
import time
import random
from datetime import datetime
from urllib.parse import urljoin

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

class UndetectedCarScraper:
    def __init__(self, headless=False):
        self.filtered_cars = []
        self.driver = None
        self.headless = headless
        self.setup_driver()
        
    def setup_driver(self):
        """Setup undetected ChromeDriver"""
        try:
            options = uc.ChromeOptions()
            
            if self.headless:
                options.add_argument("--headless=new")  # Use new headless mode
                # Additional stealth options for headless mode
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                options.add_argument("--disable-features=VizDisplayCompositor")
                options.add_argument("--disable-ipc-flooding-protection")
                options.add_argument("--disable-renderer-backgrounding")
                options.add_argument("--disable-background-timer-throttling")
                options.add_argument("--disable-backgrounding-occluded-windows")
                options.add_argument("--disable-client-side-phishing-detection")
                options.add_argument("--disable-default-apps")
                options.add_argument("--disable-hang-monitor")
                options.add_argument("--disable-prompt-on-repost")
                options.add_argument("--disable-sync")
                options.add_argument("--force-color-profile=srgb")
                options.add_argument("--metrics-recording-only")
                options.add_argument("--no-first-run")
                options.add_argument("--safebrowsing-disable-auto-update")
                options.add_argument("--enable-automation")
                options.add_argument("--password-store=basic")
                options.add_argument("--use-mock-keychain")
                # Set a realistic user agent
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
            # else:
            #     options.add_argument("--headless")  # Bu satırı kaldırdık
            
            # Additional options for better stealth
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            # options.add_argument("--disable-javascript")  # JavaScript'i etkinleştir
            options.add_argument("--window-size=1920,1080")
            
            # Create undetected driver
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # Execute stealth script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✓ Undetected ChromeDriver başarıyla başlatıldı")
            
        except Exception as e:
            print(f"✗ Undetected ChromeDriver başlatılamadı: {e}")
            print("undetected-chromedriver kütüphanesini yükleyin: pip install undetected-chromedriver")
            sys.exit(1)
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Random delay to simulate human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def build_search_url(self, brand, model, submodel=None, filters=None):
        """Build search URL based on actual sahibinden.com structure"""
        if filters is None:
            filters = {}
        
        # Base URL structure: /brand-model-submodel/transmission
        url_parts = [brand.lower()]
        
        if submodel:
            url_parts.append(f"{model}-{submodel}")
        else:
            url_parts.append(model)
        
        # Add transmission to URL path if specified
        transmission_path = ""
        if filters.get('transmission'):
            if filters['transmission'].lower() == 'otomatik':
                transmission_path = "/otomatik"
            elif filters['transmission'].lower() == 'manuel':
                transmission_path = "/manuel"
        
        # Build base URL
        base_url = f"https://www.sahibinden.com/{'-'.join(url_parts)}{transmission_path}"
        
        # Add query parameters
        params = []
        
        # Add page offset
        page = filters.get('page', 0)
        if page > 0:
            params.append(f"pagingOffset={page * 20}")
        
        # Add transmission filter (if not in path)
        if filters.get('transmission') and not transmission_path:
            if filters['transmission'].lower() == 'otomatik':
                params.append("a4_transmission=1")
            elif filters['transmission'].lower() == 'manuel':
                params.append("a4_transmission=2")
        
        # Add heavy damage filter
        if filters.get('heavy_damage') is not None:
            if filters['heavy_damage']:
                params.append("a116445=1263353")  # Evet
            else:
                params.append("a116445=1263354")  # Hayır
        
        # Add maximum kilometer filter
        if filters.get('max_km'):
            params.append(f"a4_max={filters['max_km']}")
        
        # Add minimum kilometer filter
        if filters.get('min_km'):
            params.append(f"a4_min={filters['min_km']}")
        
        # Add year range filters
        if filters.get('min_year'):
            params.append(f"a4_min_year={filters['min_year']}")
        
        if filters.get('max_year'):
            params.append(f"a4_max_year={filters['max_year']}")
        
        # Add price range filters
        if filters.get('min_price'):
            params.append(f"a4_min_price={filters['min_price']}")
        
        if filters.get('max_price'):
            params.append(f"a4_max_price={filters['max_price']}")
        
        # Combine parameters
        if params:
            base_url += "?" + "&".join(params)
        
        return base_url
    
    def wait_for_page_load(self, timeout=15):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Additional wait for dynamic content
            time.sleep(3)
            return True
        except TimeoutException:
            print("Sayfa yüklenme zaman aşımı")
            return False
    
    def wait_for_cloudflare(self, timeout=60):
        """Wait for Cloudflare challenge to complete"""
        try:
            print("  🔄 Cloudflare doğrulaması bekleniyor...")
            # Wait for the challenge to disappear
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.ID, "challenge-error-text"))
            )
            # Additional wait for page to fully load
            time.sleep(5)
            print("  ✅ Cloudflare doğrulaması tamamlandı")
            return True
        except TimeoutException:
            print("  ❌ Cloudflare doğrulaması zaman aşımı")
            return False
    
    def extract_car_details(self, url):
        """Extract detailed information from car page"""
        try:
            print(f"  Araç detayları alınıyor: {url}")
            self.driver.get(url)
            
            if not self.wait_for_page_load():
                return None
            
            # Wait for Cloudflare if present
            if "cloudflare" in self.driver.page_source.lower():
                if not self.wait_for_cloudflare():
                    return None
            
            # Random delay to simulate human behavior
            self.random_delay(1, 2)
            
            car_info = {}
            
            # Get price
            price_selectors = [
                "span.classified-price-wrapper",
                "div.classifiedInfo h3",
                "div.price-info h3",
                "span.price",
                "div.price h3",
                "h3.price",
                ".classifiedInfo h3"
            ]
            
            price = None
            for selector in price_selectors:
                try:
                    price_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    if 'TL' in price_text:
                        price = price_text.replace('TL', '').strip()
                        break
                except NoSuchElementException:
                    continue
            
            car_info['price'] = price or 'N/A'
            
            # Get location information
            try:
                location_elements = self.driver.find_elements(By.CSS_SELECTOR, "h2 a[href*='/renault-clio']")
                if len(location_elements) >= 3:
                    car_info['city'] = location_elements[0].text.strip()
                    car_info['county'] = location_elements[1].text.strip()
                    car_info['neighborhood'] = location_elements[2].text.strip()
            except:
                pass
            
            # Get detailed specifications
            try:
                spec_items = self.driver.find_elements(By.CSS_SELECTOR, "li")
                for item in spec_items:
                    try:
                        strong = item.find_element(By.TAG_NAME, "strong")
                        span = item.find_element(By.TAG_NAME, "span")
                        key = strong.text.strip().lower()
                        value = span.text.strip()
                        
                        if key == "yıl":
                            car_info['year'] = value
                        elif key == "km":
                            car_info['km'] = value
                        elif key == "vites":
                            car_info['vites'] = value
                        elif key == "yakıt tipi":
                            car_info['yakıt'] = value
                        elif key == "motor hacmi":
                            car_info['cc'] = value
                        elif key == "motor gücü":
                            car_info['hp'] = value
                        elif key == "renk":
                            car_info['color'] = value
                        elif key == "hasar durumu":
                            car_info['hasar'] = value
                        elif key == "ağır hasarlı":
                            car_info['ağır hasarlı'] = value
                    except:
                        continue
            except:
                pass
            
            # Get car link
            car_info['url'] = url
            
            # Add brand and model if not found
            if 'brand' not in car_info:
                car_info['brand'] = 'Renault'
            if 'model' not in car_info:
                car_info['model'] = 'Clio'
            
            return car_info
            
        except Exception as e:
            print(f"  Araç detayları alınırken hata: {e}")
            return None
    
    def check_filters(self, car_info, filters):
        """Check if car matches the specified filters"""
        if not car_info:
            return False
            
        # Check transmission type
        if filters.get('transmission'):
            transmission = car_info.get('vites', '').lower()
            if filters['transmission'].lower() not in transmission:
                return False
        
        # Check heavy damage
        if filters.get('heavy_damage') is not None:
            damage = car_info.get('ağır hasarlı', '').lower()
            if filters['heavy_damage'] and 'evet' not in damage:
                return False
            elif not filters['heavy_damage'] and 'evet' in damage:
                return False
        
        # Check for specific damage conditions (kaput değişen değil ve boyalı değil)
        if filters.get('exclude_damage'):
            damage_info = car_info.get('hasar', '').lower()
            if 'kaput değişen' in damage_info or 'boyalı' in damage_info:
                return False
        
        return True
    
    def get_filtered_cars(self, brand, model, submodel=None, filters=None, max_pages=10):
        """Get cars with applied filters using undetected ChromeDriver"""
        if filters is None:
            filters = {}
            
        print(f"🔍 {brand} {model} {submodel or ''} için arama yapılıyor...")
        print(f"📋 Filtreler: {filters}")
        
        page = 0
        while page < max_pages:
            # Update page in filters
            filters['page'] = page
            
            # Build URL
            url = self.build_search_url(brand, model, submodel, filters)
            print(f"\n📄 Sayfa {page + 1} kontrol ediliyor: {url}")
            
            try:
                self.driver.get(url)
                
                if not self.wait_for_page_load():
                    print("❌ Sayfa yüklenemedi, durduruluyor...")
                    break
                
                # Wait for Cloudflare if present
                if "cloudflare" in self.driver.page_source.lower():
                    if not self.wait_for_cloudflare():
                        print("❌ Cloudflare doğrulaması başarısız, durduruluyor...")
                        break
                
                # Random delay
                self.random_delay(1, 2)
                
                # Debug: Save page source for analysis
                try:
                    with open(f"debug_page_{page + 1}.html", "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                    print(f"  🔍 Debug: Sayfa kaynağı debug_page_{page + 1}.html dosyasına kaydedildi")
                except Exception as e:
                    print(f"  ⚠️ Debug dosyası kaydedilemedi: {e}")
                
                # Find car links
                car_links = []
                link_selectors = [
                    "a.classifiedTitle",
                    "a.car-title",
                    "div.car-item a",
                    "h3 a",
                    ".classifiedTitle",
                    "tr.searchResultsItem a",
                    "a[href*='/ilan/']",
                    "td.searchResultsLargeThumbnail a",
                    "td.searchResultsLargeThumbnail h3 a",
                    "div.searchResultsItem a",
                    "div.searchResultsItem h3 a",
                    "a[data-id]",
                    "tr a[href*='/ilan/']",
                    "div.listing-list-item a",
                    "div.listing-list-item h3 a",
                    "div[data-id='car-list'] a",
                    "div[data-id='search-results'] a",
                    # Headless mod için ek selector'lar
                    "a[href*='ilan']",
                    "a[href*='detay']",
                    "div a[href*='/ilan/']",
                    "table a[href*='/ilan/']",
                    "tr a[href*='/ilan/']",
                    "div.searchResultsItem a",
                    "div.searchResultsLargeThumbnail a",
                    "td a[href*='/ilan/']",
                    "li a[href*='/ilan/']"
                ]
                
                for selector in link_selectors:
                    try:
                        links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if links:
                            print(f"  ✅ Selector çalıştı: {selector} - {len(links)} link bulundu")
                            car_links = links
                            break
                        else:
                            print(f"  ⚠️ Selector boş: {selector}")
                    except Exception as e:
                        print(f"  ❌ Selector hatası: {selector} - {e}")
                        continue
                
                if not car_links:
                    print("❌ Daha fazla araç bulunamadı")
                    break
                    
                print(f"✅ Sayfa {page + 1}'de {len(car_links)} araç bulundu")
                
                # Process each car
                print(f"  🔄 {len(car_links)} araç işleniyor...")
                processed_count = 0
                for i, link in enumerate(car_links):
                    try:
                        href = link.get_attribute('href')
                        if href:
                            print(f"    📋 Araç {i+1}/{len(car_links)} işleniyor...")
                            
                            # Try to extract car details with better error handling
                            try:
                                car_info = self.extract_car_details(href)
                                processed_count += 1
                                
                                if car_info and self.check_filters(car_info, filters):
                                    self.filtered_cars.append(car_info)
                                    print(f"    ✅ Eşleşen araç bulundu: {car_info.get('price', 'N/A')} TL - {car_info.get('year', 'N/A')} {brand} {model}")
                                else:
                                    print(f"    ⚠️ Araç filtrelere uymuyor veya bilgi alınamadı")
                                
                            except Exception as detail_error:
                                print(f"    ❌ Araç detayları alınırken hata: {detail_error}")
                                # Continue with next car instead of breaking
                                continue
                            
                            # Shorter delay between car pages
                            self.random_delay(1, 2)
                            
                            # Add a small progress indicator
                            if processed_count % 5 == 0:
                                print(f"    📊 {processed_count} araç işlendi...")
                                
                    except Exception as e:
                        print(f"    ❌ Araç linki işlenirken hata: {e}")
                        continue
                
                print(f"    ✅ Toplam {processed_count} araç işlendi")
                
                page += 1
                
            except Exception as e:
                print(f"❌ Sayfa işlenirken hata: {e}")
                break
        
        print(f"\n📊 Toplam {len(self.filtered_cars)} eşleşen araç bulundu")
        return self.filtered_cars
    
    def save_to_csv(self, filename="undetected_filtered_cars.csv"):
        """Save filtered cars to CSV"""
        if not self.filtered_cars:
            print("❌ Kaydedilecek araç yok")
            return
            
        # Define CSV headers
        headers = [
            'price', 'year', 'brand', 'model', 'fuel', 'transmission', 'km', 
            'type', 'hp', 'cc', 'color', 'damage', 'heavy_damage', 'city', 
            'county', 'neighborhood', 'url'
        ]
        
        with open(filename, mode='w', encoding="utf-8", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            
            for car in self.filtered_cars:
                # Clean up data for CSV
                csv_row = {}
                for header in headers:
                    if header == 'transmission':
                        csv_row[header] = car.get('vites', '')
                    elif header == 'heavy_damage':
                        csv_row[header] = car.get('ağır hasarlı', '')
                    elif header == 'damage':
                        csv_row[header] = car.get('hasar', '')
                    else:
                        csv_row[header] = car.get(header, '')
                writer.writerow(csv_row)
        
        print(f"💾 {len(self.filtered_cars)} araç {filename} dosyasına kaydedildi")
    
    def save_to_json(self, filename="undetected_filtered_cars.json"):
        """Save filtered cars to JSON"""
        if not self.filtered_cars:
            print("❌ Kaydedilecek araç yok")
            return
            
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.filtered_cars, file, ensure_ascii=False, indent=2)
        
        print(f"💾 {len(self.filtered_cars)} araç {filename} dosyasına kaydedildi")
    
    def print_summary(self):
        """Print a summary of found cars"""
        if not self.filtered_cars:
            print("❌ Kriterlerinize uygun araç bulunamadı")
            return
            
        print(f"\n{'='*80}")
        print(f"🎯 {len(self.filtered_cars)} EŞLEŞEN ARAÇ BULUNDU")
        print(f"{'='*80}")
        
        for i, car in enumerate(self.filtered_cars, 1):
            print(f"\n{i}. {car.get('year', 'N/A')} {car.get('brand', 'N/A')} {car.get('model', 'N/A')}")
            print(f"   💰 Fiyat: {car.get('price', 'N/A')} TL")
            print(f"   ⚙️  Vites: {car.get('vites', 'N/A')}")
            print(f"   ⛽ Yakıt: {car.get('yakıt', 'N/A')}")
            print(f"   🛣️  KM: {car.get('km', 'N/A')}")
            print(f"   📍 Konum: {car.get('city', 'N/A')}, {car.get('county', 'N/A')}")
            print(f"   🔗 URL: {car.get('url', 'N/A')}")
            print(f"   🚨 Ağır Hasar: {car.get('ağır hasarlı', 'N/A')}")
            print(f"   🔧 Hasar Bilgisi: {car.get('hasar', 'N/A')}")
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            print("🔒 WebDriver kapatıldı")

def main():
    parser = argparse.ArgumentParser(description='Undetected ChromeDriver-based Car Scraper for Sahibinden.com')
    parser.add_argument('brand', help='Araç markası (örn: renault)')
    parser.add_argument('model', help='Araç modeli (örn: clio)')
    parser.add_argument('--submodel', help='Alt model (örn: 1.3-tce)')
    parser.add_argument('--transmission', choices=['otomatik', 'manuel'], 
                       help='Vites tipi filtresi')
    parser.add_argument('--heavy-damage', choices=['evet', 'hayır'], 
                       help='Ağır hasar filtresi')
    parser.add_argument('--exclude-damage', action='store_true',
                       help='Kaput değişen ve boyalı araçları hariç tut')
    parser.add_argument('--max-km', type=int, help='Maksimum kilometre')
    parser.add_argument('--min-km', type=int, help='Minimum kilometre')
    parser.add_argument('--max-year', type=int, help='Maksimum yıl')
    parser.add_argument('--min-year', type=int, help='Minimum yıl')
    parser.add_argument('--max-price', type=int, help='Maksimum fiyat')
    parser.add_argument('--min-price', type=int, help='Minimum fiyat')
    parser.add_argument('--max-pages', type=int, default=3,
                       help='Maksimum sayfa sayısı')
    parser.add_argument('--output-format', choices=['csv', 'json', 'both'], default='both',
                       help='Çıktı formatı')
    parser.add_argument('--headless', action='store_true',
                       help='Tarayıcıyı görünmez modda çalıştır')
    
    args = parser.parse_args()
    
    # Convert arguments to filters
    filters = {}
    if args.transmission:
        filters['transmission'] = args.transmission
    if args.heavy_damage:
        filters['heavy_damage'] = args.heavy_damage == 'evet'
    if args.exclude_damage:
        filters['exclude_damage'] = True
    if args.max_km:
        filters['max_km'] = args.max_km
    if args.min_km:
        filters['min_km'] = args.min_km
    if args.max_year:
        filters['max_year'] = args.max_year
    if args.min_year:
        filters['min_year'] = args.min_year
    if args.max_price:
        filters['max_price'] = args.max_price
    if args.min_price:
        filters['min_price'] = args.min_price
    
    # Create scraper and run
    scraper = UndetectedCarScraper(headless=args.headless)
    
    try:
        cars = scraper.get_filtered_cars(args.brand, args.model, args.submodel, filters, args.max_pages)
        
        if cars:
            scraper.print_summary()
            
            # Save results
            if args.output_format in ['csv', 'both']:
                scraper.save_to_csv()
            if args.output_format in ['json', 'both']:
                scraper.save_to_json()
        else:
            print("❌ Kriterlerinize uygun araç bulunamadı")
    
    except KeyboardInterrupt:
        print("\n⏹️  Kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
