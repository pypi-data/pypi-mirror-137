

import re
import socket
from collections import namedtuple
from nmap import PortScanner
from core.shell import run_shell




def is_port_open(ip_address: str, port: int | str, timeout: int = 1) -> bool:

    if isinstance(port, str):
        port = int(port)

    try:
        socket.create_connection((ip_address, port), timeout).close()
    except:
        return False

    return True


def scan_ports(
    hostname: str,
    _port: int = 1,
    port_: int = 65535
):
    ip_address = socket.gethostbyname(hostname)

    OpenPort = namedtuple("OpenPort", ["ip", "port"])
    open_ports = []
    for port in range(_port, port_):
        if is_port_open(ip_address, port):
            open_ports.append(OpenPort(ip_address, port))

    return open_ports



def is_ip_address_valid(ip_address: str) -> bool:
    if not isinstance(ip_address, str):
        return False
        # raise TypeError(f"@ip_address: '{ip_address}' must be type of string. what got: {type(ip_address)}")

    ip_bytes = ip_address.split(".")
    if not len(ip_bytes) == 4:
        return False
        # raise ValueError(f"@ip_address: '{ip_address}' must have 4 sections of bytes")

    for _byte in ip_bytes:
        try:
            _byte = int(_byte)
        except ValueError:
            return False
        else:
            if not (0 <= _byte < 256):
                return False

    return True


class InvalidIpAddress(Exception):
    pass

def _validate_ip_address(ip_address: str):
    if not is_ip_address_valid(ip_address):
        raise InvalidIpAddress(f"@ip_address: '{ip_address}' is invalid")

def is_port_online(ip_address: str, port=22) -> bool:
    _validate_ip_address(ip_address)

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_client.connect((ip_address, port))
    except socket.error as error:
        print(f"IP: {ip_address} {error}")
        return False

    return True


# def is_server_online(ip_address: str) -> bool:
#     nmap_scanner = PortScanner()
#     ip_address = socket.gethostbyname(ip_address)
#     print(ip_address)
#     nmap_scanner.scan(ip_address, '1', '-v')
#     print(nmap_scanner[ip_address])
#     return nmap_scanner[ip_address].state() == "up"
def is_server_online(ip_address: str) -> bool:
    _validate_ip_address(ip_address)
    ping_command = f"ping -c 1 {ip_address}"
    return run_shell(ping_command, devnull=True) == 0
