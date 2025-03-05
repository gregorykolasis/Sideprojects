from wakeonlan import send_magic_packet

mac = 'C8-7F-54-65-F1-DF'

try:
    print(f"Sending WOL Packet on Mac:{mac}")
    send_magic_packet(mac)
except Exception as e:
    print(f"Error {e} sending WOL Packet on Mac:{mac}")

while True:
    x=1