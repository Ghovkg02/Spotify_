# Spotify_

Download Spotify playlists to mp3 files from desktop.
Uses YouTube as an audio source by looking for videos under the same name and downloading as mp3.

Note : Works with desktop spotify links and playlists only.

# Requirements 
Python (tested with 3.10)

ffmpeg (Download from http://ffmpeg.zeranoe.com/builds/)

# Installation
1. Clone/Download this repo `git clone (https://github.com/Ghovkg02/Spotify_.git)`
2. Install the required modules. `pip install required.txt`
3. Go to [https://developer.spotify.com/my-applications](https://developer.spotify.com/my-applications) and create an app to get a client_id and client_secret key pair
4. Put these keys in `settings.json`
5. Put your [Spotify username](https://www.spotify.com/us/account/overview/) in `settings.json`
   Check in the edit profile section.
6. Go to [http://ffmpeg.zeranoe.com/builds/](http://ffmpeg.zeranoe.com/builds/) and download ffmpeg.
7. Extract the files from the zip and look for ffmpeg.exe, ffplay.exe and ffprobe.exe from the folder,
   you can search it too, and copy it to the location of Spotify.py

# Steps to Use

Go to the Spotify website
1. Get the URL of a Spotify playlist by clicking the three dots at the top to show then menu and click share.
2. In this sub-menu, click "Copy Spotify URL"; this will copy the URL to your clipboard.
3. Run Spotify.py and insert your Spotify URL, then hit enter.
4. Files will be saved to /music/ in the current working directory.

