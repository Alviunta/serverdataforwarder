from .contact_id import calculate_checksum
from .contact_id import generate_checksum
from .contact_id import process_incomming_CID
import logging
logging.getLogger('CID_LOG').addHandler(logging.NullHandler())
__all__ = ['calculate_checksum', 'generate_checksum', 'process_incomming_CID']