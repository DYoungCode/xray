import argparse
import socket
import sys
import concurrent.futures
from datetime import datetime

def get_arguments():
    parser = argparse.ArgumentParser(description="XRAY is a Python Multi-Threaded Port Scanner")

    # Target arguement (Required)
    parser.add_argument("-t", "--target", dest="target", help="Target IP / Domain", required=True)

    # Ports argument (Optional - Default to Well-known ports (1-1024)
    parser.add_argument("-p", "--ports", dest="ports", help="Port range to scan (e.g. 1-100)", default="1-1024")

    options = parser.parse_args()
    return options

def scan_port(port):
    try:
        # Scan ports 1 to 1024 (well-known ports)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:
            #print(f"Port {port} is OPEN")
            
            # lets try to grab banner
            try:
                banner = s.recv(1024).decode().strip()
                print(f"Port {port} OPEN. Banner received: {banner}")
            except:
                print(f"Port {port} OPEN")

        s.close()
    except:
        pass # if thread fails, let operation die silently


if __name__ == "__main__":

    # First get arguments from the user
    options = get_arguments()

    # resolve the target
    try:
        target = socket.gethostbyname(options.target)
    except socket.gaierror:
        print("[-] Hostname couldn't be resolved.")
        sys.exit()

    #Parse the port range string "1-100" into 2 integers
    start_port, end_port = options.ports.split("-")
    start_port = int(start_port)
    end_port = int(end_port)

    print("*" * 50)
    print(f"Scanning Target: {target}")
    print(f"Time started: {str(datetime.now())}")
    print("*" * 50)

    try:

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:

            executor.map(scan_port, range(start_port, end_port + 1))
        
    except KeyboardInterrupt:
        print("\n Exiting program.")
    except socket.error:
        print("Couldn't connect to target.")

    print(f"\nScanning completed at: {str(datetime.now())}")


    

