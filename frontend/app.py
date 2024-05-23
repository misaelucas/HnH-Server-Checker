from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Generate more mock data
crash_count = 100  # Increase the number of crashes for more data points
crash_dates = []

for _ in range(crash_count):
    random_days_ago = random.randint(0, 59)
    random_time = datetime.now() - timedelta(days=random_days_ago)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    crash_date = random_time.replace(hour=random_hour, minute=random_minute, second=random_second)
    crash_dates.append(crash_date.strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        "crash_count": crash_count,
        "crash_dates": crash_dates
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
