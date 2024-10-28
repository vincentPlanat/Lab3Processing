# Using the third party `aiorun` instead of the `asyncio.run()` to avoid
# boilerplate.
import aiorun
import asyncio
import argparse, sys, os
from datetime import datetime
import logging
import hl7
from hl7.mllp import start_hl7_server

# CLI arguments
parser = argparse.ArgumentParser(description="Server mllp listening on given port (-p <value>)")

# Logger config
logger = logging.getLogger('mon_logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Création du handler pour le fichier
file_handler = logging.FileHandler('mllp_server.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Création du handler pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Ajout des handlers au logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# List of segments subject to analyse in file
OR_PARSER_CONFIG = ['MSH', 'PID', 'ORC', 'OBR', 'OBX']
OUT_DIR_PATH = "lab3_out"

############################################################################################
def process_message (source_msg):
    logger.info(f'[process_message] processing a new received file')

    # push file to file system
    now_ts = datetime.now().strftime("%d-%m-%Y_%H:%M:%S.%f")
    out_file_name = f'{out_path}/{comment}___{now_ts}.txt'
    logger.info(f'[process_message] write received message to: {out_file_name}')
    out_file = open(out_file_name, "w") 
    out_file.writelines(source_msg.__str__())
    out_file.close()

    hl7_msg = f'{source_msg}'
    try:
        hl7_obj = hl7.parse(hl7_msg)
        logger.info(f'[process_message] message parsed successfully')
    except BaseException as err_parse:
        logger.error(f'[process_message] ERROR in parsing file: {err_parse}')
    

    # Start hl7 analysis for FHIR creation
    '''
    segments_list = []
    for i in range(len(hl7_obj)):
        segments_list.append(str(hl7_obj[i][0]))
    for sub_field in OR_PARSER_CONFIG:
        if sub_field in segments_list:
            segment_val = str(hl7_obj.segment(sub_field))
            logger.debug(f'[process_message] segment: {sub_field} present in message:  {segment_val.rstrip()}')
        else:
            logger.debug(f'[process_message] segment: {sub_field} not present in message')
    '''


############################################################################################
async def process_hl7_messages(hl7_reader, hl7_writer):
    """This will be called every time a socket connects
    with us.
    """
    peername = hl7_writer.get_extra_info("peername")
    logger.info(f"Connection established {peername}")
    try:
        # We're going to keep listening until the writer
        # is closed. Only writers have closed status.
        while not hl7_writer.is_closing():
            hl7_message = await hl7_reader.readmessage()
            process_message(hl7_message)
            # Now let's send the ACK and wait for the
            # writer to drain
            hl7_writer.writemessage(hl7_message.create_ack())
            await hl7_writer.drain()
    except asyncio.IncompleteReadError:
        # Oops, something went wrong, if the writer is not
        if not hl7_writer.is_closing():
            hl7_writer.close()
            await hl7_writer.wait_closed()
    logger.info(f"Connection closed {peername}")


############################################################################################
async def main():
    try:
        # Start the server in a with clause to make sure we
        # close it
        async with await start_hl7_server(
            process_hl7_messages, port=server_port, encoding='iso-8859-1'
        ) as hl7_server:
            # And now we server forever. Or until we are
            # cancelled...
            await hl7_server.serve_forever()
    except asyncio.CancelledError:
        # Cancelled errors are expected
        pass
    except Exception:
        logger.error("Error occurred in main")


server_port = 0
parser.add_argument("-p", "--port", type=int, default=2575,
                    help="port number used by the server (par défaut: 2575)")
parser.add_argument("-o", "--out", type=str, default=OUT_DIR_PATH,
                    help=f"output directory (default: {OUT_DIR_PATH})")
parser.add_argument("-c", "--comment", type=str, default="default",
                    help=f"test comments used to preffix generated hl7 messages (default: default)")


args = parser.parse_args()
server_port = args.port
out_path = args.out
cmd_ts = datetime.now().strftime("%d-%m-%Y")
#comment = f'ingest:{cmd_ts}'
comment = args.comment

if (not os.path.isdir(out_path)):
    print (f'directory {out_path} for storing hl7 msg does not exist. I create it')
    os.mkdir(out_path)

now_ts = datetime.now().strftime("%d-%m-%Y_%H:%M:%S.%f")
logger.info (f'start listening on {server_port} at: {now_ts}    destination output is: {out_path}  file-comments: {comment}')

aiorun.run(main(), stop_on_unhandled_errors=True)
