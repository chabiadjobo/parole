import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import requests

def extract_artist_names(artists_list):
    # Extraire les noms des artistes de la liste
    return [artist['name'] for artist in artists_list]

def get_lyrics(song, artists):
    # Concaténer les noms des artistes en une seule chaîne séparée par des espaces
    artists_str = ' '.join(artists)
    query = urllib.parse.quote(f"{song} {artists_str}")
    url = f"https://www.musixmatch.com/fr/recherche?query={query}"
    print(f"Recherche URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Recherche de la balise "a" avec la classe spécifiée et un attribut "href" correct
    link_element = soup.find('div', class_='css-175oi2r').find('a', class_='css-175oi2r r-13awgt0 r-eqz5dr r-1v1z2uz', href=True)
    if link_element and '/fr/paroles/' in link_element['href']:
        # Obtenir l'URL du deuxième lien
        lyrics_url = f"https://www.musixmatch.com{link_element['href']}"
        print(f"Paroles URL: {lyrics_url}")
        
        # Accéder à la page des paroles
        response_lyrics = requests.get(lyrics_url, headers=headers)
        lyrics_soup = BeautifulSoup(response_lyrics.text, 'html.parser')
        
        # Trouver l'élément contenant les paroles
        lyrics_element = lyrics_soup.find('span', class_='lyrics__content__ok')
        if lyrics_element:
            return lyrics_element.text.strip()
    return "Paroles non trouvées"

# Charger la liste de chansons et d'artistes depuis un fichier Excel ou CSV
df = pd.read_csv('playlist.csv')

# Convertir la chaîne de caractères en une liste de dictionnaires
df['track.album.artists'] = df['track.album.artists'].apply(eval)

# Créer une liste pour stocker les données des paroles
lyrics_data = []

# Parcourir les trois premières chansons et obtenir les paroles
for index, row in df.head(3).iterrows():
    song = row['track.name']
    artists = extract_artist_names(row['track.album.artists'])
    
    # Obtenir les paroles pour la chanson avec tous les artistes
    lyrics = get_lyrics(song, artists)
    
    # Afficher les paroles de chaque chanson avec ses artistes
    print(f"Paroles de '{song}' par {', '.join(artists)}:")
    print(lyrics)
    
    # Ajouter les données des paroles à la liste si nécessaire
    # lyrics_data.append({'Song': song, 'Artists': artists, 'Lyrics': lyrics})
