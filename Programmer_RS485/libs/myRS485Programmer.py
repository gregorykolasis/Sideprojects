import asyncio 
import os
from datetime import datetime
import numpy as np
import serial
import re
import sys
import time

FC_BUS_FIRMWARE_UPDATE_START = 241
FC_BUS_FIRMWARE_UPDATE_START_BROADCAST = 242
FC_BUS_FIRMWARE_UPDATE_CHUNK = 251
BROADCAST_ADDRESS = 222
CHUNK_SIZE = 223
ACK_TIMEOUT = 5
FIRMWARE_PATH = 'Unknown'

def format_time(seconds: float) -> str:
    """Convert float seconds to H:MM:SS or M:SS for display."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:d}h {minutes:02d}m {secs:02d}s"
    elif minutes > 0:
        return f"{minutes:d}m {secs:02d}s"
    else:
        return f"{secs:d}s"

class myRS485Programmer(asyncio.Protocol):

    debugOutgoingMessages = False

    def __init__(self, loop=None):
        self.loop = loop
        self.line_queue = asyncio.Queue()  # Queue for received lines
        self.start_firmware_upgrade = asyncio.Event() # Set when connection is made
        self.startProgramming = False
        self.update_start_time = 0

    def handle_recieved(self,decoded_data):
        # if self.startProgramming == False:
        now = datetime.now()
        timeNow = now.strftime('%H:%M:%S.%f')[:-3]
        self.logger.info(f"{timeNow} -> {decoded_data}")

        self.line_queue.put_nowait(decoded_data)
        if 'SOLVED' in decoded_data:
            self.start_firmware_upgrade.set()  # Signal that we are connected



    async def send_serial_bytes(self, payload: bytes):
        message = b'@' + payload + b'#'
        self.send_serial_data(message)

    async def send_string_cmd(self, command: str):
        command_message = f"@{command}#".encode()
        self.send_serial_data(command_message)
        print(f"[INFO] Sent string: {command_message}")

    async def send_start_command(self, slave_address, firmware_size, total_chunks, firmware_version):
        version_bytes = firmware_version.encode('ascii', 'ignore')[:8]
        version_bytes = version_bytes.ljust(8, b'\0')
        payload = bytearray()
        payload.append(slave_address)
        if slave_address == BROADCAST_ADDRESS:
            payload.append(FC_BUS_FIRMWARE_UPDATE_START_BROADCAST)
        else:
            payload.append(FC_BUS_FIRMWARE_UPDATE_START)
        payload += firmware_size.to_bytes(4, 'little')
        payload += total_chunks.to_bytes(4, 'little')
        payload += version_bytes

        await self.send_serial_bytes(payload)
        print("[INFO] Sent FIRMWARE-UPDATE-START command.")


    async def wait_for_ack(self, chunk_num: int):
        expected_ack = f"[Firmware] Chunk {chunk_num},Ok"
        resend_ack   = f"[Firmware] Chunk {chunk_num},Resend"
        start_ack    = f"[Firmware] Start update command,Ok"

        try:
            while True:
                line = await asyncio.wait_for(self.line_queue.get(), timeout=ACK_TIMEOUT)
                if expected_ack in line:
                    # Got normal ACK
                    return "OK"
                elif resend_ack in line:
                    # Got resend request
                    return "RESEND"
                elif start_ack in line:
                    # Got resend request
                    return "STARTED"
        except asyncio.TimeoutError:
            return "TIMEOUT"

    def print_progress(self,chunk_num,total_chunks):
        # -- Calculate progress percentage
        progress = chunk_num / total_chunks
        # -- Calculate ETA
        elapsed_time = time.time() - self.update_start_time  # how long we've been sending
        # Avoid division by zero for the first chunk
        average_time_per_chunk = (elapsed_time / chunk_num) if chunk_num > 0 else 0
        remaining_chunks = total_chunks - chunk_num
        eta_seconds = average_time_per_chunk * remaining_chunks
        eta_str = format_time(eta_seconds)
        # -- Create progress bar
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        # -- Print progress info (bypassing your custom logger)
        sys.__stdout__.write(
            f"\r[PROGRESS] Chunk {chunk_num}/{total_chunks} Remaining Bytes:"
            f"[{bar}] {progress * 100:5.1f}%  ETA: {eta_str}"
        )
        sys.__stdout__.flush()


    async def send_firmware_chunk(self, slave_address, current_chunk_num, chunk, chunk_num, total_chunks):
        chunk_length = len(chunk)

        payload = bytearray()
        payload.append(slave_address)
        payload.append(FC_BUS_FIRMWARE_UPDATE_CHUNK)
        payload += current_chunk_num.to_bytes(4, 'little')
        payload.append(chunk_length)
        message = b'@' + payload + chunk + b'#'

        #Print each byte in decimal form separated by spaces

        if self.debugOutgoingMessages:
            data_str = ' '.join(str(b) for b in message)
            print(f"[Send] Chunk {chunk_num}/{total_chunks} ->{data_str}")     

        # if '@' in str(payload):
        #     print(f"[@] in Payload at Chunk {chunk_num}/{total_chunks}")
        # if '#' in str(payload):
        #     print(f"[#] in Payload at Chunk {chunk_num}/{total_chunks}")            
        # if '@' in str(chunk):
        #     print(f"[@] in Body at Chunk {chunk_num}/{total_chunks}")
        # if '#' in str(chunk):
        #     print(f"[#] in Body at Chunk {chunk_num}/{total_chunks}")    

        # Some loop for possible retries
        max_retries = 3
        retries = 0
        while True:
            # Send the chunk
            self.send_serial_data(message)

            #if self.debugOutgoingMessages == False: self.print_progress(chunk_num,total_chunks)

            ack_result = await self.wait_for_ack(chunk_num)
            if ack_result == "OK":
                # Normal success
                return True
            elif ack_result == "RESEND":
                # We got a request to resend. Attempt another send unless we exceed max retries
                retries += 1
                if retries > max_retries:
                    self.logger.warning(f"[ERROR] Too many resend requests for chunk {chunk_num}. Aborting.")
                    return False
                self.logger.warning(f"[INFO] Got 'Resend' for chunk {chunk_num}, retrying... (attempt {retries})")
                # Loop continues, so we re-send
            else:  # "TIMEOUT"
                self.logger.warning(f"[ERROR] No ACK received (timeout) for chunk {chunk_num}. Aborting.")
                return False

    def extract_firmware_version(self,filename):
        # Remove extensions until no more extensions remain:
        no_ext = filename
        while True:
            base, ext = os.path.splitext(no_ext)
            if not ext:  # No more extension
                break
            no_ext = base
        # Regex to capture something like V3_04
        pattern = r'(V\d+_\d+)'
        match = re.search(pattern, no_ext)
        if match:
            return match.group(1)  # "V3_04"
        else:
            return None

    async def update_firmware(self, filePath=FIRMWARE_PATH, slave_address=0, bus_num=-1, start_chunk=1):
        # Wait until connection is actually established
        await self.start_firmware_upgrade.wait()
        # Send an initial string if needed

        if slave_address == 222:
            await self.send_string_cmd("FW-MASS-UPDATE-START")  # Bus
        else:
            await self.send_string_cmd("FW-UPDATE-START")  # Slave

        await asyncio.sleep(1)  # Give the ESP32 time to process the start command

        if not os.path.exists(filePath):
            print(f"[ERROR] Firmware file not found at {filePath}")
            return

        with open(filePath, 'rb') as firmware_file:
            firmware = firmware_file.read()

        firmware_size = len(firmware)
        total_chunks = (firmware_size + CHUNK_SIZE - 1) // CHUNK_SIZE

        firmware_version = self.extract_firmware_version(filePath)

        self.logger.critical(f"[INFO] V:{firmware_version} Firmware size: {firmware_size} bytes, Total chunks: {total_chunks}")

        print("[INFO] Sending firmware update start command...")
        await self.send_start_command(
            slave_address=slave_address,
            firmware_size=firmware_size,
            total_chunks=total_chunks,
            firmware_version=firmware_version
        )

        await asyncio.sleep(1)  # Give the ESP32 time to process the start command
        start_result = await self.wait_for_ack(0)

        if start_result == "STARTED":
            # Send firmware chunks
            self.logger.critical("[INFO] Sending firmware chunks...")
            self.update_start_time = time.time()  # Store start time for ETA calculation
            current_chunk_num = 1  # Reset chunk numbering

            # Calculate the starting byte index based on the desired starting chunk
            start_index = (start_chunk - 1) * CHUNK_SIZE

            # Adjust total_chunks if you want to reflect the remaining chunks
            remaining_chunks = total_chunks - (start_chunk - 1)

            self.startProgramming = True

            for i in range(start_index, firmware_size, CHUNK_SIZE):
                chunk = firmware[i:i + CHUNK_SIZE]

                # Send the chunk with chunk_num starting at 1
                success = await self.send_firmware_chunk(
                    slave_address=slave_address,
                    current_chunk_num=current_chunk_num,
                    chunk=chunk,
                    chunk_num=current_chunk_num,  # Reset chunk_num to start at 1
                    total_chunks=remaining_chunks  # Update total_chunks to remaining
                )

                if not success:
                    self.logger.error("[ERROR] Firmware update aborted due to missing ACK.")
                    self.startProgramming = False
                    return

                current_chunk_num += 1
                await asyncio.sleep(0.05)  # Brief pause between chunks

            self.logger.critical("[INFO] All chunks sent. Waiting for ESP32 to finalize update.")
        else:
            self.logger.critical("[ERROR] Failed to receive firmware update start response!")

        self.startProgramming = False
        await self.reset_serial()
