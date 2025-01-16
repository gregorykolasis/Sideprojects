import sys
import subprocess
import re
import requests
import os

# 1) Attempt to import mac_vendor_lookup. If missing, install it from PyPI.
try:
    from mac_vendor_lookup import MacLookup
except ImportError:
    print("[!] Installing mac-vendor-lookup from PyPI...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mac-vendor-lookup"])
    from mac_vendor_lookup import MacLookup


def init_mac_vendor_lookup():
    """
    Initialize mac_vendor_lookup and optionally update local database.
    """
    mac_lookup = MacLookup()
    try:
        # This downloads a ~350KB JSON file from GitHub with MAC vendor data.
        mac_lookup.update_vendors()
    except Exception as e:
        print(f"[!] Could not update mac-vendor-lookup: {e}")
    return mac_lookup


def get_manuf_data(local_file="manuf.txt"):
    """
    Return the text content of the Wireshark manuf file, cached in `local_file`.

    1) If local_file doesn't exist, download from GitHub once and save it.
    2) Otherwise, just read from the local file.
    """
    if not os.path.exists(local_file):
        print(f"[*] Local manuf file '{local_file}' not found. Downloading...")
        manuf_data = download_manuf_file()
        # Save to disk
        with open(local_file, "w", encoding="utf-8") as f:
            f.write(manuf_data)
        print(f"[*] Saved Wireshark manuf to '{local_file}'.")
    else:
        print(f"[*] Reading Wireshark manuf from '{local_file}'...")
        with open(local_file, "r", encoding="utf-8") as f:
            manuf_data = f.read()

    return manuf_data


def download_manuf_file():
    """
    Downloads the Wireshark manuf file from GitHub (master branch).
    Returns the text content.
    
    If the URL changes or is unreachable, you may have to update it or host your own copy.
    """
    url = "https://github.com/boundary/wireshark/raw/refs/heads/master/manuf"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_manuf(manuf_data):
    """
    Parses the Wireshark manuf data into a list of (prefix, bits, vendor).
    """
    entries = []
    for line in manuf_data.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # Regex to capture prefix (maybe with /bits) and vendor
        match = re.match(r"^([0-9A-Fa-f:]+)(?:/(\d+))?\s+([^#]+)", line)
        if not match:
            continue
        
        prefix_str, bits_str, vendor_str = match.groups()
        prefix_str = prefix_str.upper().strip()
        vendor_str = vendor_str.strip()
        
        # Determine how many bits
        if bits_str:
            bits = int(bits_str)
        else:
            parts = prefix_str.split(":")
            bits = len(parts) * 8  # 3 bytes => 24 bits, 6 bytes => 48 bits, etc.
        
        entries.append((prefix_str, bits, vendor_str))
    return entries


def lookup_mac_in_manuf(mac, manuf_entries):
    """
    Find the best (longest) prefix match among manuf_entries for the given MAC.
    """
    mac_upper = mac.upper().replace(":", "")
    best_match_bits = -1
    best_vendor = None
    
    for (prefix_str, bits, vendor_str) in manuf_entries:
        prefix_hex = prefix_str.replace(":", "")
        needed_hex_chars = bits // 4  # e.g. 24 bits -> 6 hex chars
        
        if len(prefix_hex) < needed_hex_chars:
            continue
        
        # Compare the first N hex characters
        if mac_upper[:needed_hex_chars] == prefix_hex[:needed_hex_chars]:
            if bits > best_match_bits:
                best_match_bits = bits
                best_vendor = vendor_str
    
    return best_vendor if best_vendor else None


def combined_lookup(mac, mac_lookup, manuf_entries):
    """
    1) Try mac-vendor-lookup.
    2) If that fails, try the Wireshark manuf data.
    3) Otherwise, return "Unknown Vendor".
    """
    # 1) mac_vendor_lookup
    try:
        vendor = mac_lookup.lookup(mac)
        return vendor
    except KeyError:
        pass  # Not found in mac_vendor_lookup

    # 2) Wireshark manuf
    vendor = lookup_mac_in_manuf(mac, manuf_entries)
    if vendor:
        return vendor

    # 3) Fallback
    return "Unknown Vendor"


def initVendorMap():
    global manuf_entries,mac_lookup
    # Initialize mac-vendor-lookup
    mac_lookup = init_mac_vendor_lookup()
    # Check if 'manuf.txt' exists locally; if not, download once
    manuf_data = get_manuf_data(local_file="manuf.txt")
    manuf_entries = parse_manuf(manuf_data)

def getVendor(mac):
    global manuf_entries,mac_lookup
    vendor = combined_lookup(mac, mac_lookup, manuf_entries)
    return vendor
    
def testMacs():
    test_macs = [
        "00:50:56:AB:CD:EF",  # VMware
        "00:1A:2B:44:55:66",  # Could be 'AyecomTe' or unknown
        "DC:A6:32:11:22:33"   # Jabra / Netgear / Raspberry Pi, etc., depending on DB
    ]
    for mac in test_macs:
        print(f"MAC: {mac} => {getVendor(mac)}")


if __name__ == "__main__":
    initVendorMap()
    testMacs()
