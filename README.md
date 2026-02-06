# 59Times
Why?, R:// Why not?

❌ 23:59:59 ✅ 59:59:59

## Usage

### Requirements
- Python 3
- PyQt5
- Flask (for web interface)
- pytz (for timezone support)

Install dependencies:
```
pip install -r requirements.txt
```

### Running the Desktop Clock (PyQt5 GUI)
Simply execute the main.py file:
```
python main.py
```

This will open a window displaying the current time in 59-based format in both analog and digital visualizations. The time is also written to a file named `clock59.txt`.

### Running the Flask Web Service
Start the Flask microservice:
```
python flask_app.py
```

The web service will be available at `http://localhost:5000`.

For development with debug mode enabled:
```
FLASK_DEBUG=true python flask_app.py
```

#### Web Interface
- **`/time`** - Elegant black and white web interface displaying the current 59-based time

#### API Endpoints
- **`GET /api/time`** - Get current server time in 59-based format
  ```json
  {
    "time_59": "45:32:18",
    "standard_time": "18:45:30",
    "timezone": "UTC",
    "ms_to_next_second": 523,
    "ms_to_next_minute": 30523
  }
  ```

- **`GET /api/time/<timezone>`** - Get time in a specific timezone (e.g., `/api/time/America/New_York`)
  ```json
  {
    "time_59": "40:12:55",
    "standard_time": "13:45:30",
    "timezone": "America/New_York",
    "ms_to_next_second": 523,
    "ms_to_next_minute": 30523
  }
  ```

- **`GET /api/calibration`** - Get calibration values for clock synchronization
  ```json
  {
    "ms_to_next_second": 523,
    "ms_to_next_minute": 30523,
    "time_relation": 2.3727766203703704
  }
  ```

### Features

#### Desktop Application (PyQt5)
- Digital clock showing hours, minutes, and seconds in 59-based format
- Analog clock visualization with:
  - Clock face with 59 hour markers
  - Hour hand (blue)
  - Minute hand (green)
  - Second hand (red)
- Time is also output to `clock59.txt` for external use

#### Web Service (Flask)
- Clean, minimalist web interface with black and white design
- RESTful API endpoints for time data
- Timezone conversion support
- Calibration endpoints for clock synchronization