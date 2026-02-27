import socket
import threading
from concurrent.futures import ThreadPoolExecutor

PORTS={
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}

#TARGET = "127.0.0.1" #IPv4 loopback
TARGET = "192.168.1.67"
open_ports = []
lock = threading.Lock()

def grab_banner(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((TARGET, port))

            # Try passive grab first
            try:
                banner = s.recv(1024)
                if banner:
                    return banner.decode(errors="ignore").strip()
            except:
                pass

            # Try active HTTP probe
            if port == 80:
                http_request = b"GET / HTTP/1.1\r\nHost: %b\r\n\r\n" % TARGET.encode()
                s.send(http_request)
                response = s.recv(1024)
                return response.decode(errors="ignore").strip()

    except:
        return None

    return None

def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            status = s.connect_ex((TARGET, port))

            if status == 0:
                print(f"{PORTS[port]} is OPEN on port {port}")
                banner = grab_banner(port)
                if banner:
                    print(f"  Banner: {banner[:100]}")
                with lock:
                    open_ports.append(port)
            else:
                print()
                #print(f"{PORTS[port]} is CLOSED on port {port}")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def main():
    # multithreading
    try:
        num_threads = 8#int(input("How many threads:"))
        print("Scanning ports...")
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(scan_port, PORTS.keys())

        print("Scanning done.")
        print("-------------------------------------")
        print("All open ports:")
        for port in open_ports:
            print(f"{port}: {PORTS[port]}")

    except ValueError:
        print("Invalid int")

        
    
if __name__ == "__main__":
    main()