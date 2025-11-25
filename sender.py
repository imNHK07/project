import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python sender.py <barcode>")
        sys.exit(1)

    barcode = sys.argv[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 9999))
        print(f"Sending barcode: {barcode}")
        s.sendall(barcode.encode('utf-8'))
        
        response = s.recv(1024)
        print(f"Response from listener: {response.decode('utf-8')}")
    except ConnectionRefusedError:
        print("Connection refused. Is the listener running?")
    finally:
        s.close()

if __name__ == '__main__':
    main()
