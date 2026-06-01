import json
import socket
import asyncio
from datetime import datetime
import os
from getmac import get_mac_address

#TARGET = "127.0.0.1" #IPv4 loopback
#TARGET = "192.168.1.67"
#TARGET = "192.168.1.1"
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

async def scan_port(port, TARGET):
    async with semaphore:
        service = COMMON_PORTS.get(port, "Unknown")
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(TARGET, port),
                timeout=1
            )

            #print(f"Port {port} is OPEN")

            banner = await grab_banner(reader, writer, port)

            open_ports.append({
                "port": port,
                "protocol": service,
                "banner": banner
            })

            writer.close()
            await writer.wait_closed()
        #port is closed
        except:
            #print(f"Port {port} is CLOSED")
            pass

async def port_scan(ports, TARGET):
    print("-------------------------------------")
    print(f"SCANNING PORTS for {TARGET}:")
    tasks = [scan_port(port, TARGET) for port in ports]
    await asyncio.gather(*tasks)


def save_to_json(scan_data, TARGET):

    # make sure directory exists
    os.makedirs("output", exist_ok=True)

    # set file name based on target ip
    filename = f"output/scan_{TARGET.replace(".", "-")}.json"

    try:
        #write to file
        with open(filename, "w") as f:
            json.dump(scan_data, f, indent=4)
        print(f"\nResults saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def find_mac_address(TARGET):
    return get_mac_address(ip=TARGET)

def main(TARGET, option):

    if option == 1:
        asyncio.run(port_scan(COMMON_PORTS, TARGET))
    elif option == 2:
        asyncio.run(port_scan(range(1, 65536), TARGET))
    elif option == 3:
        print(f"MAC Address of Target {TARGET} is: {find_mac_address(TARGET)}")
    

    # done scanning
    scan_data = {
    "target": TARGET,
    "timestamp": datetime.now().isoformat(),
    "results": open_ports
    }

    # #print results
    # print("SCANNING DONE")
    # print("-------------------------------------")
    # print("ALL OPEN PORTS:")
    # for port in open_ports:
    #     print(f"Port Number:{port["port"]}, Protocol: {port["protocol"]}, Banner: {port["banner"]}")
    
    #save results to output file
    print("Writing results to scan_results.json")
    save_to_json(scan_data, TARGET)