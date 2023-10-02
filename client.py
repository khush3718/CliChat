import _thread
import socket

username = input('Enter your username: ') # Get the client's username

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket object
client.connect(('127.0.0.1', 65432)) # Connect to the server

def receive():
    while True: # Infinite loop
        try: # Try to
            message = client.recv(1024).decode('ascii') # Receive a message from the server
            if message == 'USERNAME': # If the message is a request for a username
                client.send(username.encode('ascii')) # Send the client's username to the server
            else: # Else
                print(message) # Print the message
        except: # If there is an error
            print('An error occured!') # Print an error message and break out of the loop
            client.close() # Close the client's connection
            break # Break out of the loop


def write():
    while True: # Infinite loop
        message = f'{username}: {input("")}' # Get the client's message
        client.send(message.encode('ascii')) # Send the message to the server


_thread.start_new_thread(receive, ()) # Start a new thread to handle receiving messages
_thread.start_new_thread(write, ()) # Start a new thread to handle writing messages