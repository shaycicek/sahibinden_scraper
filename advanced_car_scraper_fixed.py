#!/usr/bin/env python
import sys
import csv
import json
import argparse
import time
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sahibinden.com{}"
car_url = "https://www.sahibinden.com/{}-{}?{}"

class CarScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.filtered_cars = []
        self.session = requests.Session()
        
    def return_soup(self, url):
        """Make get request and return html soup"""
        try:
            # Add delay to be respectful to the server
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                return soup
            else:
                print(f"Error accessing {url}")
                print(f"Status Code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            return None

    def clean_value(self, value):
        """Cleans values like 125 hp, 1600 cc etc."""
        if not value:
            return ""
        
        clean_these = [" hp", " cc", " cm3", " - "]
        for clean_this in clean_these:
            if clean_this == " - ":
                val_list = value.lower().split(clean_this)
                if len(val_list) > 1:
                    try:
                        value = str((int(val_list[0]) + int(val_list[1])) // 2)
                    except ValueError:
                        value = val_list[0]
                    continue
            value = value.lower().split(clean_this)[0]
        return value.strip()

    def extract_car_details(self, url):
        """Extract detailed information from car page"""
        soup = self.return_soup(url)
        if not soup:
            return None
            
        try:
            # Extract basic info
            car_info = {}
            
            # Get price - try multiple selectors
            price = None
            price_selectors = [
                "div.classifiedInfo h3",
                "div.price-info h3",
                "span.price",
                "div.price h3"
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.text.strip()
                    if 'TL' in price_text:
                        price = price_text.replace('TL', '').strip()
                        break
            
            car_info['price'] = price or 'N/A'
            
            # Get address - try multiple approaches
            address_selectors = [
                "div.classifiedInfo a",
                "div.location-info a",
                "div.address a"
            ]
            
            for selector in address_selectors:
                address_links = soup.select(selector)
                if len(address_links) >= 4:
                    car_info['city'] = address_links[1].text.strip()
                    car_info['county'] = address_links[2].text.strip()
                    car_info['neighborhood'] = address_links[3].text.strip()
                    break
            
            # Get detailed specs - try multiple selectors
            spec_selectors = [
                "ul.classifiedInfoList li",
                "div.specs li",
                "div.car-details li"
            ]
            
            for selector in spec_selectors:
                spec_items = soup.select(selector)
                if spec_items:
                    for item in spec_items:
                        span = item.find("span")
                        if span:
                            text = span.text.strip()
                            if ":" in text:
                                key, value = text.split(":", 1)
                                car_info[key.strip().lower()] = value.strip()
                    break
            
            # Get car link
            car_info['url'] = url
            
            # Add brand and model if not found
            if 'brand' not in car_info:
                car_info['brand'] = 'N/A'
            if 'model' not in car_info:
                car_info['model'] = 'N/A'
            
            return car_info
            
        except Exception as e:
            print(f"Error extracting details from {url}: {e}")
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

    def get_filtered_cars(self, brand, model, filters=None, max_pages=10):
        """Get cars with applied filters"""
        if filters is None:
            filters = {}
            
        print(f"Searching for {brand} {model} with filters: {filters}")
        
        page = 0
        while page < max_pages:
            # Construct URL with filters
            url_params = f"pagingOffset={page * 20}"
            
            # Add transmission filter to URL if specified
            if filters.get('transmission'):
                if filters['transmission'].lower() == 'otomatik':
                    url_params += "&a4_transmission=1"
                elif filters['transmission'].lower() == 'manuel':
                    url_params += "&a4_transmission=2"
            
            # Add heavy damage filter to URL if specified
            if filters.get('heavy_damage') is not None:
                if filters['heavy_damage']:
                    url_params += "&a4_heavy_damage=1"
                else:
                    url_params += "&a4_heavy_damage=2"
            
            url = car_url.format(brand, model, url_params)
            print(f"Checking page {page + 1}: {url}")
            
            soup = self.return_soup(url)
            if not soup:
                print("Failed to load page, stopping...")
                break
                
            # Find car links - try multiple selectors
            car_links = []
            link_selectors = [
                "a.classifiedTitle",
                "a.car-title",
                "div.car-item a",
                "h3 a"
            ]
            
            for selector in link_selectors:
                car_links = soup.select(selector)
                if car_links:
                    break
            
            if not car_links:
                print("No more cars found")
                break
                
            print(f"Found {len(car_links)} cars on page {page + 1}")
            
            # Process each car
            for link in car_links:
                href = link.get('href')
                if href:
                    if href.startswith('/'):
                        car_url_full = BASE_URL.format(href)
                    else:
                        car_url_full = href
                    
                    car_info = self.extract_car_details(car_url_full)
                    
                    if car_info and self.check_filters(car_info, filters):
                        self.filtered_cars.append(car_info)
                        print(f"✓ Found matching car: {car_info.get('price', 'N/A')} TL - {car_info.get('year', 'N/A')} {brand} {model}")
            
            page += 1
            
        print(f"\nTotal matching cars found: {len(self.filtered_cars)}")
        return self.filtered_cars

    def save_to_csv(self, filename="filtered_cars.csv"):
        """Save filtered cars to CSV"""
        if not self.filtered_cars:
            print("No cars to save")
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
        
        print(f"Saved {len(self.filtered_cars)} cars to {filename}")

    def save_to_json(self, filename="filtered_cars.json"):
        """Save filtered cars to JSON"""
        if not self.filtered_cars:
            print("No cars to save")
            return
            
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.filtered_cars, file, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(self.filtered_cars)} cars to {filename}")

    def print_summary(self):
        """Print a summary of found cars"""
        if not self.filtered_cars:
            print("No cars found matching your criteria")
            return
            
        print(f"\n{'='*80}")
        print(f"FOUND {len(self.filtered_cars)} MATCHING CARS")
        print(f"{'='*80}")
        
        for i, car in enumerate(self.filtered_cars, 1):
            print(f"\n{i}. {car.get('year', 'N/A')} {car.get('brand', 'N/A')} {car.get('model', 'N/A')}")
            print(f"   Price: {car.get('price', 'N/A')} TL")
            print(f"   Transmission: {car.get('vites', 'N/A')}")
            print(f"   Fuel: {car.get('yakıt', 'N/A')}")
            print(f"   KM: {car.get('km', 'N/A')}")
            print(f"   Location: {car.get('city', 'N/A')}, {car.get('county', 'N/A')}")
            print(f"   URL: {car.get('url', 'N/A')}")
            print(f"   Heavy Damage: {car.get('ağır hasarlı', 'N/A')}")
            print(f"   Damage Info: {car.get('hasar', 'N/A')}")

def main():
    parser = argparse.ArgumentParser(description='Advanced Car Scraper with Filters')
    parser.add_argument('brand', help='Car brand (e.g., ford)')
    parser.add_argument('model', help='Car model (e.g., focus)')
    parser.add_argument('--transmission', choices=['otomatik', 'manuel'], 
                       help='Transmission type filter')
    parser.add_argument('--heavy-damage', choices=['evet', 'hayır'], 
                       help='Heavy damage filter')
    parser.add_argument('--exclude-damage', action='store_true',
                       help='Exclude cars with kaput değişen or boyalı')
    parser.add_argument('--max-pages', type=int, default=5,
                       help='Maximum number of pages to search')
    parser.add_argument('--output-format', choices=['csv', 'json', 'both'], default='both',
                       help='Output format')
    
    args = parser.parse_args()
    
    # Convert arguments to filters
    filters = {}
    if args.transmission:
        filters['transmission'] = args.transmission
    if args.heavy_damage:
        filters['heavy_damage'] = args.heavy_damage == 'evet'
    if args.exclude_damage:
        filters['exclude_damage'] = True
    
    # Create scraper and run
    scraper = CarScraper()
    cars = scraper.get_filtered_cars(args.brand, args.model, filters, args.max_pages)
    
    if cars:
        scraper.print_summary()
        
        # Save results
        if args.output_format in ['csv', 'both']:
            scraper.save_to_csv()
        if args.output_format in ['json', 'both']:
            scraper.save_to_json()
    else:
        print("No cars found matching your criteria")

if __name__ == "__main__":
    main()
