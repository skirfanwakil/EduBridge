from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Path to dataset relative to directory root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, 'data', 'EduBridge_Database_Data.xlsx')

def get_data():
    if not os.path.exists(EXCEL_FILE):
        return []
    
    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna('N/A')
    
    # Standardize PinCode string representation
    if 'PinCode' in df.columns:
        df['PinCode'] = df['PinCode'].apply(
            lambda x: str(int(x)) if isinstance(x, (int, float)) and not pd.isna(x) and str(x) != 'N/A' else str(x)
        )
    
    # Fill empty categories
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
    query = request.args.get('q', '').lower().strip()
    category = request.args.get('category', '').strip()
    
    data = get_data()
    filtered = []

    for item in data:
        match_query = (
            query in str(item.get('Name', '')).lower() or
            query in str(item.get('Address', '')).lower() or
            query in str(item.get('PinCode', '')).lower() or
            query in str(item.get('Contact', '')).lower()
        )
        
        item_cat = str(item.get('Category', '')).lower()
        match_category = (category == '' or category.lower() == 'all' or item_cat == category.lower())

        if match_query and match_category:
            filtered.append(item)

    return jsonify(filtered)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
