import socket
import requests

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 9999))
    s.listen(1)
    print("Listener started on port 9999")
    while True:
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        data = conn.recv(1024)
        if not data:
            conn.close()
            continue
        barcode = data.decode('utf-8').strip()
        print(f"Received barcode: {barcode}")

        # Send barcode to web service
        try:
            response = requests.post('http://web:8000/auto_scan/', json={'barcode': barcode})
            if response.status_code == 200:
                print(f"Sent to web service, status: {response.status_code}")
                conn.sendall(b"Message received and sent to web service.")
            else:
                print(f"Error from web service. Status code: {response.status_code}")
                try:
                    error_data = response.json()
                    print("Detailed error from Django:")
                    print(error_data)
                except ValueError:
                    print("Could not parse JSON response. Raw response text:")
                    print(response.text)
                conn.sendall(b"Error processing barcode.")
        except requests.exceptions.RequestException as e:
            print(f"Error sending to web service: {e}")
            conn.sendall(b"Error sending message to web service.")
        
        conn.close()

if __name__ == '__main__':
    main()