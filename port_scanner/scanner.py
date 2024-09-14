'''
script by: Chanan Shnker
This is a little project ive been working on. 
This script is a port scanner that checks what ports are open and then attempt to do banner grabbing/ service detection.
Obviously Nmap exists and does this job much faster and with more features, but this is part of my python learning journey.
'''

import sys
import socket
import ipaddress

IP = sys.argv[1]  # taking an IP address as a command-line argument
ports = []  # array to store all open ports found

# Function to validate if the provided IP address is valid
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)  # checks if IP is valid
        return True
    except:
        return False

# Function to scan a specific port
def port_scanning(port):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(3)  # Set a timeout of 3 seconds for each connection attempt
    try:
        # Try to connect to the IP address on the given port
        sock.connect((IP, port))
        return True  # If connection is successful, the port is open
    except:
        return False  # If the connection fails, the port is closed
    finally:
        sock.close()  # Ensure the socket is closed after the attempt

# Function to perform banner grabbing on an open port
def banner_grabbing(open_port):
    # Create a socket object for the banner grabbing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(3)  # Set a timeout of 3 seconds
    try:
        # Try to connect to the IP on the specific open port
        sock.connect((IP, open_port))
        # Receive up to 1024 bytes from the connection and decode to UTF-8
        banner = sock.recv(1024).decode('utf-8').strip()
        sock.close()
        if banner:
            return banner  # Return the banner if received
        else:
            return 'No banner received'
    except:
        return 'Error! Could not receive banner'
    finally:
        sock.close()  # Ensure the socket is closed after the attempt

# Validate the provided IP address
if validate_ip(IP):
    print(f'Starting scan on {IP}:')
    # Scan all ports from 0 to 65535
    for port in range(65535):
        if port_scanning(port):
            print(f'[OPEN] Port {port} found open')  # Print open ports
            ports.append(port)  # Append open ports to the list
else:
    print(f'The IP address {IP} is not valid!')
    sys.exit()  # Exit the program if the IP is invalid

# Check if any ports were found open
if len(ports) == 0:
    print("No ports seem to be found open on the host.")
else:
    print('Attempting to detect service versions:')
    # For each open port, attempt banner grabbing/service detection
    for open_port in ports:
        banner = banner_grabbing(open_port)
        print(f'[BANNER] {banner}')
