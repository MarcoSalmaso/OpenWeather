# OpenWeather Veneto 🌤️

Una semplice applicazione Node.js per recuperare le previsioni meteo delle principali città del Veneto utilizzando le API di OpenWeather.

## Caratteristiche

- **Previsioni complete**: Meteo attuale e previsioni a 5 giorni
- **Città del Veneto**: Include le 7 città principali (Venezia, Verona, Padova, Vicenza, Treviso, Rovigo, Belluno)
- **Interfaccia italiana**: Descrizioni meteo in italiano
- **Flessibile**: Visualizza tutte le città o una città specifica

## Prerequisiti

- Node.js (versione 12 o superiore)
- Connessione internet per le chiamate API

## Installazione

1. Clona o scarica questo repository
2. Installa le dipendenze:
   ```bash
   npm install
   ```

## Utilizzo

### Visualizzare meteo per tutte le città del Veneto
```bash
npm start
# oppure
node index.js
```

### Visualizzare meteo per una città specifica
```bash
node index.js Venezia
node index.js Verona
node index.js Padova
# ... e così via
```

### Mostrare l'aiuto
```bash
node index.js help
```

## Città supportate

- **Venezia**
- **Verona** 
- **Padova**
- **Vicenza**
- **Treviso**
- **Rovigo**
- **Belluno**

## Output dell'applicazione

L'applicazione mostra:
- Temperatura attuale
- Condizioni meteo (in italiano)
- Umidità
- Velocità del vento
- Previsioni per i prossimi 5 giorni con temperature min/max

## API utilizzate

- **OpenWeather One Call API 3.0**: `https://openweathermap.org/api/one-call-3`
- **Endpoint**: `https://api.openweathermap.org/data/3.0/onecall`
- **Parametri**: coordinate geografiche, API key, unità metriche, lingua italiana

## Struttura del progetto

```
OpenWeather/
├── index.js          # File principale dell'applicazione
├── package.json      # Configurazione del progetto Node.js
└── README.md         # Documentazione (questo file)
```

## Dipendenze

- **axios**: Per le chiamate HTTP alle API di OpenWeather

## Risoluzione problemi API key

Se vedi l'errore "API KEY NON VALIDA", verifica:

1. **Attivazione**: Le nuove API key richiedono alcune ore per attivarsi
2. **Account verificato**: Controlla la tua email per confermare l'account
3. **Subscription**: Verifica di avere accesso alle API Current Weather e 5 Day Forecast
4. **Test manuale**: Prova questo comando per testare la tua API key:
   ```bash
   curl "https://api.openweathermap.org/data/2.5/weather?lat=45.4408&lon=12.3155&appid=TUA_API_KEY&units=metric"
   ```

## Note tecniche

- L'applicazione implementa un delay tra le chiamate API per rispettare i rate limits
- Utilizza coordinate geografiche precise per ogni città
- Gestisce gli errori di rete e API con fallback a dati demo
- Formattazione delle date in formato italiano
- Mostra dati di esempio se l'API key non è valida

## Licenza

ISC

---

*Sviluppato per fornire previsioni meteo accurate per il Veneto* 🇮🇹