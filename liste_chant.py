import requests
import pandas as pd

# Remplacez 'YOUR_ACCESS_TOKEN' par votre véritable jeton d'accès Spotify
access_token = 'BQBdkQ0Ieh2MRG3KLNP_A3MEmNt5ArsImsWCf2bmp8CoB_UOSkar-VKB-DnNZtf4prMLZknK_UGoZiI2ceaaSz_7VVOO7H9pe3jIeiOLhAwE_FDW9Ng'

# URL de l'API Spotify pour récupérer une playlist spécifique
playlist_api_url = 'https://api.spotify.com/v1/playlists/37i9dQZEVXbKQ1ogMOyW9N'

# En-tête contenant le jeton d'accès
headers = {
    'Authorization': 'Bearer ' + access_token
}

# Envoi de la demande GET à l'API Spotify
response = requests.get(playlist_api_url, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    playlist_data = response.json()

    # Utiliser json_normalize pour aplatir les données JSON imbriquées
    df = pd.json_normalize(playlist_data['tracks']['items'])

    # Export vers un fichier Excel
    df.to_excel('playlist.xlsx', index=False)

    # Export vers un fichier CSV
    df.to_csv('playlist.csv', index=False)

    print('Exportation terminée.')
else:
    print('Erreur lors de la demande :', response.status_code)
print(df)