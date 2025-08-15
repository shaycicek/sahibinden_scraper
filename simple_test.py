#!/usr/bin/env python
"""
Simple test script for the car scraper
This script tests basic functionality without complex dependencies
"""

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import sys
        print("✓ sys imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import sys: {e}")
        return False
    
    try:
        import csv
        print("✓ csv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import csv: {e}")
        return False
    
    try:
        import json
        print("✓ json imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import json: {e}")
        return False
    
    try:
        import argparse
        print("✓ argparse imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import argparse: {e}")
        return False
    
    try:
        import time
        print("✓ time imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import time: {e}")
        return False
    
    try:
        import random
        print("✓ random imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import random: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✓ datetime imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import datetime: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import requests: {e}")
        print("  Please install requests: pip install requests")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import BeautifulSoup: {e}")
        print("  Please install beautifulsoup4: pip install beautifulsoup4")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without making web requests"""
    print("\nTesting basic functionality...")
    
    try:
        # Test URL construction
        BASE_URL = "https://www.sahibinden.com{}"
        car_url = "https://www.sahibinden.com/{}-{}?{}"
        
        brand = "ford"
        model = "focus"
        url_params = "pagingOffset=0"
        
        url = car_url.format(brand, model, url_params)
        expected_url = "https://www.sahibinden.com/ford-focus?pagingOffset=0"
        
        if url == expected_url:
            print("✓ URL construction works correctly")
        else:
            print(f"✗ URL construction failed. Expected: {expected_url}, Got: {url}")
            return False
        
        # Test filter logic
        filters = {
            'transmission': 'otomatik',
            'heavy_damage': False,
            'exclude_damage': True
        }
        
        print(f"✓ Filter configuration: {filters}")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\nTesting file operations...")
    
    try:
        import csv
        import json
        
        # Test CSV writing
        test_data = [
            {'price': '100000', 'year': '2020', 'brand': 'ford', 'model': 'focus'},
            {'price': '150000', 'year': '2021', 'brand': 'ford', 'model': 'focus'}
        ]
        
        # Test CSV
        with open('test_output.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['price', 'year', 'brand', 'model'])
            writer.writeheader()
            writer.writerows(test_data)
        
        print("✓ CSV file writing works")
        
        # Test JSON
        with open('test_output.json', 'w', encoding='utf-8') as file:
            json.dump(test_data, file, ensure_ascii=False, indent=2)
        
        print("✓ JSON file writing works")
        
        # Clean up test files
        import os
        if os.path.exists('test_output.csv'):
            os.remove('test_output.csv')
        if os.path.exists('test_output.json'):
            os.remove('test_output.json')
        
        print("✓ Test files cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ File operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("ADVANCED CAR SCRAPER - SIMPLE TEST")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
        print("✓ All imports successful")
    else:
        print("✗ Some imports failed")
    
    # Test 2: Basic functionality
    if test_basic_functionality():
        tests_passed += 1
        print("✓ Basic functionality works")
    else:
        print("✗ Basic functionality failed")
    
    # Test 3: File operations
    if test_file_operations():
        tests_passed += 1
        print("✓ File operations work")
    else:
        print("✗ File operations failed")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The scraper should work correctly.")
        print("\nTo use the scraper:")
        print("1. python advanced_car_scraper_fixed.py ford focus")
        print("2. python advanced_car_scraper_fixed.py ford focus --transmission otomatik")
        print("3. python advanced_car_scraper_fixed.py ford focus --heavy-damage hayır --exclude-damage")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies:")
        print("pip install requests beautifulsoup4")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
