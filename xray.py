import socket
from datetime import datetime

target = "127.0.0.1"

print("*" * 50)
print(f"Scanning Target: {target}")
print(f"Time started: {str(datetime.now())}")
print("*" * 50)

try:
    # Scan ports 1 to 1024 (well-known ports)
    for port in range(1, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is OPEN")
        
        s.close()

except KeyboardInterrupt:
    print("\n Exiting program.")

except socket.gaierror:
    print("Hostname couldn't be resolved.")

except socket.error:
    print("Couldn't connect to target.")


    

