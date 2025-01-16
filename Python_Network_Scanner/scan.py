import argparse
import json
import socket
import time
import os
import sys
import concurrent.futures
from ipaddress import ip_address
from vendor import initVendorMap,getVendor

try:
    from scapy.all import srp, sr1, Ether, ARP, IP, ICMP
except ModuleNotFoundError:
    os.system("pip install scapy")
    sys.exit()

def guess_interface_type(mac):
    """
    Basic OUI lookup approach to guess if device is Wi-Fi or Ethernet.
    Requires an OUI database or API lookup for real accuracy.
    """
    # 1) Extract the first 3 bytes (OUI) from the MAC address
    #    e.g. "00:1A:2B" from "00:1A:2B:44:55:66"
    oui = mac.upper()[0:8].replace(":", "-")  # "00-1A-2B"
    
    # 2) Query an OUI DB (either a local file or API).
    #    Here, we’ll pretend we have a dictionary of known OUIs.
    #    This is just an example; in practice you'd load a large DB.
    known_ouis = {
        "00-1A-2B": "Intel Corporate (Wireless)",  
        "00-1B-2C": "Intel Corporate (Wired)"
        # ... etc.
    }
    
    vendor_info = known_ouis.get(oui, "Unknown Vendor")
    if "Wireless" in vendor_info or "Wi-Fi" in vendor_info:
        return "Wi-Fi"
    elif "Ethernet" in vendor_info or "Wired" in vendor_info:
        return "Ethernet"
    else:
        return "Unknown"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target',
                        help='Target IP/subnet (e.g. 192.168.1.0/24)',
                        required=False)
    return parser.parse_args()

def get_hostname(ip_address):
    """
    Attempt to perform a reverse DNS lookup to get the hostname.
    Returns None if lookup fails.
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return None

def get_ping_time(ip_address, timeout=1.0):
    """
    Send an ICMP Echo Request (ping) to the given IP and measure round-trip time (ms).
    Return None if host is unreachable or times out.
    """
    start_time = time.time()
    resp = sr1(IP(dst=ip_address)/ICMP(), timeout=timeout, verbose=False)
    if resp is None:
        return None
    end_time = time.time()
    return round((end_time - start_time) * 1000, 2)  # milliseconds

def scan_ports(ip_address, ports=[22, 23, 80, 443, 445, 3389]):
    """
    Attempt a simple TCP connect scan on a list of ports.
    Returns a list of open ports.
    """
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip_address, port)) == 0:
                open_ports.append(port)
    return open_ports

def arp_scan(ip):
    """
    ARP-scan the target IP/subnet.
    Returns a list of (sent_pkt, recv_pkt) tuples.
    """
    arp_req = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    answered = srp(broadcast/arp_req, timeout=2, verbose=False)[0]
    return answered

def gather_host_info(ip_address, mac_address):
    """
    For a given IP and MAC, gather hostname, ping time, open ports, etc.
    Returns a dictionary with the host information.
    """
    hostname = get_hostname(ip_address)
    ping_time = get_ping_time(ip_address)
    uptime = None  # Placeholder, real uptime would need SNMP or another method
    open_ports = scan_ports(ip_address)
    interface_type = guess_interface_type(mac_address)
    
    return {
        "IP": ip_address,
        "MAC": mac_address,
        "Hostname": hostname,
        "Ping": ping_time,
        "Uptime": uptime,
        "OpenPorts": open_ports,
        "Vendor": getVendor(mac_address),   # Wi-Fi / Ethernet / Unknown
    }

def main():
    options = get_args()

    # 1) ARP SCAN to discover live hosts
    if options.target == None:
        options.target = "192.168.1.0/24"
    
    print(f"[ARP_SCAN] Started for IP(s) ->{options.target}")
    answered_list = arp_scan(options.target)
    print("[ARP_SCAN] Finished")

    initVendorMap()

    # 2) Prepare a list of tasks (ip, mac) for each discovered host
    tasks = []
    for sent_pkt, recv_pkt in answered_list:
        ip = recv_pkt.psrc
        mac_address = recv_pkt.hwsrc
        tasks.append((ip, mac_address))

    results = []

    # 3) Use multithreading to speed up per-host checks (hostname, ping, port scan)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_ip = {
            executor.submit(gather_host_info, ip, mac): ip
            for (ip, mac) in tasks
        }

        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                host_info = future.result()
                results.append(host_info)
            except Exception as e:
                print(f"[-] Error gathering info for {ip}: {e}")

    # Sort the results in ascending order by IP
    results.sort(key=lambda r: ip_address(r["IP"]))
    # 4) Print each device as JSON
    for i, device_info in enumerate(results, start=1):
        print(f"[{i}] -> {json.dumps(device_info, indent=4)}")

if __name__ == "__main__":
    main()
    while True:
        nothing = 1
