import socket

def is_even(number):
    """Check if a number is even"""
    try:
        return int(number) % 2 == 0
    except ValueError:
        return "Invalid input - please send a number"

def udp_server():
    host = '127.0.0.1'  # localhost
    port = 12345
    
    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Bind socket to address and port
        server_socket.bind((host, port))
        print(f"UDP Server listening on {host}:{port}")
        print("Waiting for numbers to check if even/odd...")
        
        while True:
            # Receive data from client
            data, client_address = server_socket.recvfrom(1024)
            number = data.decode()
            
            print(f"Received from {client_address}: {number}")
            
            # Process the number
            result = is_even(number)
            response = f"The number {number} is {'even' if result == True else 'odd' if result == False else result}"
            
            # Send response back to client
            server_socket.sendto(response.encode(), client_address)
            print(f"Sent response: {response}")
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        print("Socket closed")

if __name__ == "__main__":
    udp_server()
