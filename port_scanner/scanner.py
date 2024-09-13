import sys
import socket

IP = sys.argv[1] 
ports = []

def port_scanning(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(3)
    try:
        sock.connect((IP, port))
        return True
    except:
        return False
    finally:
        sock.close()

def banner_grabbing(open_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(3)
    try:
        sock.connect((IP,open_port))
        banner = sock.recv(1024).decode('utf-8').strip()
        sock.close()
        if banner:
            return banner
        else:
            return 'No banner recived'
    except:
        return 'Error! could not recieve banner'
    finally:
        sock.close()


print(f'starting scan on {IP}:')
for port in range(65535):
    if port_scanning(port):
        print(f'[OPEN] port {port} found open')
        ports.append(port)

if length(ports) == 0:
    print("Host seems to be down!")
else:
    print('Attempting to detect service versions:')
    for open_port in ports:
        banner = banner_grabbing(open_port)
        print(f'[BANNER] {banner}')
    

