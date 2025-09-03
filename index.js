const axios = require('axios');

const API_KEY = '1114aa33423b17900d48b4962229ee34';
const CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather';
const FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast';

const venetoCities = {
    'Venezia': { lat: 45.4408, lon: 12.3155 },
    'Verona': { lat: 45.4384, lon: 10.9916 },
    'Padova': { lat: 45.4064, lon: 11.8768 },
    'Vicenza': { lat: 45.5477, lon: 11.5448 },
    'Treviso': { lat: 45.6669, lon: 12.2433 },
    'Rovigo': { lat: 45.0712, lon: 11.7904 },
    'Belluno': { lat: 46.1432, lon: 12.2136 }
};



async function getWeatherData(lat, lon, cityName) {
    try {
        const [currentResponse, forecastResponse] = await Promise.all([
            axios.get(CURRENT_WEATHER_URL, {
                params: {
                    lat: lat,
                    lon: lon,
                    appid: API_KEY,
                    units: 'metric',
                    lang: 'it'
                }
            }),
            axios.get(FORECAST_URL, {
                params: {
                    lat: lat,
                    lon: lon,
                    appid: API_KEY,
                    units: 'metric',
                    lang: 'it'
                }
            })
        ]);

        const currentWeather = currentResponse.data;
        const forecast = forecastResponse.data;
        
        console.log(`\n=== PREVISIONI METEO PER ${cityName.toUpperCase()} ===`);
        console.log(`Temperatura attuale: ${currentWeather.main.temp}°C (percepita: ${currentWeather.main.feels_like}°C)`);
        console.log(`Condizioni: ${currentWeather.weather[0].description}`);
        console.log(`Umidità: ${currentWeather.main.humidity}%`);
        console.log(`Velocità del vento: ${currentWeather.wind.speed} m/s`);
        console.log(`Pressione: ${currentWeather.main.pressure} hPa`);
        
        console.log(`\nPREVISIONI PROSSIMI GIORNI:`);
        const dailyForecasts = {};
        
        forecast.list.forEach(item => {
            const date = new Date(item.dt * 1000).toLocaleDateString('it-IT');
            if (!dailyForecasts[date]) {
                dailyForecasts[date] = {
                    temps: [],
                    conditions: item.weather[0].description,
                    date: date
                };
            }
            dailyForecasts[date].temps.push(item.main.temp);
        });
        
        Object.values(dailyForecasts).slice(0, 5).forEach(day => {
            const minTemp = Math.min(...day.temps);
            const maxTemp = Math.max(...day.temps);
            console.log(`${day.date}: ${minTemp.toFixed(1)}°C - ${maxTemp.toFixed(1)}°C, ${day.conditions}`);
        });
        
        return { current: currentWeather, forecast: forecast };
    } catch (error) {
        console.error(`Errore nel recuperare i dati meteo per ${cityName}:`, error.message);
        return null;
    }
}

async function getAllVenetoWeather() {
    console.log('🌤️  PREVISIONI METEO VENETO 🌤️');
    console.log('=====================================');
    
    for (const [cityName, coords] of Object.entries(venetoCities)) {
        await getWeatherData(coords.lat, coords.lon, cityName);
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}

async function getSingleCityWeather(cityName) {
    const city = venetoCities[cityName];
    if (!city) {
        console.log(`Città "${cityName}" non trovata. Città disponibili: ${Object.keys(venetoCities).join(', ')}`);
        return;
    }
    
    await getWeatherData(city.lat, city.lon, cityName);
}

function showHelp() {
    console.log('\n📋 COMANDI DISPONIBILI:');
    console.log('node index.js                    - Mostra meteo per tutte le città del Veneto');
    console.log('node index.js [nome-città]       - Mostra meteo per una città specifica');
    console.log('node index.js help              - Mostra questo messaggio');
    console.log('\n🏙️  CITTÀ DISPONIBILI:');
    console.log(Object.keys(venetoCities).join(', '));
}

async function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        await getAllVenetoWeather();
    } else if (args[0] === 'help') {
        showHelp();
    } else {
        const cityName = args[0].charAt(0).toUpperCase() + args[0].slice(1).toLowerCase();
        await getSingleCityWeather(cityName);
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = { getWeatherData, getAllVenetoWeather, getSingleCityWeather };