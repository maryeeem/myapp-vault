from flask import Flask, jsonify, request
import psycopg2
from vault_client import VaultClient
import time

app = Flask(__name__)
vault = VaultClient()

db_creds = None
db_creds_expiry = 0

def get_db_connection():
    global db_creds, db_creds_expiry
    if time.time() > db_creds_expiry:
        db_creds = vault.get_db_credentials()
        db_creds_expiry = time.time() + db_creds['lease_duration'] - 300
    conn = psycopg2.connect(
        host='localhost',
        database='myapp',
        user=db_creds['username'],
        password=db_creds['password']
    )
    return conn

@app.route('/health')
def health():
    config = vault.get_config('myapp/config')
    return jsonify({
        'status': 'healthy',
        'app_name': config['app_name'],
        'environment': config['env']
    })

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json.get('data')
    ciphertext = vault.encrypt_data(data)
    return jsonify({'ciphertext': ciphertext})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    ciphertext = request.json.get('ciphertext')
    plaintext = vault.decrypt_data(ciphertext)
    return jsonify({'plaintext': plaintext})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users LIMIT 10")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'users': [{'id': u[0], 'email': u[1]} for u in users], 'db_user': db_creds['username']})

if __name__ == '__main__':
    db_creds = vault.get_db_credentials()
    db_creds_expiry = time.time() + db_creds['lease_duration'] - 300
    app.run(debug=True, host='0.0.0.0', port=5000)

