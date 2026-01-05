# MyApp Vault

## Description

**MyApp Vault** est une application Python sécurisée qui utilise **HashiCorp Vault** pour gérer :

- L'authentification via **AppRole**
- La génération de **credentials dynamiques** pour PostgreSQL
- Le **chiffrement/déchiffrement** de données sensibles avec le moteur Transit
- La lecture de **secrets statiques** depuis le KV store

L'application est construite avec **Flask**, exposant des endpoints HTTP pour interagir avec Vault et la base de données.

---

## Structure du projet

```text
myapp-vault/
├── app.py               # Application principale Flask
├── vault_client.py      # Client Python pour interagir avec Vault
├── requirements.txt     # Dépendances Python
└── .env.example         # Exemple de variables d'environnement
```

# Installation

## Cloner le dépôt :
```text
git clone https://github.com/maryeeem/myapp-vault.git
cd myapp-vault
```

## Installer les dépendances Python :
```text
pip install -r requirements.txt
```

## Configurer les variables d'environnement :
```text
export VAULT_ADDR='http://localhost:8200'
export VAULT_ROLE_ID='<votre-role-id>'
export VAULT_SECRET_ID='<votre-secret-id>'

```
## Astuce : tu peux copier .env.example en .env et remplir tes valeurs.

## Lancement de l'application
```text
python app.py
```

## L'application Flask tourne sur le port 5000

## Accessible sur 
```text
http://127.0.0.1:5000 ou http://<votre-ip>:5000
```
## Endpoints disponibles
## Endpoint	Méthode	Description
```text
/health	GET	Vérifie la santé de l'application et retourne le nom et l'environnement
/encrypt	POST	Chiffre les données envoyées en JSON { "data": "texte à chiffrer" }
/decrypt	POST	Déchiffre le texte chiffré envoyé en JSON { "ciphertext": "vault:v1:..." }
/users	GET	Récupère les 10 premiers utilisateurs de la base de données avec les credentials dynamiques
```
## Exemple de test avec curl
## Vérifier la santé
```text
curl http://127.0.0.1:5000/health
```
## Chiffrement
```text
curl -X POST http://127.0.0.1:5000/encrypt \
  -H "Content-Type: application/json" \
  -d '{"data": "informations sensibles"}'
```
## Déchiffrement
```text
curl -X POST http://127.0.0.1:5000/decrypt \
  -H "Content-Type: application/json" \
  -d '{"ciphertext": "vault:v1:..."}'
```
## Accéder aux utilisateurs
```text
curl http://127.0.0.1:5000/users
```
## Technologies utilisées

```text 
Python 3.10+

Flask

psycopg2

HashiCorp Vault

hvac (Python client Vault)

Notes importantes

Ne jamais mettre le .env réel sur GitHub (utiliser .env.example)

Assurez-vous que Vault est initialisé et déverrouillé avant de lancer l'application

Les credentials DB sont dynamiques et expirent, le renouvellement automatique est intégré


```
