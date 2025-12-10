import socket
import ssl

def is_even(number):
    """Check if a number is even"""
    try:
        return int(number) % 2 == 0
    except ValueError:
        return "Invalid input - please send a number"

def tls_server():
    host = '0.0.0.0'
    port = 8443  # Standard HTTPS port for TLS
    
    try:
        # Create TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind socket
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"TLS Server listening on {host}:{port}")
        print("Generating SSL context...")
        
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="certificates/server.crt", 
                              keyfile="certificates/server.key")
        
        print("SSL context created. Waiting for TLS connections...")
        
        while True:
            try:
                # Accept TCP connection
                client_socket, client_address = server_socket.accept()
                print(f"\nTCP connection from {client_address}")
                
                # Wrap with TLS
                secure_socket = context.wrap_socket(client_socket, server_side=True)
                print(f"TLS handshake complete with {client_address}")
                
                with secure_socket:
                    while True:
                        # Receive encrypted data
                        data = secure_socket.recv(1024)
                        if not data:
                            print(f"Client {client_address} disconnected")
                            break
                            
                        number = data.decode()
                        print(f"Received encrypted data from {client_address}: {number}")
                        
                        # Process the number
                        result = is_even(number)
                        response = f"The number {number} is {'even' if result == True else 'odd' if result == False else result}"
                        
                        # Send encrypted response
                        secure_socket.sendall(response.encode())
                        print(f"Sent encrypted response: {response}")
                        
            except ssl.SSLError as e:
                print(f"SSL Error with client {client_address}: {e}")
                if 'client_socket' in locals():
                    client_socket.close()
            except ConnectionResetError:
                print(f"Client {client_address} disconnected unexpectedly")
            except Exception as e:
                print(f"Error with client {client_address}: {e}")
                
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        if 'server_socket' in locals():
            server_socket.close()
            print("Server socket closed")

if __name__ == "__main__":
    tls_server()