import socket
import sys
import concurrent.futures
from datetime import datetime

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of arguments.")
    print("Syntax: python xray.py <ip>")
    sys.exit() 

def scan_port(port):
    try:
        # Scan ports 1 to 1024 (well-known ports)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is OPEN")
        
        s.close()
    except:
        pass # if thread fails, let operation die silently


if __name__ == "__main__":

    print("*" * 50)
    print(f"Scanning Target: {target}")
    print(f"Time started: {str(datetime.now())}")
    print("*" * 50)

    try:

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:

            executor.map(scan_port, range(1, 1025))
        
    except KeyboardInterrupt:
        print("\n Exiting program.")

    except socket.gaierror:
        print("Hostname couldn't be resolved.")

    except socket.error:
        print("Couldn't connect to target.")

    print(f"\nScanning completed at: {str(datetime.now())}")


    

