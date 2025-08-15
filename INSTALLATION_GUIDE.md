# Installation Guide - Advanced Car Scraper

This guide contains the necessary steps to run the advanced car scraper.

## 1. Python Installation

### For Windows:
1. **Download Python**: https://www.python.org/downloads/
2. **During Installation**: Check "Add Python to PATH" option
3. **Complete Installation**: Accept all default settings

### Verify Installation:
```bash
python --version
# or
py --version
```

## 2. Install Required Libraries

Navigate to the project folder and run:
```bash
pip install -r requirements.txt
```

### Manual Installation:
```bash
pip install requests beautifulsoup4 selenium undetected-chromedriver
```

## 3. Test Installation

### Simple Test:
```bash
python simple_test.py
```

### Advanced Test:
```bash
python test_scraper.py
```

## 4. Using the Scraper

### Basic Usage:
```bash
python undetected_car_scraper.py ford focus
```

### With Filters:
```bash
# Automatic transmission only
python undetected_car_scraper.py ford focus --transmission otomatik

# No heavy damage
python undetected_car_scraper.py ford focus --heavy-damage hayır

# Exclude hood replacement and painted cars
python undetected_car_scraper.py ford focus --exclude-damage

# All filters combined
python undetected_car_scraper.py ford focus --transmission otomatik --heavy-damage hayır --exclude-damage

# With price and year limits
python undetected_car_scraper.py ford focus --max-price 500000 --min-year 2018 --max-km 100000
```

## 5. Troubleshooting

### Python Not Found Error:
- Ensure Python is added to PATH
- Restart command prompt
- Try using `py` command: `py --version`

### Library Installation Error:
```bash
# Update pip
python -m pip install --upgrade pip

# Install libraries individually
pip install requests
pip install beautifulsoup4
pip install selenium
pip install undetected-chromedriver
```

### Internet Connection Error:
- Check your internet connection
- Verify sahibinden.com is accessible
- Check proxy settings if using one

### Site Structure Changes:
- Code updates may be required
- Use the latest version of `undetected_car_scraper.py`

### Chrome/ChromeDriver Issues:
- Ensure Chrome browser is installed and up to date
- Try running in visible mode instead of headless
- Check Chrome version compatibility

## 6. Output Files

After running the scraper, these files will be created:
- `undetected_filtered_cars.csv`: Car list in CSV format
- `undetected_filtered_cars.json`: Car list in JSON format

## 7. Important Notes

**Responsible Usage:**
- Do not send requests too quickly
- Implement rate limiting
- Follow sahibinden.com's terms of service

**Data Currency:**
- Results reflect data at the time of execution
- Data is continuously updated

**Browser Automation:**
- The scraper uses undetected-chromedriver to bypass protection
- Headless mode may not work due to advanced bot detection
- Visible mode is recommended for better reliability

## 8. Support

If you encounter issues:
1. Run `simple_test.py` script
2. Check error messages
3. Verify Python and library versions
4. Test your internet connection
5. Check Chrome browser installation

## 9. Advanced Features

### Available Filters:
- `--transmission`: otomatik/manuel
- `--heavy-damage`: evet/hayır
- `--exclude-damage`: Exclude hood replacement and painted cars
- `--max-km` / `--min-km`: Kilometer range
- `--max-year` / `--min-year`: Year range
- `--max-price` / `--min-price`: Price range
- `--max-pages`: Maximum pages to scrape (default: 3)
- `--headless`: Run in headless mode
- `--output-format`: csv/json/both (default: both)

### Example Advanced Usage:
```bash
# Find automatic Renault Clio 1.3 TCE, no heavy damage, max 150k km, max 500k TL
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --heavy-damage hayır --max-km 150000 --max-price 500000 --max-pages 5
```
