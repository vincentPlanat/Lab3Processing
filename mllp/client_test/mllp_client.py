# Using the third party `aiorun` instead of the `asyncio.run()` to avoid
# boilerplate.
import aiorun
import asyncio
import argparse
import time
import os
import sys
import hl7
from hl7.mllp import open_hl7_connection

# CLI arguments
parser = argparse.ArgumentParser(description="Client mllp listening sending on given port (-p <value>)")

async def main():
    # Open the connection to the HL7 receiver.
    # Using wait_for is optional, but recommended so
    # a dead receiver won't block you for long
    hl7_reader, hl7_writer = await asyncio.wait_for(
        open_hl7_connection(DEST_IP, DEST_PORT,encoding='iso-8859-1'),
        timeout=10,
    )

    hl7_files_list = os.listdir(SOURCE_HL7_PATH)
    for file_hl7 in hl7_files_list:
        file_path = f'{SOURCE_HL7_PATH}/{file_hl7}'
        # print (f'processing file: {file_path}')
        lines = open(file_path, encoding="utf8", errors='ignore').readlines()
        msg = '\r'.join(lines)
        try:
            hl7_message = hl7.parse(msg)
        except BaseException as err_parse:
            print(f'[analyse_hl7_file] ERROR in parsing file: {err_parse}')
        
        print(f'send message {file_hl7}')
        # Write the HL7 message, and then wait for the writer
        # to drain to actually send the message
        hl7_writer.writemessage(hl7_message)
        await hl7_writer.drain()
        
        # Now wait for the ACK message from the receiever
        hl7_ack = await asyncio.wait_for(
        hl7_reader.readmessage(),
        timeout=10
        )
        print(f'Received ACK\n {hl7_ack}'.replace('\r', '\n'))

parser.add_argument("-s", "--system", type=str, default="192.168.0.105",
                    help="destination system running the mllp server (default: 192.168.0.105)")
parser.add_argument("-p", "--port", type=int, default=2575,
                    help="destination port number used by the mllp server (default: 2575)")
parser.add_argument("-i", "--inpath", type=str, default="hl7_msg",
                    help=f"input directory sourcing the test hl7 msg (default: hl7_msg)")
args = parser.parse_args()
DEST_IP = args.system
DEST_PORT = args.port
SOURCE_HL7_PATH = args.inpath

if (not os.path.isdir(SOURCE_HL7_PATH)):
    print (f'directory {SOURCE_HL7_PATH} containing hl7 msg does not exist. Exit')
    sys.exit()

print (f'client sending traffic to: {DEST_IP}:{DEST_PORT}')

aiorun.run(main(), stop_on_unhandled_errors=True)