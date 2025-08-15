# Advanced Car Scraper - Usage Guide

This guide explains how to use the updated car scraper based on the actual sahibinden.com URL structure.

## URL Structure Analysis

Example URL: `https://www.sahibinden.com/renault-clio-1.3-tce/otomatik?a116445=1263354&a4_max=150000`

**URL Components:**
- **Brand**: renault
- **Model**: clio
- **Submodel**: 1.3-tce
- **Transmission**: otomatik (in URL path)
- **Kilometer**: Maximum 150,000 (a4_max=150000)
- **Heavy Damage**: No (a116445=1263354)

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

### 8. All Filters Combined (Matching Example URL)
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır
```

## All Filter Options

### Basic Parameters
- `brand`: Car brand (required)
- `model`: Car model (required)
- `--submodel`: Submodel (optional)

### Filters
- `--transmission`: Transmission type (`otomatik` or `manuel`)
- `--heavy-damage`: Heavy damage status (`evet` or `hayır`)
- `--exclude-damage`: Exclude cars with hood replacement and paint damage
- `--max-km`: Maximum kilometer
- `--min-km`: Minimum kilometer
- `--max-year`: Maximum model year
- `--min-year`: Minimum model year
- `--max-price`: Maximum price (TL)
- `--min-price`: Minimum price (TL)

### Other Options
- `--max-pages`: Maximum number of pages (default: 3)
- `--output-format`: Output format (`csv`, `json`, `both`)
- `--headless`: Run in headless mode

## URL Structure

The scraper uses this URL structure:
```
https://www.sahibinden.com/{brand}-{model}-{submodel}/{transmission}?{parameters}
```

### Example URLs:
```
# Basic search
https://www.sahibinden.com/renault-clio

# With submodel
https://www.sahibinden.com/renault-clio-1.3-tce

# With transmission
https://www.sahibinden.com/renault-clio-1.3-tce/otomatik

# With filters
https://www.sahibinden.com/renault-clio-1.3-tce/otomatik?a4_max=150000&a116445=1263354
```

## Output Formats

### CSV File (`undetected_filtered_cars.csv`)
- Price, model year, brand, model
- Transmission type, fuel, kilometer
- Damage status, location information
- Sahibinden.com link

### JSON File (`undetected_filtered_cars.json`)
- All details in JSON format
- Ideal for programmatic use

## Test Examples

### Test 1: Renault Clio 1.3 TCe Automatic
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --max-km 150000 --heavy-damage hayır --max-pages 2
```

### Test 2: Ford Focus Manual
```bash
python undetected_car_scraper.py ford focus --transmission manuel --min-year 2018 --max-pages 2
```

### Test 3: Volkswagen Golf
```bash
python undetected_car_scraper.py volkswagen golf --max-price 300000 --min-year 2020 --max-pages 2
```

### Test 4: Advanced Search with All Filters
```bash
python undetected_car_scraper.py renault clio --submodel 1.3-tce --transmission otomatik --heavy-damage hayır --max-km 150000 --max-price 500000 --min-year 2018 --exclude-damage --max-pages 5
```

## Important Notes

1. **Responsible Usage**: Rate limiting is implemented (1-3 second delays)
2. **URL Structure**: Matches actual sahibinden.com URL structure
3. **Filter Parameters**: Uses real site parameters
4. **Error Handling**: Multiple HTML selector support
5. **Session Management**: Efficient connection management
6. **Browser Automation**: Uses undetected-chromedriver for bypassing protection

## Troubleshooting

### "No cars found" Error
- Check brand/model name
- Ensure submodel name is correct
- Filters might be too restrictive

### URL Error
- Write brand and model names in lowercase
- Use hyphens (-) in submodel names
- Avoid special characters

### Connection Error
- Check your internet connection
- Verify sahibinden.com is accessible
- Check proxy settings if using one

### Browser Automation Issues
- Ensure Chrome browser is installed and updated
- Try running in visible mode instead of headless
- Check Chrome version compatibility

## Performance Tips

1. **Limit Page Count**: Test with `--max-pages 3`
2. **Add Filters Gradually**: Start with basic search, then add filters
3. **Choose Output Format**: Use `--output-format csv` for CSV only
4. **Error Recovery**: Wait a few minutes and try again
5. **Use Visible Mode**: Better reliability than headless mode

## Advanced Usage Scenarios

### Scenario 1: Budget Car Search
```bash
# Find affordable automatic cars under 300k TL
python undetected_car_scraper.py ford focus --transmission otomatik --max-price 300000 --min-year 2015 --max-km 100000
```

### Scenario 2: Premium Car Search
```bash
# Find premium cars with specific criteria
python undetected_car_scraper.py bmw 3 --submodel 320i --transmission otomatik --min-year 2020 --max-price 800000 --exclude-damage
```

### Scenario 3: Family Car Search
```bash
# Find family-friendly cars
python undetected_car_scraper.py volkswagen passat --transmission otomatik --min-year 2018 --max-km 80000 --heavy-damage hayır
```

## Output File Structure

### CSV Columns:
- `price`: Price in TL
- `year`: Model year
- `brand`: Car brand
- `model`: Car model
- `fuel`: Fuel type
- `transmission`: Transmission type
- `km`: Kilometer
- `type`: Car type
- `hp`: Horsepower
- `cc`: Engine displacement
- `color`: Color
- `damage`: Damage information
- `heavy_damage`: Heavy damage status
- `city`: City
- `county`: County
- `neighborhood`: Neighborhood
- `url`: Sahibinden.com link
