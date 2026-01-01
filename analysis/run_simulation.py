import sys
import os

# Agregar el directorio raíz al path para importar el modelo principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import traceback

# Import heavy model lazily inside the endpoint to avoid slow startup

app = Flask(__name__)
CORS(app)

# Use the script directory as output dir to avoid cwd issues when serving files
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json()
        # read params with defaults
        capacity_kwh = float(data.get('capacity_kwh', 1000))
        power_kw = float(data.get('power_kw', 500))
        temp_celsius = float(data.get('temp_celsius', 30))
        dod = float(data.get('dod', 0.95))
        cycles_per_day = float(data.get('cycles_per_day', 1))
        c_rate = float(data.get('c_rate', 0.5))
        soc_min = float(data.get('soc_min', 0.05))
        soc_max = float(data.get('soc_max', 0.95))
        eol_threshold = float(data.get('eol_threshold', 80))

        # Lazy import - usar modelo V3.2 LFP Universal
        from bess_degradation_model_v3 import BESSDegradationModelLFP
        model = BESSDegradationModelLFP(capacity_kwh=capacity_kwh, power_kw=power_kw, temp_celsius=temp_celsius, dod=dod)

        # Run annual and lifetime simulation
        annual = model.annual_degradation(cycles_per_day=cycles_per_day, c_rate=c_rate, soc_min=soc_min, soc_max=soc_max)
        df_lifetime, years = model.simulate_lifetime(cycles_per_day=cycles_per_day, c_rate=c_rate, soc_min=soc_min, soc_max=soc_max, eol_threshold=eol_threshold)

        # Save CSV
        import time
        csv_name = f"bess_simulation_{int(time.time() % 1e6)}.csv"
        csv_path = os.path.join(OUTPUT_DIR, csv_name)
        df_lifetime.to_csv(csv_path, index=False)

        summary = {
            'years_to_EOL': int(years),
            'annual_total_degradation_percent': round(annual['total_degradation']*100, 4),
            'soh_percent': round(annual['soh'], 2),
            'residual_capacity_kwh': round(annual['residual_capacity_kwh'], 2)
        }

        return jsonify({'summary': summary, 'csv_path': csv_name})

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({'error': str(e), 'traceback': tb}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route('/', methods=['GET'])
def index():
    """Serve bess_simulator.html from script directory"""
    html_path = os.path.join(OUTPUT_DIR, 'bess_simulator.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    else:
        return f"<h1>Error: HTML file not found</h1><p>Looking for: {html_path}</p>", 404

if __name__ == '__main__':
    # Run server on port 5000
    app.run(host='127.0.0.1', port=5000)
