import json
import os
import urllib.request
import sys
import time
from youtubesearchpython import VideosSearch
from pytube import YouTube

PYTHON_EXECUTABLE = os.path.join(os.path.dirname(sys.executable), 'python.exe')  

# Third-party packages check
print('Importing third-party libraries')
try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except ImportError:
    print('spotipy is not installed.')
    print('\t"{0}" -m pip install spotipy'.format(PYTHON_EXECUTABLE))
    input()
    sys.exit(1)

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, APIC, error
    from mutagen.easyid3 import EasyID3
except ImportError:
    print('mutagen is not installed.')
    print('\t"{0}" -m pip install mutagen'.format(PYTHON_EXECUTABLE))
    input()
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('beautifulsoup4 is not installed.')
    print('\t"{0}" -m pip install beautifulsoup4'.format(PYTHON_EXECUTABLE))
    input()
    sys.exit(1)

try:
    from pytube import YouTube
except ImportError:
    print('pytube is not installed.')
    print('\t"{0}" -m pip install pytube'.format(PYTHON_EXECUTABLE))
    input()
    sys.exit(1)

# Get Keys
with open('settings.json') as data_file:
    settings = json.load(data_file)

# Create Spotify object
print('Setting up Spotify object...')
client_credentials_manager = SpotifyClientCredentials(client_id=settings['spotify']['client_id'],
                                                      client_secret=settings['spotify']['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False


def chunks(l, n):
    
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def stripString(text):
    return "".join([i for i in text if i not in [i for i in '/\\:*?"><|']])


def downloadYoutubeToMP3(link):
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download()
        return True
    except Exception as e:
        print(repr(e))
        return False


song_data = {}  # song_data[uri] = {'artist':x, 'album':x, 'title':x, 'album_art':x, 'track':x}
individual_songs = []

url = input("Enter url: ")

start_time = time.time()

username = settings['spotify_username']
from urllib.parse import urlparse, parse_qs

# Parse the URL
parsed_url = urlparse(url)

# Extract the playlist ID from the path
path_segments = parsed_url.path.split('/')
if len(path_segments) >= 3 and path_segments[1] == "playlist":
    playlist_id = path_segments[2]
    print("Playlist ID:", playlist_id)
else:
    print("Invalid URL format: ", url)
    # Handle the error or exit the program as needed

offset = 0
results = sp.user_playlist_tracks(username, playlist_id, offset=offset)
individual_songs += results['items']
while results['next'] is not None:
    offset += 100
    results = sp.user_playlist_tracks(username, playlist_id, offset=offset)
    individual_songs += results['items']

for song in individual_songs:
    song = song['track']
    song_data[song['uri']] = {'artist': song['artists'][0]['name'],
                              'album': song['album']['name'],
                              'title': song['name'],
                              'album_art': song['album']['images'][0]['url'],
                              'track': str(song['track_number'])}

for song in song_data:
    try:
        print("")
        search_term = song_data[song]['artist'] + " " + song_data[song]['title'] + " lyrics"
        videos_search = VideosSearch(search_term, limit=1)
        results = videos_search.result()

        if len(results['result']) == 0:
            print("No search results found on YouTube for the given query.")
            continue

        video_URL = results['result'][0]['link']

        print("Video link =", video_URL)

        # Use pytube to download audio
        yt = YouTube(video_URL)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_stream.download(output_path=os.path.join(os.getcwd(), 'music')) # Download audio in the current working directory
        
        # Rename the downloaded file to match the song details
        audio_file = os.path.join(os.getcwd(), yt.title + '.mp4')
        new_audio_file = os.path.join(os.getcwd(), f"{song_data[song]['artist']} - {song_data[song]['title']}.mp4")
        
        if os.path.exists(audio_file):  # Check if the original file exists
            os.rename(audio_file, new_audio_file)  # Rename the file

        print("Downloaded:", song_data[song]['artist'], "-", song_data[song]['title'])  # Display download message

    except Exception as e:
        print("An error occurred:", e)
        continue
        time.sleep(1)
        # Add a small delay to allow the renaming process to complete
          # You can adjust the sleep time if needed
        files_in_cd = os.listdir(os.getcwd())
        for i in files_in_cd:
            if i.endswith(".mp4"):
                file = os.getcwd() + "\\" + i
        try:
            print("Tagging \\" + file.split("\\")[-1])
        except:
            print("Tagging (Special characters in name)")

        audio = MP3(file, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass
        urllib.request.urlretrieve(song_data[song]['album_art'], (os.getcwd() + "/TempAArtImage.jpg"))
        audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'cover',
                            data=open(os.getcwd() + "/TempAArtImage.jpg", 'rb').read()))
        audio.save()
        os.remove(os.getcwd() + "/TempAArtImage.jpg")
        audio = EasyID3(file)
        audio["tracknumber"] = song_data[song]['track']
        audio["title"] = song_data[song]['title']
        audio["album"] = song_data[song]['album']
        audio["artist"] = song_data[song]['artist']
        audio.save()

        if not os.path.exists(os.getcwd() + "/output/"):
            os.makedirs(os.getcwd() + "/output/")
        title = stripString(song_data[song]['title'])
        artist = stripString(song_data[song]['artist'])
        album = stripString(song_data[song]['album'])

        try:
            os.rename(file, (os.getcwd() + "/output/" + stripString(artist + " - " + title + ".mp3")))
            print("Saved at: " + os.getcwd() + "/output/" + stripString(artist + " - " + title + ".mp3"))
        except Exception as e:
            print("Could not rename")
            print(repr(e))
            for i in range(10):
                try:
                    print("Attempting: " + os.getcwd() + "/output/" + stripString(
                        artist + " - " + title + "(" + str(i + 1) + ").mp3"))
                    os.rename(file,
                              os.getcwd() + "/output/" + stripString(
                                  artist + " - " + title + "(" + str(i + 1) + ").mp3"))
                    print(
                        "Saved at: " + os.getcwd() + "/output/" + stripString(
                            artist + " - " + title + "(" + str(i + 1) + ").mp3"))
                    break
                except Exception as ex:
                    print("Rename Error on " + i + ": " + str(repr(ex)))
            else:
                print("Could not rename (2nd layer)")
                os._exit(5)
        except Exception as e:
            print("Some error happened somewhere????")
            print(e)
            a = input("Ack")

a = input("Complete ghovv")

