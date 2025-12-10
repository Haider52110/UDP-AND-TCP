import socket

def is_even(number):
    """Check if a number is even"""
    try:
        return int(number) % 2 == 0
    except ValueError:
        return "Invalid input - please send a number"

def tcp_server():
    host = '127.0.0.1'  # localhost
    port = 12346
    
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind and listen
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"TCP Server listening on {host}:{port}")
        print("Waiting for connections...")
        
        while True:
            # Accept client connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            
            try:
                with client_socket:
                    while True:
                        # Receive data from client
                        data = client_socket.recv(1024)
                        if not data:
                            break
                            
                        number = data.decode()
                        print(f"Received from {client_address}: {number}")
                        
                        # Process the number
                        result = is_even(number)
                        response = f"The number {number} is {'even' if result == True else 'odd' if result == False else result}"
                        
                        # Send response back to client
                        client_socket.send(response.encode())
                        print(f"Sent response: {response}")
                        
            except ConnectionResetError:
                print(f"Client {client_address} disconnected unexpectedly")
            except Exception as e:
                print(f"Error with client {client_address}: {e}")
                
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    tcp_server()
