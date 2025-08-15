# Sahibinden.com Car Scraper

Advanced web scraper for extracting car details from Sahibinden.com using undetected-chromedriver to bypass Cloudflare protection.

## Features

- **Cloudflare Bypass**: Uses undetected-chromedriver to bypass bot protection
- **Comprehensive Filtering**: Filter by brand, model, transmission, damage status, mileage, year, and price
- **Multiple Output Formats**: Save results as CSV and JSON
- **Robust Error Handling**: Handles stale elements, timeouts, and network issues
- **Progress Tracking**: Real-time progress indicators and debug functionality
- **Headless Mode Support**: Optional headless operation

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

### Advanced Filtering
```bash
python undetected_car_scraper.py renault clio \
    --submodel 1.3-tce \
    --transmission otomatik \
    --heavy-damage hayır \
    --max-km 150000 \
    --max-pages 3
```

### Available Filters
- `--transmission`: otomatik/manuel
- `--heavy-damage`: evet/hayır
- `--max-km`: Maximum kilometer
- `--min-km`: Minimum kilometer
- `--max-year`: Maximum year
- `--min-year`: Minimum year
- `--max-price`: Maximum price
- `--min-price`: Minimum price
- `--exclude-damage`: Exclude cars with hood replacement or paint damage
- `--max-pages`: Maximum pages to scrape (default: 3)
- `--headless`: Run in headless mode
- `--output-format`: csv/json/both (default: both)

## Output

The scraper generates two output files:
- `undetected_filtered_cars.csv`: CSV format with all car details
- `undetected_filtered_cars.json`: JSON format with structured data

## Project Structure

- `undetected_car_scraper.py`: Main scraper with advanced features
- `requirements.txt`: Python dependencies
- `SELENIUM_GUIDE.md`: Detailed setup and troubleshooting guide
- `USAGE_GUIDE.md`: Comprehensive usage examples
- `INSTALLATION_GUIDE.md`: Step-by-step installation guide

## Technical Details

- **Browser Automation**: Selenium WebDriver with undetected-chromedriver
- **HTML Parsing**: BeautifulSoup4 for data extraction
- **Error Handling**: Comprehensive exception handling for web scraping challenges
- **Rate Limiting**: Built-in delays to avoid overwhelming the server

## Important Notes

- Use responsibly and respect the website's terms of service
- The scraper includes delays to simulate human behavior
- Cloudflare protection may occasionally block requests
- Headless mode may not work due to advanced bot detection

## Troubleshooting

If you encounter issues:
1. Check the debug HTML files generated during scraping
2. Ensure Chrome browser is installed and up to date
3. Try running in visible mode instead of headless
4. Check the SELENIUM_GUIDE.md for detailed troubleshooting

## License

This project is for educational purposes. Please use responsibly and in accordance with Sahibinden.com's terms of service.