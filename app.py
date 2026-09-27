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

    # Standardize Category
    if 'Category' in df.columns and 'Name' in df.columns:
        def fill_cat(row):
            cat = str(row['Category']).strip()
            if cat in ['N/A', '', 'nan']:
                name = str(row['Name']).lower()
                if any(k in name for k in ['muslim', 'memon', 'bohra', 'islamic', 'dargah', 'azad']):
                    return 'Muslim Minority'
                return 'General'
            return cat
        df['Category'] = df.apply(fill_cat, axis=1)
    
    return df.to_dict(orient='records')

@app.route('/')
def home():
    scholarships = get_data()
    categories = sorted(list(set([s['Category'] for s in scholarships if s.get('Category') and s['Category'] != 'N/A'])))
    return render_template('index.html', scholarships=scholarships, categories=categories)

@app.route('/api/search', methods=['GET'])
def search_api():
    pincode_query = request.args.get('pincode', '').strip()
    selected_category = request.args.get('category', '').strip()
    
    data = get_data()
    
    # 1. Selected Category filter
    if selected_category and selected_category.lower() != 'all':
        data = [item for item in data if str(item.get('Category', '')).lower() == selected_category.lower()]

    exact_results = []
    nearby_list = []

    if not pincode_query:
        return jsonify({
            'exact': data,
            'nearby': []
        })

    target_pin = None
    if pincode_query.isdigit():
        target_pin = int(pincode_query)

    # 2. PinCode match and distance calculation
    for item in data:
        item_pin_str = str(item.get('PinCode', '')).strip()
        
        if item_pin_str == pincode_query:
            exact_results.append(item)
        elif target_pin and item_pin_str.isdigit():
            item_pin = int(item_pin_str)
            diff = abs(item_pin - target_pin)
            nearby_item = item.copy()
            nearby_item['distance'] = diff
            nearby_list.append(nearby_item)
        else:
            nearby_item = item.copy()
            nearby_item['distance'] = 999999
            nearby_list.append(nearby_item)

    # 3. Sort nearby by proximity (1st nearest order)
    nearby_list.sort(key=lambda x: x['distance'])

    return jsonify({
        'exact': exact_results,
        'nearby': nearby_list
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
