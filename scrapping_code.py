import urllib.parse
import urllib.request
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
    print(url)
    
    with urllib.request.urlopen(url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # Recherche de la balise "a" avec la classe spécifiée et un attribut "href"
            link_element = soup.find('a', class_='css-175oi2r r-1otgn73', href=True)
            if link_element:
                # Obtenir l'URL du deuxième lien
                lyrics_url = link_element['href']
                print(lyrics_url)
                # Accéder à la page des paroles
                with urllib.request.urlopen(lyrics_url) as lyrics_response:
                    lyrics_html = lyrics_response.read()
                    lyrics_soup = BeautifulSoup(lyrics_html, 'html.parser')
                    # Trouver l'élément contenant les paroles
                    lyrics_element = lyrics_soup.find('div', class_='css-175oi2r r-13awgt0 r-eqz5dr r-1v1z2uz')
                    if lyrics_element:
                        return lyrics_element.text.strip()              
            return "Paroles non trouvées"    


# Charger la liste de chansons et d'artistes depuis un fichier Excel ou CSV
df = pd.read_csv('playlist.csv')

# Convertir la chaîne de caractères en une liste de dictionnaires
df['track.album.artists'] = df['track.album.artists'].apply(eval)

# Créer une liste pour stocker les données des paroles
lyrics_data = []

# Parcourir les deux premières chansons et obtenir les paroles
for index, row in df.head(3).iterrows():  # Limiter aux deux premières lignes
    song = row['track.name']
    artists = extract_artist_names(row['track.album.artists'])
    
    # Obtenir les paroles pour la chanson avec tous les artistes
    lyrics = get_lyrics(song, artists)
    
    # Afficher les paroles de chaque chanson avec ses artistes
    print(f"Paroles de '{song}' par {', '.join(artists)}:")
    print(lyrics)
    
    # Ajouter les données des paroles à la liste si nécessaire
    # lyrics_data.append({'Song': song, 'Artists': artists, 'Lyrics': lyrics})