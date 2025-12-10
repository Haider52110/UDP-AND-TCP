import socket

def tcp_client():
    host = '127.0.0.1'  # server IP
    port = 12346
    
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        client_socket.connect((host, port))
        print(f"Connected to server {host}:{port}")
        
        while True:
            # Get user input
            number = input("Enter a number to check (or 'quit' to exit): ")
            
            if number.lower() == 'quit':
                break
            
            # Send data to server
            client_socket.send(number.encode())
            
            # Receive response from server
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode()}")
            
    except KeyboardInterrupt:
        print("\nClient shutting down...")
    except ConnectionRefusedError:
        print("Connection refused - make sure the server is running")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    tcp_client()
