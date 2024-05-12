import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_artist_names(artists_list):
    # Extraire les noms des artistes de la liste
    return [artist['name'] for artist in artists_list]

def get_lyrics(song, artist):
    # Construire l'URL de recherche Musixmatch
    search_url = f"https://www.musixmatch.com/fr/recherche?query={song} {artist}"
    
    # Envoyer une demande GET à l'URL de recherche
    response = requests.get(search_url)
    
    # Vérifier si la demande a réussi
    if response.status_code == 200:
        # Analyser le contenu HTML de la page de recherche
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver l'élément contenant les paroles (peut varier selon le site)
        lyrics_element = soup.find('span', class_='lyrics__content__ok')
        
        # Extraire les paroles si l'élément est trouvé
        if lyrics_element:
            return lyrics_element.text.strip()
        else:
            return "Paroles non trouvées"
    else:
        return "Erreur lors de la requête"

# Charger la liste de chansons et d'artistes depuis un fichier Excel ou CSV
df = pd.read_csv('playlist.csv')

# Convertir la chaîne de caractères en une liste de dictionnaires
df['track.album.artists'] = df['track.album.artists'].apply(eval)

# Créer une liste pour stocker les données des paroles
lyrics_data = []

# Parcourir chaque chanson et obtenir les paroles
for index, row in df.iterrows():
    song = row['track.name']
    artists = extract_artist_names(row['track.album.artists'])
    
    # Parcourir chaque artiste et obtenir les paroles de la chanson
    for artist in artists:
        lyrics = get_lyrics(song, artist)
        lyrics_data.append({'Song': song, 'Artist': artist, 'Lyrics': lyrics})
        print(lyrics)

# Créer une DataFrame à partir des données des paroles
lyrics_df = pd.DataFrame(lyrics_data)

# Sauvegarder la DataFrame dans un fichier Excel
lyrics_df.to_excel('paroles.xlsx', index=False)

# Sauvegarder la DataFrame dans un fichier CSV
lyrics_df.to_csv('paroles.csv', index=False)
