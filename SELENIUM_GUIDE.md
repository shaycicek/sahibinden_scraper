# Selenium-Based Car Scraper - Usage Guide

This guide explains how to set up and use the advanced car scraper that uses Selenium WebDriver to bypass bot protection.

## Why Selenium?

### Problems with Requests Library
- 403 Forbidden errors
- Blocked by bot protection
- IP-based restrictions

### Selenium Advantages
- Real browser simulation
- JavaScript support
- Bypass bot protection
- Human behavior simulation

## Requirements

### 1. Python Libraries
```bash
pip install selenium==4.15.2
pip install beautifulsoup4
pip install requests
pip install undetected-chromedriver
```

### 2. Chrome WebDriver
Chrome browser must be installed. WebDriver will be downloaded automatically.

## Installation

### 1. Install Libraries
```bash
pip install -r requirements.txt
```

### 2. Chrome Browser
- Ensure Google Chrome is installed
- WebDriver will be managed automatically

## Usage Examples

### 1. Basic Usage
```bash
python undetected_car_scraper.py renault clio
```

### 2. With Submodel
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce
```

### 3. Transmission Filter
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik
```

### 4. Kilometer Filter
```bash
python undetected_car_scraper.py renault clio --max-km 150000
```

### 5. Heavy Damage Filter
```bash
python undetected_car_scraper.py renault clio --heavy-damage hayır
```

### 6. Year Range
```bash
python undetected_car_scraper.py renault clio --min-year 2020 --max-year 2023
```

### 7. Price Range
```bash
python undetected_car_scraper.py renault clio --min-price 200000 --max-price 500000
```

### 8. All Filters Combined
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 2
```

### 9. Headless Mode
```bash
python undetected_car_scraper.py renault clio --headless
```

## All Parameters

### Required Parameters
- `brand`: Car brand (e.g., renault, ford, volkswagen)
- `model`: Car model (e.g., clio, focus, golf)

### Optional Parameters
- `--submodel`: Submodel (e.g., 1.3-tce, 1.6-tdi)
- `--transmission`: Transmission type (`otomatik` or `manuel`)
- `--heavy-damage`: Heavy damage status (`evet` or `hayır`)
- `--exclude-damage`: Exclude cars with hood replacement and paint damage
- `--max-km`: Maximum kilometer
- `--min-km`: Minimum kilometer
- `--max-year`: Maximum model year
- `--min-year`: Minimum model year
- `--max-price`: Maximum price (TL)
- `--min-price`: Minimum price (TL)
- `--max-pages`: Maximum number of pages (default: 3)
- `--output-format`: Output format (`csv`, `json`, `both`)
- `--headless`: Run browser in headless mode

## Features

### 1. Human Behavior Simulation
- Random delays (1-3 seconds)
- Page loading waits
- Realistic browser settings

### 2. Bot Protection Bypass
- Hide WebDriver property
- Realistic User-Agent
- Remove automation indicators

### 3. Error Handling
- Page loading timeouts
- Element not found situations
- Connection errors

### 4. Multiple Selector Support
- Alternative selectors for different HTML structures
- Dynamic content support
- Resilience to site changes

## Output Files

### CSV File (`undetected_filtered_cars.csv`)
```
price,year,brand,model,fuel,transmission,km,type,hp,cc,color,damage,heavy_damage,city,county,neighborhood,url
450000,2020,renault,clio,benzin,otomatik,75000,hatchback,130,1333,beyaz,hasarsız,hayır,istanbul,kadıköy,moda,https://...
```

### JSON File (`undetected_filtered_cars.json`)
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

## Test Scenarios

### Test 1: Basic Search
```bash
python undetected_car_scraper.py renault clio --max-pages 1
```

### Test 2: Filtered Search
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 1
```

### Test 3: Headless Mode
```bash
python undetected_car_scraper.py ford focus --headless --max-pages 1
```

## Important Notes

### 1. Performance
- Selenium is slower than requests
- 1-3 second delay per page
- Real browser opens

### 2. System Requirements
- Chrome browser required
- Sufficient RAM (at least 2GB)
- Internet connection

### 3. Responsible Usage
- Rate limiting is implemented
- Be respectful to the server
- Don't send too many requests

## Troubleshooting

### Chrome WebDriver Error
```
✗ WebDriver could not be started: Message: unknown error: cannot find Chrome binary
```
**Solution**: Install Chrome browser

### Page Loading Error
```
❌ Page could not be loaded, stopping...
```
**Solution**: Check your internet connection

### Element Not Found
```
❌ Error processing car: NoSuchElementException
```
**Solution**: Site structure may have changed, update selectors

### Memory Error
```
❌ Unexpected error: OutOfMemoryError
```
**Solution**: Reduce page count (`--max-pages 1`)

### Undetected ChromeDriver Issues
```
✗ Undetected ChromeDriver could not be started
```
**Solution**: 
- Update Chrome browser
- Try running in visible mode
- Check Chrome version compatibility

## Performance Tips

### 1. Limit Page Count
```bash
--max-pages 2  # Only scan 2 pages
```

### 2. Use Headless Mode
```bash
--headless  # Browser window won't open
```

### 3. Choose Output Format
```bash
--output-format csv  # CSV output only
```

### 4. Use Filters
```bash
--max-km 100000  # Fewer results, faster processing
```

### 5. Use Visible Mode for Reliability
```bash
# Don't use --headless for better reliability
python undetected_car_scraper.py renault clio
```

## Example Usage Scenarios

### Scenario 1: Renault Clio 1.3 TCe Automatic
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 2
```

### Scenario 2: Ford Focus Manual 2018+
```bash
python undetected_car_scraper.py ford focus --transmission manuel --min-year 2018 --max-pages 2
```

### Scenario 3: Volkswagen Golf Under 300K TL
```bash
python undetected_car_scraper.py volkswagen golf --max-price 300000 --min-year 2020 --max-pages 2
```

### Scenario 4: Advanced Search with All Filters
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --heavy-damage hayır --max-km 150000 --max-price 500000 --min-year 2018 --exclude-damage --max-pages 3
```

## Security and Legal Warnings

1. **Responsible Usage**: Follow site rules
2. **Rate Limiting**: Don't send requests too quickly
3. **Legal Responsibility**: User is responsible
4. **Data Usage**: Designed for personal use

## Support

If you encounter issues:
1. Ensure Chrome browser is installed
2. Check your internet connection
3. Reduce page count
4. Simplify filters
5. Try running in visible mode instead of headless

## Technical Details

### Undetected ChromeDriver
- Automatically bypasses Cloudflare protection
- Hides automation indicators
- Simulates real browser behavior

### Browser Options
- Disabled automation flags
- Realistic user agent
- Stealth mode settings
- Window size configuration

### Error Recovery
- Automatic retry mechanism
- Graceful error handling
- Detailed error logging

---

**Note**: This scraper is for educational purposes and requires responsible usage.
