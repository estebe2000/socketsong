from email.errors import NoBoundaryInMultipartDefect
from re import A
from mpyg321.mpyg321 import MPyg321Player
from time import sleep
import os
import glob
import socket, threading



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
    print("0 : Liste \n1 : choose number \n2 : pause/resume \n3 : next \n4 : previous \n5 : stop/play \n6 : exit")
    choose = input()
    return choose

def menu_s():
    return "0 : Liste \n1 : choose number \n2 : pause/resume \n3 : next \n4 : previous \n5 : stop/play \n6 : menu"

def listsong():
    nb = 0
    litfull = "Liste des musique disponible: \n"
    for i in playlist:
        x = i.split("/")
        y = len(x)
        litfull = litfull +"\n"+str(nb)+":--> "+ x[y-1] 
        nb +=1
    print(nb)
    return litfull
    
def choosesong (nbsong):
    listsong()
    a= nbsong
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

# Global variable that mantain client's connections
connections = []
playlist = []
boucle = True
actualsong = 0
play = False
player = MyPlayer()

def player_s (cmd):
    global boucle,actualsong,play
    
    
    #player.play_song(playlist[actualsong]) # play a song
    choix_s = cmd.split()
    choix = int(choix_s[0])
    print(choix)
    if choix == 0 :
        return listsong()
    elif choix == 1 :
        choosesong(int(choix_s[1]))
    elif choix == 2 :
        playpause()
        return ("play/pause")
    elif choix == 3:
        nextsong()
        return("next song")
    elif choix == 4:
        prevsong()
        return ("previous song")
    elif choix == 5 :
        stopplay()
        return("play/stop")
    elif choix == 6 :
        return menu_s()
        #player.quit()                  # quit the player
            

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    while True:
        try:
            # Get client message
            msg = connection.recv(1024)

            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                
                # Log message sent by user
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                
                # Build message format and broadcast to users connected on server
                #msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                msg_to_send = str(player_s(msg.decode()))
                broadcast(msg_to_send, connection)


            # Close connection if no message was sent
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break


def broadcast(message: str, connection: socket.socket) -> None:
    '''
        Broadcast message to all users connected to the server
    '''

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn == connection:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)
        

        if client_conn != connection:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    '''
        Remove specified connection from connections list
    '''

    # Check if connection exists on connections list
    if conn in connections:
        # Close socket connection and remove connection from connections list
        conn.close()
        connections.remove(conn)


def server() -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''

    LISTENING_PORT = 12000
    create_playlist("/home/estebe2000/project/*.mp3")

    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        
        while True:

            # Accept client connection
            socket_connection, address = socket_instance.accept()
            # Add client connection to connections list
            connections.append(socket_connection)
            socket_connection.send(menu_s().encode())
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()



def start():
    global boucle,actualsong,play
    create_playlist("*.mp3")

    
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
    

if __name__ == "__main__":
    #start()
    server()
