import requests
import base64

client_id = '65fc5f23c0dc43739c3034f06db20b7e'
client_secret = '2d9d378e874f469783b2b6cc848389ab'

# Création des en-têtes et des paramètres de la demande
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')
headers = {
    'Authorization': f'Basic {auth_header}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'client_credentials'
}

# Envoi de la demande POST pour obtenir le token d'accès
response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

# Vérification de la réponse
if response.status_code == 200:
    token = response.json()['access_token']
    print(token)
else:
    print("Erreur lors de la demande :", response.status_code)
