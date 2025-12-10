import socket
import ssl

def tls_client():
    host = '0.0.0.0'
    port = 8443
    
    try:
        print(f"Attempting to connect to TLS server at {host}:{port}")
        
        # Create TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Create SSL context
        context = ssl.create_default_context()
        
        # For self-signed certificates, we need to disable verification
        # In production, you would use proper certificate validation
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        print("Wrapping socket with TLS...")
        
        # Wrap socket with TLS
        secure_socket = context.wrap_socket(client_socket, server_hostname=host)
        
        # Connect to server
        secure_socket.connect((host, port))
        print(f"TLS connection established with {host}:{port}")
        print("All communication is now encrypted!")
        
        while True:
            # Get user input
            number = input("\nEnter a number to check (or 'quit' to exit): ")
            
            if number.lower() == 'quit':
                break
            
            try:
                # Send encrypted data
                secure_socket.sendall(number.encode())
                print(f"Sent encrypted data: {number}")
                
                # Receive encrypted response
                response = secure_socket.recv(1024)
                print(f"Server response: {response.decode()}")
                
            except ssl.SSLError as e:
                print(f"SSL Error: {e}")
                break
            except BrokenPipeError:
                print("Connection broken by server")
                break
                
    except ConnectionRefusedError:
        print("Connection refused - make sure the TLS server is running")
    except ssl.SSLError as e:
        print(f"SSL Handshake failed: {e}")
    except KeyboardInterrupt:
        print("\nClient shutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'secure_socket' in locals():
            secure_socket.close()
            print("\nTLS connection closed")

if __name__ == "__main__":
    tls_client()