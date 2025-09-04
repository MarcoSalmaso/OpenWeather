# OpenWeather Veneto 🌤️

Applicazione Python per importare automaticamente i dati meteo delle principali città del Veneto in un database PostgreSQL utilizzando le API di OpenWeather.

## Caratteristiche

- **Import automatico**: Dati meteo correnti e previsioni a 5 giorni
- **Database PostgreSQL**: Salvataggio strutturato dei dati nello schema `analytics`
- **Storico mantenuto**: Le previsioni passate diventano dati storici
- **Città del Veneto**: Include le 7 città principali (Venezia, Verona, Padova, Vicenza, Treviso, Rovigo, Belluno)
- **Cloud Functions**: Può essere deployato come Google Cloud Function
- **Configurazione flessibile**: Supporta variabili d'ambiente

## Prerequisiti

- Python 3.7 o superiore
- Database PostgreSQL
- API Key di OpenWeather

## Installazione

1. Clona o scarica questo repository
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Configurazione

### Variabili d'ambiente
Crea un file `.env` o imposta le seguenti variabili:

```bash
# API OpenWeather
api=your_openweather_api_key

# Database PostgreSQL
host=localhost
dbname=postgres
user=postgres
password=your_password
port=5432
```

## Utilizzo

### Esecuzione locale
```bash
python3 weather_import.py
```

### Deploy come Cloud Function
```bash
# Il file è già configurato per Google Cloud Functions
# Usa functions_framework per il deploy
```

## Struttura Database

### Tabelle create automaticamente:

#### `analytics.locazioni_meteo`
Dati meteo correnti (1 record per città, sempre aggiornato):
- `city_name` - Nome città
- `latitude`, `longitude` - Coordinate
- `temperature`, `feels_like` - Temperature attuali 
- `humidity`, `pressure`, `wind_speed` - Dati atmosferici
- `weather_main`, `weather_description` - Condizioni meteo
- `api_timestamp` - Timestamp dai dati API
- `timestamp` - Timestamp inserimento

#### `analytics.previsioni_forecast`
Previsioni meteo storiche e future:
- `city_name` - Nome città  
- `forecast_datetime` - Data/ora della previsione
- `temperature`, `feels_like`, `temp_min`, `temp_max` - Temperature
- `humidity`, `pressure`, `wind_speed` - Dati atmosferici
- `weather_main`, `weather_description` - Condizioni meteo
- `timestamp` - Timestamp inserimento

## Città supportate

- **Venezia** - 45.4408°N, 12.3155°E
- **Verona** - 45.4384°N, 10.9916°E
- **Padova** - 45.4064°N, 11.8768°E
- **Vicenza** - 45.5477°N, 11.5448°E
- **Treviso** - 45.6669°N, 12.2433°E
- **Rovigo** - 45.0712°N, 11.7904°E
- **Belluno** - 46.1432°N, 12.2136°E

## API utilizzate

- **OpenWeather Current Weather API**: `https://api.openweathermap.org/data/2.5/weather`
- **OpenWeather 5 Day Forecast API**: `https://api.openweathermap.org/data/2.5/forecast`
- **Parametri**: coordinate geografiche, API key, unità metriche, lingua italiana

## Struttura del progetto

```
OpenWeather/
├── weather_import.py     # Script principale Python
├── requirements.txt      # Dipendenze Python
├── .env.example         # Template variabili d'ambiente
└── README.md            # Documentazione (questo file)
```

## Dipendenze

- **requests**: Per le chiamate HTTP alle API di OpenWeather
- **psycopg2-binary**: Connettore PostgreSQL
- **functions-framework**: Per Google Cloud Functions

## Funzionalità avanzate

### Gestione dello storico
- **Dati correnti**: Sempre aggiornati (1 record per città)
- **Previsioni**: Le previsioni passate diventano dati storici
- **Aggiornamento smart**: Solo le previsioni future vengono aggiornate

### Prevenzione duplicati
- Vincoli di unicità per evitare record duplicati
- UPSERT per aggiornamenti sicuri

## Risoluzione problemi

### API Key non valida
1. **Attivazione**: Le nuove API key richiedono alcune ore per attivarsi
2. **Account verificato**: Controlla la tua email per confermare l'account  
3. **Test manuale**: 
   ```bash
   curl "https://api.openweathermap.org/data/2.5/weather?lat=45.4408&lon=12.3155&appid=TUA_API_KEY&units=metric"
   ```

### Errori database
- Verifica che PostgreSQL sia in esecuzione
- Controlla le credenziali di connessione
- Assicurati che lo schema `analytics` esista

## Note tecniche

- **Rate limiting**: Rispetta i limiti delle API OpenWeather
- **Coordinate precise**: Utilizza coordinate geografiche accurate per ogni città
- **Gestione errori**: Logging dettagliato per debugging
- **Timezone**: Tutti i timestamp sono in UTC

## Licenza

ISC

---

*Sviluppato per fornire previsioni meteo accurate per il Veneto* 🇮🇹