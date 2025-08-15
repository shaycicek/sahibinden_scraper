#!/usr/bin/env python
"""
Selenium-based Car Scraper for Sahibinden.com
Uses real browser simulation to bypass bot protection
"""

import sys
import csv
import json
import argparse
import time
import random
from datetime import datetime
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

class SeleniumCarScraper:
    def __init__(self, headless=False):
        self.filtered_cars = []
        self.driver = None
        self.headless = headless
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome WebDriver with realistic options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Realistic browser settings
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set realistic window size
        chrome_options.add_argument("--window-size=1920,1080")
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Fix for user data directory issue
        import tempfile
        import os
        temp_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✓ Chrome WebDriver başarıyla başlatıldı")
        except Exception as e:
            print(f"✗ WebDriver başlatılamadı: {e}")
            print("Chrome WebDriver'ı yüklediğinizden emin olun: https://chromedriver.chromium.org/")
            sys.exit(1)
    
    def random_delay(self, min_seconds=2, max_seconds=5):
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
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Additional wait for dynamic content
            time.sleep(2)
            return True
        except TimeoutException:
            print("Sayfa yüklenme zaman aşımı")
            return False
    
    def extract_car_details(self, url):
        """Extract detailed information from car page using Selenium"""
        try:
            print(f"  Araç detayları alınıyor: {url}")
            self.driver.get(url)
            
            if not self.wait_for_page_load():
                return None
            
            # Random delay to simulate human behavior
            self.random_delay(1, 3)
            
            car_info = {}
            
            # Get price
            price_selectors = [
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
            address_selectors = [
                "div.classifiedInfo a",
                "div.location-info a",
                "div.address a",
                ".classifiedInfo a"
            ]
            
            for selector in address_selectors:
                try:
                    address_links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(address_links) >= 4:
                        car_info['city'] = address_links[1].text.strip()
                        car_info['county'] = address_links[2].text.strip()
                        car_info['neighborhood'] = address_links[3].text.strip()
                        break
                except:
                    continue
            
            # Get detailed specifications
            spec_selectors = [
                "ul.classifiedInfoList li",
                "div.specs li",
                "div.car-details li",
                ".classifiedInfoList li"
            ]
            
            for selector in spec_selectors:
                try:
                    spec_items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if spec_items:
                        for item in spec_items:
                            try:
                                span = item.find_element(By.TAG_NAME, "span")
                                text = span.text.strip()
                                if ":" in text:
                                    key, value = text.split(":", 1)
                                    car_info[key.strip().lower()] = value.strip()
                            except:
                                continue
                        break
                except:
                    continue
            
            # Get car link
            car_info['url'] = url
            
            # Add brand and model if not found
            if 'brand' not in car_info:
                car_info['brand'] = 'N/A'
            if 'model' not in car_info:
                car_info['model'] = 'N/A'
            
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
        """Get cars with applied filters using Selenium"""
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
                
                # Debug: Save page source to analyze HTML structure
                try:
                    with open(f"debug_page_{page + 1}.html", "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                    print(f"  🔍 Debug: Sayfa kaynağı debug_page_{page + 1}.html dosyasına kaydedildi")
                except Exception as e:
                    print(f"  ⚠️ Debug dosyası kaydedilemedi: {e}")
                
                # Random delay
                self.random_delay(2, 4)
                
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
                    "div.listing-list-item h3 a"
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
                for i, link in enumerate(car_links[:5]):  # Limit to 5 cars per page for testing
                    try:
                        href = link.get_attribute('href')
                        if href:
                            car_info = self.extract_car_details(href)
                            
                            if car_info and self.check_filters(car_info, filters):
                                self.filtered_cars.append(car_info)
                                print(f"  ✅ Eşleşen araç bulundu: {car_info.get('price', 'N/A')} TL - {car_info.get('year', 'N/A')} {brand} {model}")
                            
                            # Random delay between car pages
                            self.random_delay(1, 2)
                    except Exception as e:
                        print(f"  ❌ Araç işlenirken hata: {e}")
                        continue
                
                page += 1
                
            except Exception as e:
                print(f"❌ Sayfa işlenirken hata: {e}")
                break
        
        print(f"\n📊 Toplam {len(self.filtered_cars)} eşleşen araç bulundu")
        return self.filtered_cars
    
    def save_to_csv(self, filename="selenium_filtered_cars.csv"):
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
    
    def save_to_json(self, filename="selenium_filtered_cars.json"):
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
    parser = argparse.ArgumentParser(description='Selenium-based Car Scraper for Sahibinden.com')
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
    scraper = SeleniumCarScraper(headless=args.headless)
    
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
