import socket

target = "127.0.0.1"

# AF_INET = IPv4 (vs IPv6 (AF_INET6))
# SOCK_STREAM = TCP (vs_UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 80

# wait 1 second. If fw blocks packets, we'll wait forever
s.settimeout(1)

# Attempt conn, connect_ex doesn't crash if conn fails, just returns status
result = s.connect_ex((target, port))

if result == 0:
    print(f"Port {port} is OPEN")
else:
    print(f"Port {port} is CLOSED")

    

