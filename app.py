from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, 'data', 'EduBridge_Database_Data.xlsx')

def get_data():
    if not os.path.exists(EXCEL_FILE):
        return []
    
    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna('N/A')
    
    def clean_pincode(x):
        try:
            if isinstance(x, (int, float)) and not pd.isna(x):
                return str(int(x))
            val = str(x).strip()
            if val.endswith('.0'):
                val = val[:-2]
            return val
        except:
            return str(x).strip()

    if 'PinCode' in df.columns:
        df['PinCode'] = df['PinCode'].apply(clean_pincode)
    
    return df.to_dict(orient='records')

@app.route('/')
def home():
    scholarships = get_data()
    return render_template('index.html', scholarships=scholarships)

@app.route('/api/search', methods=['GET'])
def search_api():
    pincode_query = request.args.get('pincode', '').strip()
    
    data = get_data()
    exact_results = []
    nearby_results = []

    if not pincode_query:
        return jsonify({
            'exact': data,
            'nearby': []
        })

    target_pin = None
    if pincode_query.isdigit():
        target_pin = int(pincode_query)

    for item in data:
        item_pin_str = str(item.get('PinCode', '')).strip()
        
        # Exact match check
        if item_pin_str == pincode_query:
            exact_results.append(item)
        elif target_pin and item_pin_str.isdigit():
            item_pin = int(item_pin_str)
            # Nearby pincode (+/- 2 range)
            if abs(item_pin - target_pin) <= 2 and item_pin != target_pin:
                nearby_results.append(item)

    return jsonify({
        'exact': exact_results,
        'nearby': nearby_results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
