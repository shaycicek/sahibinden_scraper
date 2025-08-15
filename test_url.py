#!/usr/bin/env python
"""
Simple URL test script to check sahibinden.com access
"""

import requests
import time
import random

def test_basic_access():
    """Test basic access to sahibinden.com"""
    print("Testing basic access to sahibinden.com...")
    
    # Test 1: Basic request
    try:
        response = requests.get("https://www.sahibinden.com", timeout=10)
        print(f"Basic request: Status {response.status_code}")
        if response.status_code == 200:
            print("✓ Basic access successful")
            return True
        else:
            print(f"✗ Basic access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Basic access error: {e}")
        return False

def test_with_headers():
    """Test with realistic headers"""
    print("\nTesting with realistic headers...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        response = requests.get("https://www.sahibinden.com", headers=headers, timeout=10)
        print(f"Headers request: Status {response.status_code}")
        if response.status_code == 200:
            print("✓ Headers access successful")
            return True
        else:
            print(f"✗ Headers access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Headers access error: {e}")
        return False

def test_with_session():
    """Test with session management"""
    print("\nTesting with session management...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        # First request to get cookies
        response1 = session.get("https://www.sahibinden.com", timeout=10)
        print(f"Session request 1: Status {response1.status_code}")
        
        if response1.status_code == 200:
            print("✓ Session access successful")
            
            # Wait a bit
            time.sleep(random.uniform(2, 4))
            
            # Second request to test persistence
            response2 = session.get("https://www.sahibinden.com/renault-clio", timeout=10)
            print(f"Session request 2: Status {response2.status_code}")
            
            if response2.status_code == 200:
                print("✓ Session persistence successful")
                return True
            else:
                print(f"✗ Session persistence failed: {response2.status_code}")
                return False
        else:
            print(f"✗ Session access failed: {response1.status_code}")
            return False
    except Exception as e:
        print(f"✗ Session access error: {e}")
        return False

def test_search_url():
    """Test the specific search URL structure"""
    print("\nTesting search URL structure...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    # Test the URL from your example
    test_url = "https://www.sahibinden.com/renault-clio-1.3-tce/otomatik?a116445=1263354&a4_max=150000"
    
    try:
        response = session.get(test_url, timeout=10)
        print(f"Search URL test: Status {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Search URL access successful")
            print(f"Content length: {len(response.content)} bytes")
            return True
        else:
            print(f"✗ Search URL access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Search URL access error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SAHIBINDEN.COM ACCESS TEST")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Basic access
    if test_basic_access():
        tests_passed += 1
    
    # Test 2: With headers
    if test_with_headers():
        tests_passed += 1
    
    # Test 3: With session
    if test_with_session():
        tests_passed += 1
    
    # Test 4: Search URL
    if test_search_url():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The scraper should work.")
    elif tests_passed > 0:
        print("⚠️  Some tests passed. The scraper might work with modifications.")
    else:
        print("❌ All tests failed. The site might be blocking all automated access.")
        print("\nPossible solutions:")
        print("1. Use a VPN or proxy")
        print("2. Increase delay between requests")
        print("3. Use different User-Agent strings")
        print("4. Implement CAPTCHA solving")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
