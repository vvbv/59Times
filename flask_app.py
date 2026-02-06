"""
Flask microservice for 59-based time functionality.
This module provides web API endpoints and a web interface for the 59Times clock.
"""

from flask import Flask, jsonify, render_template_string
from datetime import datetime
import pytz

# Import core time functions from main.py
from main import TIME_RELATION, clock59, currentDaySecondStandardTime, formatTime

app = Flask(__name__)

# HTML template for the /time web interface
TIME_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>59Times Clock</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #ffffff;
            color: #000000;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .clock-container {
            text-align: center;
            padding: 3rem;
            border: 2px solid #000000;
            border-radius: 0;
        }
        .time-display {
            font-size: 5rem;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            letter-spacing: 0.1em;
        }
        .label {
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            margin-top: 0.5rem;
        }
        .standard-time {
            font-size: 1.5rem;
            font-family: 'Courier New', monospace;
            margin-top: 1rem;
            color: #555555;
        }
        .divider {
            width: 100px;
            height: 2px;
            background-color: #000000;
            margin: 1.5rem auto;
        }
        h1 {
            font-weight: 300;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-auto">
                <div class="clock-container">
                    <h1>59Times</h1>
                    <div class="time-display" id="time59">{{ time_59 }}</div>
                    <div class="label">59-Based Time</div>
                    <div class="divider"></div>
                    <div class="standard-time" id="standardTime">{{ standard_time }}</div>
                    <div class="label">Standard Time ({{ timezone }})</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function updateTime() {
            fetch('/api/time')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('time59').textContent = data.time_59;
                    document.getElementById('standardTime').textContent = data.standard_time;
                })
                .catch(error => console.error('Error fetching time:', error));
        }
        
        // Update every second
        setInterval(updateTime, 1000);
    </script>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


def get_standard_time(timezone_str='UTC'):
    """Get current time in the specified timezone."""
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        return now.strftime('%H:%M:%S')
    except pytz.UnknownTimeZoneError:
        # Fallback to local time
        return datetime.now().strftime('%H:%M:%S')


def get_ms_to_next_second(tz=None):
    """Calculate milliseconds remaining until the next second."""
    if tz:
        now = datetime.now(tz)
    else:
        now = datetime.now()
    microseconds_remaining = 1000000 - now.microsecond
    return int(microseconds_remaining / 1000)


def get_ms_to_next_minute(tz=None):
    """Calculate milliseconds remaining until the next minute."""
    if tz:
        now = datetime.now(tz)
    else:
        now = datetime.now()
    seconds_remaining = 60 - now.second - 1
    microseconds_remaining = 1000000 - now.microsecond
    total_ms = (seconds_remaining * 1000) + int(microseconds_remaining / 1000)
    return total_ms


def clock59_from_seconds(current_seconds):
    """
    Calculate 59-based time from seconds since midnight.
    This helper function is used to avoid duplicating the conversion logic.
    """
    current_seconds_59 = current_seconds * TIME_RELATION
    current_hour = current_seconds_59 / pow(59, 2)
    current_minute = (59/100) * ((current_hour - int(current_hour)) * 100)
    current_second = (59/100) * ((current_minute - int(current_minute)) * 100)
    return [int(current_hour), int(current_minute), int(current_second)]


def clock59_with_timezone(timezone_str='UTC'):
    """
    Calculate 59-based time for a specific timezone.
    Uses the same algorithm as clock59() but applies timezone offset.
    """
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        # Calculate seconds since midnight in the given timezone
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        current_seconds = (now - midnight).total_seconds()
        
        return clock59_from_seconds(current_seconds)
    except pytz.UnknownTimeZoneError:
        # Fallback to local time calculation
        return clock59()


@app.route('/')
def index():
    """Root endpoint - redirects to /time."""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/time">
    </head>
    <body>
        <p>Redirecting to <a href="/time">/time</a>...</p>
    </body>
    </html>
    ''')


@app.route('/time')
def time_page():
    """Web interface displaying the current time."""
    time_59_list = clock59()
    time_59 = formatTime(time_59_list)
    standard_time = get_standard_time('UTC')
    
    return render_template_string(
        TIME_PAGE_TEMPLATE,
        time_59=time_59,
        standard_time=standard_time,
        timezone='UTC'
    )


@app.route('/api/time')
def api_time():
    """
    API endpoint: Get current server time in 59-based format.
    Returns JSON with time_59, standard_time, timezone, and calibration values.
    """
    time_59_list = clock59()
    
    return jsonify({
        'time_59': formatTime(time_59_list),
        'standard_time': get_standard_time('UTC'),
        'timezone': 'UTC',
        'ms_to_next_second': get_ms_to_next_second(),
        'ms_to_next_minute': get_ms_to_next_minute()
    })


@app.route('/api/time/<path:timezone_str>')
def api_time_timezone(timezone_str):
    """
    API endpoint: Get current time in a specified timezone converted to 59-based format.
    
    Args:
        timezone_str: Timezone string (e.g., 'America/New_York', 'Europe/London')
    
    Returns JSON with time_59, standard_time, timezone, and calibration values.
    """
    try:
        # Validate timezone and get timezone object
        tz = pytz.timezone(timezone_str)
        time_59_list = clock59_with_timezone(timezone_str)
        
        return jsonify({
            'time_59': formatTime(time_59_list),
            'standard_time': get_standard_time(timezone_str),
            'timezone': timezone_str,
            'ms_to_next_second': get_ms_to_next_second(tz),
            'ms_to_next_minute': get_ms_to_next_minute(tz)
        })
    except pytz.UnknownTimeZoneError:
        return jsonify({
            'error': f'Unknown timezone: {timezone_str}',
            'valid_example': 'America/New_York, Europe/London, Asia/Tokyo'
        }), 400


@app.route('/api/calibration')
def api_calibration():
    """
    API endpoint: Get calibration values for clock synchronization.
    Returns milliseconds until next second and next minute.
    """
    return jsonify({
        'ms_to_next_second': get_ms_to_next_second(),
        'ms_to_next_minute': get_ms_to_next_minute(),
        'time_relation': TIME_RELATION
    })


if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
