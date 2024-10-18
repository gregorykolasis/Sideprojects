import select
import socket
import time

ip = '192.168.1.2'
port = 80

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.settimeout(1)
conn.connect((ip, port))

while True:
    try:
        ready_to_read, ready_to_write, in_error = \
            select.select([conn,], [conn,], [], 5)
    except select.error:
        conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
        conn.close()
        # connection error event here, maybe reconnect
        print('connection error')
        break
    if len(ready_to_read) > 1:
        recv = conn.recv(2048)
        # do stuff with received data
        print(f'received: {recv}')
        print(len(ready_to_read))
        time.sleep(0.1)
    if len(ready_to_write) > 0:
        # connection established, send some stuff
        conn.send(b'A')
        time.sleep(0.1)