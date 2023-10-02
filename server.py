import _thread
import socket

host = '127.0.0.1' # Standard loopback interface address (localhost)
port = 65432 # Port to listen on (non-privileged ports are > 1023)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket object
server.bind((host, port)) # Bind the socket to the port

server.listen(2) # Listen for incoming connections

clients = [] # List of clients. We will append clients to this list as they connect
usernames = [] # List of usernames. We will append usernames to this list as they connect

# Function to broadcast messages to all clients

def broadcast(message):
    for client in clients: # Iterate through all clients
        client.send(message) # Send the message to the client

# Function to handle client connections

def handle_client(client):
    while True: # Infinite loop
        try: # Try to
            message = client.recv(1024) # Receive a message from the client
            broadcast(message) # Broadcast the message to all clients
        except: # If there is an error
            index = clients.index(client) # Get the index of the client
            clients.remove(client) # Remove the client from the list of clients
            client.close() # Close the client's connection
            username = usernames[index] # Get the username of the client
            broadcast(f'{username} has left the chat room!'.encode('ascii')) # Broadcast that the client has left the chat room
            usernames.remove(username) # Remove the client's username from the list of usernames
            break # Break out of the loop


# Function to receive / handle client connections

def receive():
    while True: # Infinite loop
        client, address = server.accept() # Accept a client connection
        print(f'Connected with {str(address)}') # Print the address of the client

        client.send('USERNAME'.encode('ascii')) # Send the client a request for a username
        username = client.recv(1024).decode('ascii') # Receive the username from the client
        usernames.append(username) # Append the username to the list of usernames
        clients.append(client) # Append the client to the list of clients

        print(f'Username of the client is {username}!') # Print the username of the client
        broadcast(f'{username} has joined the chat room!'.encode('ascii')) # Broadcast that the client has joined the chat room
        client.send('Connected to the server!'.encode('ascii')) # Send the client a connection confirmation message

        _thread.start_new_thread(handle_client, (client, )) # Start a new thread to handle the client


print('Server is listening...') # Print that the server is listening
receive() # Call the receive function