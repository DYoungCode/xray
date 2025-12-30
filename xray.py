import argparse
import socket
import sys
import threading
import concurrent.futures
from datetime import datetime
from colorama import init, Fore

import json

# true resets color back to white after every print 
init(autoreset=True)

def get_arguments():
    parser = argparse.ArgumentParser(description="XRAY is a Python Multi-Threaded Port Scanner")

    # Target arguement (Required)
    parser.add_argument("-t", "--target", dest="target", help="Target IP / Domain", required=True)

    # Ports argument (Optional - Default to Well-known ports (1-1024)
    parser.add_argument("-p", "--ports", dest="ports", help="Port range to scan (e.g. 1-100)", default="1-1024")

    # Ability to output results to a JSON file
    parser.add_argument("-o", "--output", dest="output", help="Save results to a JSON file (optional)")

    options = parser.parse_args()
    return options

# Create a results list, 
results = []
results_lock = threading.Lock()

def scan_port(port):
    try:
        # Scan ports 1 to 1024 (well-known ports)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:            
            # lets try to grab banner
            try:
                banner = s.recv(1024).decode().strip()
                print(Fore.GREEN + f"Port {port} OPEN. Banner received: {banner}")
            except:
                print(Fore.GREEN + f"Port {port} OPEN")

            # Save to our list in safe manner
            with results_lock:
                results.append({
                    "port": port,
                    "banner": banner,
                    "status": "open"
                })

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
        print(Fore.RED + f"[-] Hostname couldn't be resolved.")
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
        print(Fore.RED + "Couldn't connect to target.")

    if options.output:
        try:
            with open(options.output, "w") as f:
                json.dump(results, f, indent=4)
            print(f"\n[+] Results saved to {options.output}")
        except IOError:
            print(Fore.RED + "\n[-] Could not write to file.")

    print(f"\nScanning completed at: {str(datetime.now())}")


    

