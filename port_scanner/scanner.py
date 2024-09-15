'''
script by: Chanan Shnker
This is a little project I've been working on. 
This script is a port scanner that checks what ports are open and then attempts to do banner grabbing/service detection.
Obviously Nmap exists and does this job much faster and with more features, but this is part of my Python learning journey.
'''

import sys
import argparse  # For command-line argument parsing
import socket    # For creating network connections (sockets)
import ipaddress # For IP address validation

# Set up the argument parser
parser = argparse.ArgumentParser()

# Define the available command-line arguments
parser.add_argument("-t", "--target", help="target to scan")
parser.add_argument("-b", "--banner", help="attempt to retrieve a banner from the open port", action="store_true")
parser.add_argument("-v", "--verbose", help="display results as they are discovered", action="store_true")
parser.add_argument("-o", "--output", help="file to save the output to")

# Parse the arguments
args = parser.parse_args()

# Assign the target IP from the arguments
IP = args.target

# Initialize lists to store open ports and output data
ports = []
output = []

# Function to validate if the IP address is valid
def validate_ip(ip):
    try:
        # Use ipaddress library to check if the IP address is valid
        ipaddress.ip_address(ip) 
        return True
    except:
        return False

# Function to scan a single port
def port_scanning(port):
    # Create a new TCP socket (IPv4)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout of 3 seconds for the connection attempt
    socket.setdefaulttimeout(3)
    try:
        # Try to connect to the target IP and port
        sock.connect((IP, port))
        return True  # Return True if the connection is successful (port is open)
    except:
        return False  # Return False if the connection fails (port is closed)
    finally:
        # Close the socket after the attempt
        sock.close()

# Function to attempt banner grabbing from an open port
def banner_grabbing(open_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(3)  # Set a 3-second timeout
    try:
        # Try to connect to the target IP and open port
        sock.connect((IP, open_port))
        # Try to receive 1024 bytes of data (the banner)
        banner = sock.recv(1024).decode('utf-8').strip()
        sock.close()
        if banner:
            return banner  # Return the banner if data was received
        else:
            return 'No banner received'  # No banner found
    except:
        return 'Error! Could not receive banner'  # Return an error if unable to get the banner
    finally:
        sock.close()  # Close the socket

# If no arguments are provided, display the help message
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

# If the target IP is valid, start scanning
if validate_ip(IP):
    print(f'Starting scan on {IP}:')
    # Scan all 65535 ports
    for port in range(65535):
        if port_scanning(port):  # If the port is open
            port_output = f'[OPEN] Port {port} found open'  # Format the output for the open port
            ports.append(port)  # Add the open port to the list
            if args.verbose:  # If verbose mode is enabled, print the result immediately
                print(port_output)
            output.append(port_output)  # Store the result for later output
else:
    # Print error if the IP address is invalid and exit
    print(f'The IP address {IP} is not valid!')
    sys.exit()

# If the banner grabbing option is enabled and there are open ports
if args.banner:
    if len(ports) == 0:
        print("No ports seem to be found open on the host.")  # No open ports found
    else:
        print('Attempting to detect service versions:')
        for open_port in ports:
            # For each open port, attempt to grab the banner
            banner = banner_grabbing(open_port)
            banner_output = f'[BANNER] port {open_port}: {banner}'  # Format the banner output
            if args.verbose:  # Print the banner if verbose mode is enabled
                print(banner_output)
            output.append(banner_output)  # Store the banner result for later output

# If verbose mode is not enabled, print all results at the end
if args.verbose == False:
    for line in output:
        print(line)

# If the output option is set, write all results to the specified file
if args.output:
    with open(args.output, "a") as f:
        for line in output:
            f.write(line + '\n')  # Write each line of output to the file
