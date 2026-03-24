import json
import socket
import asyncio
from datetime import datetime
import os

TARGET = "127.0.0.1" #IPv4 loopback
TARGET = "192.168.1.67"

# list of known ports
COMMON_PORTS={
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

open_ports = []
semaphore = asyncio.Semaphore(500)

async def grab_banner(reader, writer, port):
    try:
        try:
            data = await asyncio.wait_for(reader.read(1024), timeout=1)
            if data:
                banner = data.decode(errors="ignore").strip()
                return banner
        except:
            pass
 
    except:
        return None
    return None

async def scan_port(port):
    async with semaphore:
        service = COMMON_PORTS.get(port, "Unknown")
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, port),
                timeout=1
            )

            print(f"Port {port} is OPEN")

            banner = await grab_banner(reader, writer, port)

            open_ports.append({
                "port": port,
                "protocol": service,
                "banner": banner
            })

            writer.close()
            await writer.wait_closed()
        except:
            print(f"Port {port} is CLOSED")

async def port_scan(ports):
    print("Scanning ports:")
    tasks = [scan_port(port) for port in ports]
    await asyncio.gather(*tasks)


def save_to_json(scan_data):
    os.makedirs("output", exist_ok=True)
    filename = f"output/scan_{TARGET.replace(".", "-")}.json"
    try:
        with open(filename, "w") as f:
            json.dump(scan_data, f, indent=4)
        print(f"\nResults saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():

    #get ip address
    

    #get scan option
    while True:
        option = input(
            "\nSelect scan type:\n"
            "1. Common ports\n"
            "2. Full scan (1–65535)\n"
            "Enter option: "
        )

        if option == "1":
            asyncio.run(port_scan(COMMON_PORTS))
            break
        elif option == "2":
            asyncio.run(port_scan(range(1, 65536)))
            break
        else:
            print("Invalid option. Please enter 1 or 2.")
    
    # done scanning
    scan_data = {
    "target": TARGET,
    "timestamp": datetime.now().isoformat(),
    "results": open_ports
    }

    #print results
    print("Scanning done.")
    print("-------------------------------------")
    print("All Open Ports:")
    for port in open_ports:
        print(f"Port Number:{port["port"]}, Protocol: {port["protocol"]}, Banner: {port["banner"]}")
    
    #save to output file
    print("Writing results to scan_results.json")
    save_to_json(scan_data)
    
if __name__ == "__main__":
    main()