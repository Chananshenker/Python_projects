'''
script by: Chanan Shnker
This is a port scanner that checks for open ports and attempts banner grabbing/service detection.
'''

import sys
import argparse
import socket
import ipaddress

# Set up argument parser
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--target", help = "target to scan")
parser.add_argument("-b", "--banner", help = "attempt to retrieve a banner", action="store_true")
parser.add_argument("-v", "--verbose", help = "display results as discovered", action="store_true")
parser.add_argument("-o", "--output", help = "file to save the output to")
parser.add_argument("-e", "--extensive", help = "scan all 65535 ports (default 1-9999)", action="store_true")

args = parser.parse_args()

IP = args.target
ports = []
output = []

# Validate the target IP address
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip) 
        return True
    except:
        return False

# Check if the port is open
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

# Identify service by port number
def find_service_by_port(port):
    try:
        service = socket.getservbyport(port)
        return service
    except OSError:
        return "Unknown service"

# Attempt to grab a banner from an open port
def banner_grabbing(open_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2) 
    try:
        sock.connect((IP, open_port))
        banner = sock.recv(1024).decode('utf-8').strip()
        sock.close()
        if banner:
            return banner  
        else:
            return 'No banner received'
    except:
        return 'Error! Could not receive banner'
    finally:
        sock.close() 

# Main scanning loop
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

port_range = 65535 if args.extensive else 9999

if validate_ip(IP):
    print(f'[SCANNER] Starting scan on {IP}:')
    for port in range(port_range):
        if port_scanning(port):
            service = find_service_by_port(port)
            port_output = f'[OPEN] Port {port} ({service}) found open'
            ports.append(port) 
            if args.verbose and not args.banner:
                print(port_output)
            if not args.banner:
                output.append(port_output)
else:
    print(f'The IP address {IP} is not valid!')
    sys.exit()

# Perform banner grabbing if specified
if args.banner:
    if len(ports) == 0:
        print("No ports seem to be found open on the host.")
    else:
        print('[SCANNER] Attempting to detect service versions:')
        for open_port in ports:
            banner = banner_grabbing(open_port)
            service = find_service_by_port(open_port)
            banner_output = f'[OPEN] port {open_port} open ({service}): {banner}'
            if args.verbose:
                print(banner_output)
            output.append(banner_output)

# Print output if not verbose
if not args.verbose:
    for line in output:
        print(line)

# Save output to file if specified
if args.output:
    with open(args.output, "a") as f:
        for line in output:
            f.write(line + '\n')
