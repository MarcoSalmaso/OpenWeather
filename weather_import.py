import requests
import psycopg2
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
import functions_framework


API_KEY = os.getenv('api')
CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

VENETO_CITIES = {
    'Venezia': {'lat': 45.4408, 'lon': 12.3155},
    'Verona': {'lat': 45.4384, 'lon': 10.9916},
    'Padova': {'lat': 45.4064, 'lon': 11.8768},
    'Vicenza': {'lat': 45.5477, 'lon': 11.5448},
    'Treviso': {'lat': 45.6669, 'lon': 12.2433},
    'Rovigo': {'lat': 45.0712, 'lon': 11.7904},
    'Belluno': {'lat': 46.1432, 'lon': 12.2136}
}

class WeatherDatabase:
    def __init__(self, connection_params: Dict[str, str]):
        self.connection_params = connection_params
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            print("Connesso al database PostgreSQL")
        except Exception as e:
            print(f"Errore connessione database: {e}")
            raise

    def create_tables(self):
        create_current_weather_table = """
        CREATE TABLE IF NOT EXISTS analytics.locazioni_meteo (
            id SERIAL PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL,
            latitude DECIMAL(8,6) NOT NULL,
            longitude DECIMAL(9,6) NOT NULL,
            temperature DECIMAL(5,2),
            feels_like DECIMAL(5,2),
            humidity INTEGER,
            pressure INTEGER,
            wind_speed DECIMAL(5,2),
            weather_main VARCHAR(50),
            weather_description VARCHAR(200),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            api_timestamp TIMESTAMP
        );
        """
        
        create_forecast_table = """
        CREATE TABLE IF NOT EXISTS analytics.previsioni_forecast (
            id SERIAL PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL,
            latitude DECIMAL(8,6) NOT NULL,
            longitude DECIMAL(9,6) NOT NULL,
            forecast_datetime TIMESTAMP NOT NULL,
            temperature DECIMAL(5,2),
            feels_like DECIMAL(5,2),
            temp_min DECIMAL(5,2),
            temp_max DECIMAL(5,2),
            humidity INTEGER,
            pressure INTEGER,
            wind_speed DECIMAL(5,2),
            weather_main VARCHAR(50),
            weather_description VARCHAR(200),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_current_weather_table)
            cursor.execute(create_forecast_table)
            self.connection.commit()
            cursor.close()
            print("Tabelle create/verificate con successo")
        except Exception as e:
            print(f"Errore creazione tabelle: {e}")
            raise

    def insert_current_weather(self, city_name: str, weather_data: Dict):
        upsert_query = """
        INSERT INTO analytics.locazioni_meteo (
            city_name, latitude, longitude, temperature, feels_like, 
            humidity, pressure, wind_speed, weather_main, weather_description,
            api_timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (city_name) 
        DO UPDATE SET
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            temperature = EXCLUDED.temperature,
            feels_like = EXCLUDED.feels_like,
            humidity = EXCLUDED.humidity,
            pressure = EXCLUDED.pressure,
            wind_speed = EXCLUDED.wind_speed,
            weather_main = EXCLUDED.weather_main,
            weather_description = EXCLUDED.weather_description,
            api_timestamp = EXCLUDED.api_timestamp,
            timestamp = CURRENT_TIMESTAMP
        """
        
        try:
            cursor = self.connection.cursor()
            api_timestamp = datetime.fromtimestamp(weather_data['dt'])
            
            cursor.execute(upsert_query, (
                city_name,
                weather_data['coord']['lat'],
                weather_data['coord']['lon'],
                weather_data['main']['temp'],
                weather_data['main']['feels_like'],
                weather_data['main']['humidity'],
                weather_data['main']['pressure'],
                weather_data.get('wind', {}).get('speed', 0),
                weather_data['weather'][0]['main'],
                weather_data['weather'][0]['description'],
                api_timestamp
            ))
            self.connection.commit()
            cursor.close()
            print(f"Dati meteo correnti per {city_name} aggiornati nel database")
        except Exception as e:
            print(f"Errore aggiornamento dati correnti per {city_name}: {e}")

    def insert_forecast_data(self, city_name: str, forecast_data: Dict):
        # Prima elimina solo le previsioni future per questa città (mantiene lo storico passato)
        delete_query = """
        DELETE FROM analytics.previsioni_forecast 
        WHERE city_name = %s AND forecast_datetime >= CURRENT_DATE
        """
        
        # Poi inserisce le nuove previsioni
        insert_query = """
        INSERT INTO analytics.previsioni_forecast (
            city_name, latitude, longitude, forecast_datetime, temperature, 
            feels_like, temp_min, temp_max, humidity, pressure, wind_speed,
            weather_main, weather_description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor = self.connection.cursor()
            
            # Elimina solo le previsioni future per questa città
            cursor.execute(delete_query, (city_name,))
            
            for forecast_item in forecast_data['list']:
                forecast_datetime = datetime.fromtimestamp(forecast_item['dt'])
                
                cursor.execute(insert_query, (
                    city_name,
                    forecast_data['city']['coord']['lat'],
                    forecast_data['city']['coord']['lon'],
                    forecast_datetime,
                    forecast_item['main']['temp'],
                    forecast_item['main']['feels_like'],
                    forecast_item['main']['temp_min'],
                    forecast_item['main']['temp_max'],
                    forecast_item['main']['humidity'],
                    forecast_item['main']['pressure'],
                    forecast_item.get('wind', {}).get('speed', 0),
                    forecast_item['weather'][0]['main'],
                    forecast_item['weather'][0]['description']
                ))
            
            self.connection.commit()
            cursor.close()
            print(f"Previsioni per {city_name} aggiornate (storico mantenuto)")
        except Exception as e:
            print(f"Errore aggiornamento previsioni per {city_name}: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connessione database chiusa")

class WeatherCollector:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict]:
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'it'
            }
            response = requests.get(CURRENT_WEATHER_URL, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Errore nel recupero dati meteo correnti: {e}")
            return None

    def get_forecast(self, lat: float, lon: float) -> Optional[Dict]:
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'it'
            }
            response = requests.get(FORECAST_URL, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Errore nel recupero previsioni: {e}")
            return None

@functions_framework.http
def main(requests):
    host = os.getenv('host')
    database = os.getenv('dbname')
    user = os.getenv('user')
    password = os.getenv('password')
    port = os.getenv('port')

    # Configurazione database
    db_config = {
        'host': host,
        'database': database,
        'user': user,
        'password': password,
        'port': port
    }
    
    db = WeatherDatabase(db_config)
    collector = WeatherCollector(API_KEY)
    
    try:
        # Connessione e setup database
        db.connect()
        db.create_tables()
        
        # Raccolta dati per ogni città
        for city_name, coords in VENETO_CITIES.items():
            print(f"\nRaccogliendo dati per {city_name}...")
            
            # Dati meteo correnti
            current_weather = collector.get_current_weather(coords['lat'], coords['lon'])
            if current_weather:
                db.insert_current_weather(city_name, current_weather)
            
            # Previsioni
            forecast = collector.get_forecast(coords['lat'], coords['lon'])
            if forecast:
                db.insert_forecast_data(city_name, forecast)
        
        print("\nImportazione completata con successo!")
        return "Importazione completata con successo!"
        
    except Exception as e:
        print(f"Errore durante l'importazione: {e}")
    finally:
        db.close()