# German Cities Weather Dashboard

A real-time weather monitoring system for major German cities, featuring both a live web dashboard and a data collection script for analytics.

## Features

### Live Web Dashboard (`weather-dashboard.html`)
- Real-time weather data for 5 major German cities (Würzburg, Frankfurt, Munich, Nuremberg, Stuttgart)
- Beautiful, responsive UI with color-coded temperature indicators
- Air quality monitoring with EPA index
- Automatic refresh every 15 minutes
- City comparison metrics
- Weather alerts for extreme conditions
- Mobile-friendly design

### Data Collection Script (`weather_collector.py`)
- Automated weather data collection
- CSV export for analysis tools (Tableau, Excel, etc.)
- Historical data simulation
- Comprehensive metrics including:
  - Temperature, humidity, pressure
  - Wind speed and direction
  - Air quality indicators (PM2.5, PM10, CO, NO2, O3)
  - Custom business analytics fields
  - Weather severity scoring
  - Comfort index calculations

## Prerequisites

### For Web Dashboard
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- WeatherAPI.com API key (free tier available)

### For Data Collection Script
- Python 3.7+
- pip (Python package manager)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/syedFaizanShahJMU/WeatherDashboard.git
cd WeatherDashboard
```

### 2. Get Your API Key
1. Visit [WeatherAPI.com](https://www.weatherapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 3. Setup for Web Dashboard
1. Open `weather-dashboard.html` in a text editor
2. Replace the API key on line 241:
```javascript
const API_KEY = 'YOUR_API_KEY_HERE';
```
3. Open the file in your web browser

### 4. Setup for Data Collection Script
1. Install required Python packages:
```bash
pip install -r requirements.txt
```

2. Set your API key as an environment variable:

**On macOS/Linux:**
```bash
export WEATHER_API_KEY='your_api_key_here'
```

**On Windows:**
```bash
set WEATHER_API_KEY=your_api_key_here
```

Or create a `.env` file in the project directory:
```
WEATHER_API_KEY=your_api_key_here
```

## Usage

### Web Dashboard
Simply open `weather-dashboard.html` in your browser. The dashboard will automatically:
- Load current weather for all cities
- Refresh data every 15 minutes
- Display weather alerts when conditions are extreme

### Data Collection Script
Run the script with:
```bash
python weather_collector.py
```

Choose from three collection modes:
1. **Single snapshot** - Current weather data
2. **24 hours** - Simulated hourly data for 1 day
3. **7 days** - Simulated hourly data for 1 week

Data is saved to `german_weather_data.csv` and can be imported into:
- Tableau Public
- Microsoft Excel
- Google Sheets
- Any data analysis tool

## Data Fields

The collector captures 50+ data points per city including:

**Basic Weather**
- Temperature (°C and °F)
- Feels like temperature
- Humidity, pressure, visibility
- Wind speed, direction, degree
- Cloud coverage
- UV index
- Precipitation

**Air Quality**
- CO, NO2, O3 levels
- PM2.5 and PM10
- US EPA Index
- GB DEFRA Index

**Calculated Metrics**
- Temperature category
- Humidity category
- Air quality category
- Weather severity score (1-10)
- Comfort index (0-100)
- Various alert flags

## Project Structure

```
WeatherDashboard/
│
├── weather-dashboard.html    # Live web dashboard
├── weather_collector.py      # Data collection script
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── german_weather_data.csv # Generated data (excluded from git)
```

## API Rate Limits

WeatherAPI.com free tier allows:
- 1,000,000 calls per month
- Up to 3 calls per second

This project stays well within limits:
- Web dashboard: ~288 calls/day (auto-refresh every 15 min)
- Data collector: 5 calls per run

## Weather Alerts

The dashboard shows alerts for:
- Temperature ≥ 30°C (Very Hot)
- Temperature ≤ 0°C (Freezing)
- Wind speed ≥ 30 km/h (Strong Winds)
- Humidity ≥ 90% (Very High)
- UV Index ≥ 8 (High UV)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Weather data provided by [WeatherAPI.com](https://www.weatherapi.com/)
- Built for real-time monitoring and business analytics

## Support

For issues or questions:
1. Check the [Issues](https://github.com/syedFaizanShahJMU/WeatherDashboard/issues) page
2. Create a new issue if your problem isn't already listed

## Future Enhancements

- [ ] Historical data visualization
- [ ] Weather forecasting
- [ ] Email alerts for severe weather
- [ ] Mobile app version
- [ ] More German cities
- [ ] Multi-language support

---

**Note:** Remember to never commit your API key to version control. Use environment variables or a `.env` file (which is gitignored).
