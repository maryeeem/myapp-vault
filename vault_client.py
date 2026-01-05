import hvac
import base64
import os
from typing import Dict

class VaultClient:
    def __init__(self):
        self.vault_addr = os.getenv('VAULT_ADDR', 'http://localhost:8200')
        self.role_id = os.getenv('VAULT_ROLE_ID')
        self.secret_id = os.getenv('VAULT_SECRET_ID')
        self.client = None
        self._authenticate()
    
    def _authenticate(self):
        self.client = hvac.Client(url=self.vault_addr)
        response = self.client.auth.approle.login(
            role_id=self.role_id,
            secret_id=self.secret_id
        )
        print(f"✓ Authentifié avec succès, Token TTL: {response['auth']['lease_duration']}s")
    
    def get_db_credentials(self) -> Dict[str, str]:
        response = self.client.secrets.database.generate_credentials(name='myapp-role')
        creds = {
            'username': response['data']['username'],
            'password': response['data']['password'],
            'lease_id': response['lease_id'],
            'lease_duration': response['lease_duration']
        }
        return creds
    
    def encrypt_data(self, plaintext: str) -> str:
        plaintext_b64 = base64.b64encode(plaintext.encode()).decode()
        response = self.client.secrets.transit.encrypt_data(name='myapp-key', plaintext=plaintext_b64)
        return response['data']['ciphertext']
    
    def decrypt_data(self, ciphertext: str) -> str:
        response = self.client.secrets.transit.decrypt_data(name='myapp-key', ciphertext=ciphertext)
        plaintext_b64 = response['data']['plaintext']
        return base64.b64decode(plaintext_b64).decode()
    
    def get_config(self, path: str) -> Dict:
        response = self.client.secrets.kv.v2.read_secret_version(path=path)
        return response['data']['data']
