#!/usr/bin/env python
"""
Test script for the advanced car scraper
This script demonstrates how to use the CarScraper class programmatically
"""

from advanced_car_scraper import CarScraper

def test_basic_search():
    """Test basic search without filters"""
    print("=== Testing Basic Search ===")
    scraper = CarScraper()
    
    # Search for Ford Focus without any filters
    filters = {}
    cars = scraper.get_filtered_cars("ford", "focus", filters, max_pages=2)
    
    if cars:
        print(f"Found {len(cars)} cars")
        scraper.print_summary()
        scraper.save_to_csv("test_basic_search.csv")
    else:
        print("No cars found")

def test_transmission_filter():
    """Test transmission filter"""
    print("\n=== Testing Transmission Filter ===")
    scraper = CarScraper()
    
    # Search for automatic Ford Focus
    filters = {'transmission': 'otomatik'}
    cars = scraper.get_filtered_cars("ford", "focus", filters, max_pages=2)
    
    if cars:
        print(f"Found {len(cars)} automatic cars")
        scraper.print_summary()
        scraper.save_to_csv("test_automatic_cars.csv")
    else:
        print("No automatic cars found")

def test_damage_filter():
    """Test damage filter"""
    print("\n=== Testing Damage Filter ===")
    scraper = CarScraper()
    
    # Search for non-heavy damaged cars
    filters = {'heavy_damage': False}
    cars = scraper.get_filtered_cars("ford", "focus", filters, max_pages=2)
    
    if cars:
        print(f"Found {len(cars)} non-heavy damaged cars")
        scraper.print_summary()
        scraper.save_to_csv("test_non_damaged_cars.csv")
    else:
        print("No non-heavy damaged cars found")

def test_combined_filters():
    """Test combined filters"""
    print("\n=== Testing Combined Filters ===")
    scraper = CarScraper()
    
    # Search for automatic, non-heavy damaged cars
    filters = {
        'transmission': 'otomatik',
        'heavy_damage': False,
        'exclude_damage': True
    }
    cars = scraper.get_filtered_cars("ford", "focus", filters, max_pages=2)
    
    if cars:
        print(f"Found {len(cars)} cars matching all criteria")
        scraper.print_summary()
        scraper.save_to_csv("test_combined_filters.csv")
    else:
        print("No cars found matching all criteria")

def main():
    """Run all tests"""
    print("Starting Advanced Car Scraper Tests")
    print("=" * 50)
    
    try:
        test_basic_search()
        test_transmission_filter()
        test_damage_filter()
        test_combined_filters()
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
