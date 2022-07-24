from re import A
from mpyg321.mpyg321 import MPyg321Player
from time import sleep
import os
import glob

playlist = []
boucle = True
actualsong = 0
play = True

class MyPlayer(MPyg321Player):
    """We create a class extending the basic player to implement callbacks"""

    def on_any_stop(self):
        """Callback when the music stops for any reason"""
        print("The music has stopped")

    def on_user_pause(self):
        """Callback when user pauses the music"""
        print("The music has paused")

    def on_user_resume(self):
        """Callback when user resumes the music"""
        print("The music has resumed")

    def on_user_stop(self):
        """Callback when user stops music"""
        print("The music has stopped (by user)")

    def on_music_end(self):
        """Callback when music ends"""
        print("The music has ended")
        nextsong()

    def on_user_mute(self):
        """Callback when music is muted"""
        print("The music has been muted (continues playing)")

    def on_user_unmute(self):
        """Callback when music is unmuted"""
        print("Music has been unmuted")

def create_playlist(path):
    for song in glob.glob(path):
        print("Adding...",song)
        playlist.append(song)

def menu():
    print("0 : Liste")
    print("1 : choose number ")
    print("2 : pause/resume")
    print("3 : next")
    print("4 : previous")
    print("5 : stop/play")
    print("6 : exit")
    choose = input()
    return choose

def listsong():
    nb = 0
    for i in playlist:
        print (nb,"   :",i)
        nb +=1
    
def choosesong ():
    listsong()
    a= input("votre choix de morceau :")
    actualsong = int(a) 
    player.play_song(playlist[actualsong]) # play a song

def nextsong():
    global actualsong
    if actualsong+1 < len(playlist):
        actualsong += 1
    else :
        actualsong = 0
    player.play_song(playlist[actualsong]) # play a song

def prevsong():
    global actualsong
    if actualsong-1 < 0:
        actualsong = len(playlist)-1
    else :
        actualsong += -1
    player.play_song(playlist[actualsong]) # play a song

def playpause():
    global play
    if not play :
        player.resume()                # resume playing
        play = True
    else :
        player.pause()                 # pause playing
        play = False

def stopplay():
    global play
    if not play :
        player.play_song(playlist[actualsong]) # play a song
        play = True
    else :
        player.stop()                 # pause playing
        play = False

create_playlist("*.mp3")

player = MyPlayer()
player.play_song(playlist[actualsong]) # play a song

while boucle:
    choix = int(menu())
    print(choix)
    if choix == 0 :
        listsong()
    elif choix == 1 :
        choosesong()
    elif choix == 2 :
        playpause()
    elif choix == 3:
        nextsong()
    elif choix == 4:
        prevsong()
    elif choix == 5 :
        stopplay()
    elif choix == 6 :
        player.quit()                  # quit the player
        boucle = False
    

