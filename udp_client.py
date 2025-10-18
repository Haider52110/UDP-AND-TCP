import socket

def udp_client():
    host = '127.0.0.1'  # server IP
    port = 12345
    
    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            # Get user input
            number = input("Enter a number to check (or 'quit' to exit): ")
            
            if number.lower() == 'quit':
                break
            
            # Send data to server
            client_socket.sendto(number.encode(), (host, port))
            
            # Receive response from server
            response, server_address = client_socket.recvfrom(1024)
            print(f"Server response: {response.decode()}")
            
    except KeyboardInterrupt:
        print("\nClient shutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Socket closed")

if __name__ == "__main__":
    udp_client()
