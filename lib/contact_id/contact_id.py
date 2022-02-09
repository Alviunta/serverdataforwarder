import logging
class WrongArgError(Exception):
    pass
logging.getLogger('CID_LOG').setLevel(logging.DEBUG)
def calculate_checksum(recived, separator = " "):
    if separator is None:
       raise Exception("Separator not set")
    ret_checksum = 0
    for i in range(len(recived)):
        if recived[i] != separator:
            if recived[i] == '0':
                ret_checksum += 10
            else:
                ret_checksum += int("0x"+recived[i], 16)
    ret_checksum %= 15
    return ret_checksum

def generate_checksum(generate_cks, separator = " "):
    """Esta funcion calcula el checksum correspondiete al string ingresado de acuerdo al estandar de Contact ID 

    Args:
        generate_cks (String): Esta variable es la cadena a la que se le calcula el checksum.
        separator (str, optional): Separator used to generate string. Defaults to " ".

    Raises:
        Exception: Separator is none

    Returns:
        Hex: Hex value according to imput string.
    """
    if separator is None:
        raise Exception("Separator not set")
    cksum = 0
    for i in range(len(generate_cks)-1):
        if generate_cks[i] != separator:
            if generate_cks[i] == '0':
                cksum += 10
            else:
                cksum += int("0x"+generate_cks[i], 16)
    cksum = 15 - (cksum%15)
    if cksum == 0x0:
        cksum = 0xf
    return  cksum

def process_incomming_CID(recived, separator = " "):
    """
    Parameters:
        :-> CID string
        :-> Character separator
    Expected format: (length 21)
        Formato: AAAA TT QEEE PP UUU S
         -> AAAA: account number (0-9, B-F)
         -> TT: Message type (CID = 18)
         -> Q: Qualifier  1 - New event / 3 - restoral / 6 - Previously reported condition still present
         -> EEE: Event code (3 Hex digits 0-9,B-F)
         -> PP: Group or Partition number (2 Hex digits 0-9, B-F). 00 indicate no specific group
         -> UUU: Zone number (Event reports) or User# (Open / Close reports ) (3 Hex digits 0-9,B-F ). 000 indicate no specific zone or user
         -> S: 1 Digit Hex checksum calculated such that: (Sum of all message digits + S) MOD 15 = 0 
    """
    if len(recived) != 21:
        raise Exception("Message length error - must be 21 {}".format(len(recived)))
    if recived[-1] == '0':
        try:
            recived = recived[0:-1] + hex(generate_checksum(recived, separator))[-1]
        except Exception as exc:
            raise Exception("Generate_checksum issue")
    parameter_CID = recived.split(separator)
    parameter_CID.insert(3, parameter_CID[2])
    parameter_CID[2] = parameter_CID[2][0]
    parameter_CID[3] = parameter_CID[3][1:]

    values = ("AccountNumber", "MessageType", "Qualifier", "EventCode", "PartitionNumber", "ZoneUserNumber", "Checksum")
    ret_dictionary = {"AccountNumber": "", "MessageType" : "", "Qualifier" : "", "EventCode" : "", "PartitionNumber" : "", "ZoneUserNumber" : "", "Checksum" : ""}

    try:
        calculate_checksum(recived, separator)
    except Exception as exc:
        logging.debug(recived)
        logging.debug("Wrong checksum")
        raise Exception("Wrong checksum") 

    if len(parameter_CID) != len(values):
        logging.debug("Error in CID format. Wrong field count.")
        logging.debug("CID error format: %s - %d", recived, len(parameter_CID))
        raise Exception("Error in CID format. Wrong field count.")
    elif parameter_CID[1] != "18":
        logging.debug("Message type not suported: %s", parameter_CID[1])
        raise Exception("Wrong message type - expected: 18")
    elif not parameter_CID[2] in ('1', '3', '6'):
        logging.debug("Invalid Qualifier %s", parameter_CID[2])
        raise Exception("Wrong CID - Qualifier not suported")

    for element in range(len(parameter_CID)):
        ret_dictionary.update({values[element] : parameter_CID[element]})

    logging.debug("CID message %s", ret_dictionary)
    return ret_dictionary

