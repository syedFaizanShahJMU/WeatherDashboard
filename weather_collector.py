import requests
import pandas as pd
from datetime import datetime
import json
import os

API_KEY = os.getenv('WEATHER_API_KEY')

# German cities
cities = [
    'Würzburg,Germany',
    'Frankfurt,Germany', 
    'Munich,Germany',
    'Nuremberg,Germany',
    'Stuttgart,Germany'
]

def collect_weather_data():
    """Collect current weather data for all German cities"""
    data = []
    timestamp = datetime.now()
    
    for city in cities:
        try:
            # API call
            url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"
            response = requests.get(url)
            weather = response.json()
            
            # Extract data for Tableau
            record = {
                'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Date': timestamp.strftime('%Y-%m-%d'),
                'Time': timestamp.strftime('%H:%M:%S'),
                'Hour': timestamp.hour,
                'City': weather['location']['name'],
                'Country': weather['location']['country'],
                'Region': weather['location']['region'],
                'Latitude': weather['location']['lat'],
                'Longitude': weather['location']['lon'],
                'Temperature_C': weather['current']['temp_c'],
                'Temperature_F': weather['current']['temp_f'],
                'Feels_Like_C': weather['current']['feelslike_c'],
                'Feels_Like_F': weather['current']['feelslike_f'],
                'Humidity_%': weather['current']['humidity'],
                'Pressure_mb': weather['current']['pressure_mb'],
                'Pressure_in': weather['current']['pressure_in'],
                'Wind_Speed_kph': weather['current']['wind_kph'],
                'Wind_Speed_mph': weather['current']['wind_mph'],
                'Wind_Direction': weather['current']['wind_dir'],
                'Wind_Degree': weather['current']['wind_degree'],
                'Visibility_km': weather['current']['vis_km'],
                'Visibility_miles': weather['current']['vis_miles'],
                'UV_Index': weather['current']['uv'],
                'Cloud_Coverage_%': weather['current']['cloud'],
                'Weather_Condition': weather['current']['condition']['text'],
                'Weather_Code': weather['current']['condition']['code'],
                'Is_Day': weather['current']['is_day'],
                'Precipitation_mm': weather['current']['precip_mm'],
                'Precipitation_in': weather['current']['precip_in'],
                
                # Air Quality Data
                'AQ_CO': weather['current']['air_quality']['co'],
                'AQ_NO2': weather['current']['air_quality']['no2'],
                'AQ_O3': weather['current']['air_quality']['o3'],
                'AQ_PM2_5': weather['current']['air_quality']['pm2_5'],
                'AQ_PM10': weather['current']['air_quality']['pm10'],
                'AQ_US_EPA_Index': weather['current']['air_quality']['us-epa-index'],
                'AQ_GB_DEFRA_Index': weather['current']['air_quality']['gb-defra-index'],
                
                # Calculated Fields for BA Analysis
                'Temp_Category': categorize_temperature(weather['current']['temp_c']),
                'Humidity_Category': categorize_humidity(weather['current']['humidity']),
                'Air_Quality_Category': categorize_air_quality(weather['current']['air_quality']['us-epa-index']),
                'Weather_Severity_Score': calculate_weather_severity(weather['current']),
                'Comfort_Index': calculate_comfort_index(weather['current']['temp_c'], weather['current']['humidity']),
                
                # Business Metrics
                'Heat_Alert': 'Yes' if weather['current']['temp_c'] >= 30 else 'No',
                'Cold_Alert': 'Yes' if weather['current']['temp_c'] <= 0 else 'No',
                'High_Humidity_Alert': 'Yes' if weather['current']['humidity'] >= 90 else 'No',
                'High_Wind_Alert': 'Yes' if weather['current']['wind_kph'] >= 30 else 'No',
                'Poor_Air_Quality_Alert': 'Yes' if weather['current']['air_quality']['us-epa-index'] >= 3 else 'No'
            }
            
            data.append(record)
            print(f"✓ Collected data for {weather['location']['name']}")
            
        except Exception as e:
            print(f"✗ Error collecting data for {city}: {e}")
    
    return data

def categorize_temperature(temp):
    """Categorize temperature for business analysis"""
    if temp >= 30: return 'Very Hot'
    elif temp >= 25: return 'Hot'
    elif temp >= 20: return 'Warm'
    elif temp >= 15: return 'Mild'
    elif temp >= 10: return 'Cool'
    elif temp >= 0: return 'Cold'
    else: return 'Very Cold'

def categorize_humidity(humidity):
    """Categorize humidity levels"""
    if humidity >= 90: return 'Very High'
    elif humidity >= 70: return 'High'
    elif humidity >= 50: return 'Moderate'
    elif humidity >= 30: return 'Low'
    else: return 'Very Low'

def categorize_air_quality(epa_index):
    """Categorize air quality"""
    categories = {
        1: 'Good',
        2: 'Moderate', 
        3: 'Unhealthy for Sensitive',
        4: 'Unhealthy',
        5: 'Very Unhealthy',
        6: 'Hazardous'
    }
    return categories.get(epa_index, 'Unknown')

def calculate_weather_severity(current_weather):
    """Calculate overall weather severity score (1-10)"""
    score = 0
    
    # Temperature extremes
    temp = current_weather['temp_c']
    if temp >= 35 or temp <= -5: score += 3
    elif temp >= 30 or temp <= 0: score += 2
    elif temp >= 28 or temp <= 2: score += 1
    
    # Wind
    wind = current_weather['wind_kph']
    if wind >= 50: score += 3
    elif wind >= 30: score += 2
    elif wind >= 20: score += 1
    
    # Precipitation
    if current_weather['precip_mm'] > 10: score += 2
    elif current_weather['precip_mm'] > 5: score += 1
    
    # Air quality
    aqi = current_weather['air_quality']['us-epa-index']
    if aqi >= 4: score += 2
    elif aqi >= 3: score += 1
    
    return min(score, 10)  # Cap at 10

def calculate_comfort_index(temp, humidity):
    """Calculate comfort index (1-100, higher is more comfortable)"""
    # Ideal: 20-25°C, 40-60% humidity
    temp_score = 100 - abs(22.5 - temp) * 4  # Penalty for deviation from 22.5°C
    humidity_score = 100 - abs(50 - humidity) * 2  # Penalty for deviation from 50%
    
    comfort = (temp_score + humidity_score) / 2
    return max(0, min(100, comfort))  # Keep between 0-100

def save_to_csv(data, filename='german_weather_data.csv'):
    """Save data to CSV for Tableau"""
    df = pd.DataFrame(data)
    
    # Try to append to existing file
    try:
        existing_df = pd.read_csv(filename)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_csv(filename, index=False)
        print(f"✓ Data appended to {filename}")
        print(f"✓ Total records: {len(combined_df)}")
    except FileNotFoundError:
        df.to_csv(filename, index=False)
        print(f"✓ New file created: {filename}")
        print(f"✓ Records: {len(df)}")
    
    return df

def collect_historical_data(hours=24):
    """Collect data every hour for the past X hours (simulated)"""
    all_data = []
    
    for i in range(hours):
        print(f"\n📊 Collecting data point {i+1}/{hours}")
        data = collect_weather_data()
        all_data.extend(data)
        
        # Modify timestamp to simulate historical data
        for record in data:
            original_time = datetime.strptime(record['Timestamp'], '%Y-%m-%d %H:%M:%S')
            new_time = original_time - pd.Timedelta(hours=i)
            record['Timestamp'] = new_time.strftime('%Y-%m-%d %H:%M:%S')
            record['Date'] = new_time.strftime('%Y-%m-%d')
            record['Time'] = new_time.strftime('%H:%M:%S')
            record['Hour'] = new_time.hour
        
        if i < hours - 1:  # Don't wait after the last collection
            print("⏰ Waiting 2 seconds before next collection...")
            import time
            time.sleep(2)
    
    return all_data

if __name__ == "__main__":
    print("🇩🇪 German Cities Weather Data Collector for Tableau")
    print("=" * 55)
    
    choice = input("""
Choose collection mode:
1. Single snapshot (right now)
2. Collect 24 hours of data (simulated historical)
3. Collect 7 days of data (simulated historical)

Enter choice (1, 2, or 3): """)
    
    if choice == "1":
        data = collect_weather_data()
        df = save_to_csv(data)
        
    elif choice == "2":
        data = collect_historical_data(24)
        df = save_to_csv(data)
        
    elif choice == "3":
        data = collect_historical_data(24 * 7)  # 7 days worth
        df = save_to_csv(data)
        
    else:
        print("Invalid choice. Collecting single snapshot...")
        data = collect_weather_data()
        df = save_to_csv(data)
    
    print(f"\n✅ Data collection complete!")
    print(f"✅ CSV file ready for Tableau import")
    print(f"✅ File contains {len(df) if 'df' in locals() else len(data)} records")
    print(f"\n📋 Next steps:")
    print(f"1. Open Tableau Public")
    print(f"2. Connect to Text File")
    print(f"3. Select 'german_weather_data.csv'")
    print(f"4. Start building your visualizations!")
