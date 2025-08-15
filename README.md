# Sahibinden.com Car Scraper

Advanced web scraper for extracting car details from Sahibinden.com using undetected-chromedriver to bypass Cloudflare protection.

## Features

- **Cloudflare Bypass**: Uses undetected-chromedriver to bypass bot protection
- **Advanced Filtering**: Filter by brand, model, submodel, transmission, damage status, mileage, year, and price
- **Hood Status Detection**: Automatically detect and filter cars based on hood (kaput) condition
- **Parallel Processing**: Fast mode with concurrent processing for improved speed
- **Multiple Output Formats**: Save results as CSV and JSON
- **Robust Error Handling**: Handles stale elements, timeouts, and network issues
- **Progress Tracking**: Real-time progress indicators and debug functionality
- **Headless Mode Support**: Optional headless operation with enhanced stealth
- **Enhanced Stealth**: Advanced bot detection avoidance techniques

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Chrome browser (required for undetected-chromedriver)

## Usage

### Basic Usage
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik
```

### Advanced Filtering with Hood Status
```bash
python undetected_car_scraper.py renault clio \
    --submodel 1.3-tce \
    --transmission otomatik \
    --heavy-damage hayır \
    --min-year 2015 \
    --max-km 150000 \
    --original-hood-only \
    --max-pages 3
```

### Fast Mode (Parallel Processing)
```bash
python undetected_car_scraper.py renault clio \
    --fast \
    --workers 5 \
    --max-pages 2
```

### Available Filters
- `--submodel`: Alt model (örn: 1.3-tce)
- `--transmission`: otomatik/manuel
- `--heavy-damage`: evet/hayır
- `--original-hood-only`: Sadece kaputu orjinal olan araçlar
- `--exclude-damage`: Kaput değişen ve boyalı araçları hariç tut
- `--max-km`: Maximum kilometer
- `--min-km`: Minimum kilometer
- `--max-year`: Maximum year
- `--min-year`: Minimum year
- `--max-price`: Maximum price (TL)
- `--min-price`: Minimum price (TL)
- `--max-pages`: Maximum pages to scrape (default: 3)
- `--headless`: Run in headless mode
- `--fast`: Enable fast mode with parallel processing
- `--workers`: Number of parallel workers (default: 3)
- `--output-format`: csv/json/both (default: both)

## Output

The scraper generates two output files with enhanced data:
- `undetected_filtered_cars.csv`: CSV format with all car details including hood status
- `undetected_filtered_cars.json`: JSON format with structured data

### New Output Fields
- `hood_status`: Kaput durumu (Orjinal/Boyalı/Değişen/Bilinmiyor)
- `damage_details`: Detaylı hasar bilgileri
- `heavy_damage`: Ağır hasar durumu
- Enhanced location and specification data

## Performance Modes

### Normal Mode
- Sequential processing
- More detailed error handling
- Better for debugging

### Fast Mode (--fast)
- Parallel processing with ThreadPoolExecutor
- 3-stage optimization:
  1. Basic info extraction from listing pages
  2. Quick pre-filtering
  3. Parallel detailed extraction
- 3-5x faster than normal mode
- Adjustable worker count (--workers)

## Anti-Detection Features

- **Enhanced Stealth**: Advanced browser fingerprinting evasion
- **Human-like Delays**: Random delays between requests
- **Realistic User Agent**: Updated Chrome user agent
- **Plugin Simulation**: Fake plugin data to appear more human
- **Language Detection**: Turkish language preference simulation

## Project Structure

- `undetected_car_scraper.py`: Main scraper with advanced features
- `requirements.txt`: Python dependencies
- `SELENIUM_GUIDE.md`: Detailed setup and troubleshooting guide
- `USAGE_GUIDE.md`: Comprehensive usage examples
- `INSTALLATION_GUIDE.md`: Step-by-step installation guide

## Technical Details

- **Browser Automation**: Selenium WebDriver with undetected-chromedriver
- **HTML Parsing**: BeautifulSoup4 for data extraction
- **Parallel Processing**: ThreadPoolExecutor for concurrent operations
- **Error Handling**: Comprehensive exception handling for web scraping challenges
- **Rate Limiting**: Built-in delays to avoid overwhelming the server
- **Stealth Technology**: Advanced bot detection avoidance

## Important Notes

- Use responsibly and respect the website's terms of service
- The scraper includes delays to simulate human behavior
- Cloudflare protection may occasionally block requests
- Headless mode may not work due to advanced bot detection
- Fast mode may trigger rate limiting - use with caution
- Wait 15-30 minutes between large scraping sessions

## Troubleshooting

### Bot Detection Issues
If you see "Olağan dışı erişim tespit ettik" error:
1. Wait 15-30 minutes before retrying
2. Try running in visible mode instead of headless
3. Reduce the number of workers in fast mode
4. Increase delays between requests

### General Issues
1. Check the debug HTML files generated during scraping
2. Ensure Chrome browser is installed and up to date
3. Try running in visible mode instead of headless
4. Check the SELENIUM_GUIDE.md for detailed troubleshooting

## Performance Tips

- Use `--fast` mode for large searches (5-10x faster)
- Limit `--max-pages` to avoid overwhelming the server
- Use `--workers 3-5` for optimal performance
- Run during off-peak hours for better success rates
- Consider using VPN if you get blocked frequently

## License

This project is for educational purposes. Please use responsibly and in accordance with Sahibinden.com's terms of service.
