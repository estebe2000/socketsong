from mpyg321 import MPyg321Player
from time import sleep

player = MPyg321Player()       # instanciate the player
player.play_song("sample.mp3") # play a song
sleep(5)
player.pause()                 # pause playing
sleep(3)
player.resume()                # resume playing
sleep(5)
player.stop()                  # stop playing
player.quit()                  # quit the player
