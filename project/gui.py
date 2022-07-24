from http import client
import socket, threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
#from kivy.uix.textinput import TextInput

SERVER_ADDRESS = '192.168.1.46'
SERVER_PORT = 12000

class MainApp(App):
    socket_instance = socket.socket()
    socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
    def build(self):
        
        print('Connected to chat!')
        layout = BoxLayout(padding=10)
        btn1 = Button(text ="Push Me !",
            background_normal = './images/play.png',
            background_down = './images/play1.png',
            size_hint = (.3, .3),
            pos_hint = {"x":0.35, "y":0.3}
        )
        btn1.bind(on_press=self.on_press_button)
        btn2 = Button(text ="Push Me !",
            background_normal = './media/play.png',
            background_down = './media/pause.png',
            size_hint = (.3, .3),
            pos_hint = {"x":0.35, "y":0.3}
        )
        layout.add_widget(btn1)
        layout.add_widget(btn2)


        return layout

    def on_press_button(self, instance):
        self.client("5")
        print('You pressed the button!')

    def handle_messages(connection: socket.socket):
        '''
            Receive messages sent by the server and display them to user
        '''

        while True:
            try:
                msg = connection.recv(1024)

                # If there is no message, there is a chance that connection has closed
                # so the connection will be closed and an error will be displayed.
                # If not, it will try to decode message in order to show to user.
                if msg:
                    print(msg.decode())
                else:
                    connection.close()
                    break

            except Exception as e:
                print(f'Error handling message from server: {e}')
                connection.close()
                break

    def client(self, msg) -> None:
        '''
            Main process that start client connection to the server 
            and handle it's input messages
        '''

        
        
        try:
            
            # Read user's input until it quit from chat and close connection
            #while True:
            #msg = input()

            #if msg == 'quit':
            #    break

            # Parse message to utf-8
            self.socket_instance.send(msg.encode())

            # Close connection with the server
            #self.socket_instance.close()

        except Exception as e:
            print(f'Error connecting to server socket {e}')
            self.socket_instance.close()


if __name__ == "__main__":
    #client()
    app = MainApp()
    app.run()