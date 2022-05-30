import logging
import string

class contact_id():
    def __init__(self, allowchecksum = True, checksumgenerator = False, separator = ' ', loggername = None):
        """_summary_

        Args:
            allowchecksum (bool, optional): Enable / Disable checksum validation. Defaults to True.
            checksumgenerator (bool, optional): Enable / Disable checksum generation when checksum is setted to 0. Defaults to False.
            separator (str, optional): Used to split string into parameters. Defaults to ' '.
            loggername (_type_, optional): Logger name, used as "logging.getLogger(loggername)". Logging configuration must be setted appart. Defaults to None.
        """
        #AAAA TT QEEE PP UUU C
        self.checksumallowed = allowchecksum
        self.generatorallowed = checksumgenerator
        self.separator = separator.upper()
        
        self.expectedaccountlen = 4
        self.expectedmessagetype = "18"
        self.expectedqualifiers = ("1","3","6")
        self.expectedeventlen = 3
        self.expectedpartitionlen = 2
        self.expecteduserlen = 3
        self.expectedmsglen = 16 + len(separator)*5
        self.retchecksum = None
        
        self.allowedchar = set(string.hexdigits)
        self.allowedchar.add(self.separator)
        
        if loggername is not None:
            self.log =logging.getLogger(loggername)
            self.loggerenabled = True
        else:
            self.loggerenabled = False   
        
    def _checksumgenerator(self):
        cksum = 0
        for parameter in range(len(self.splitmsg)-1):
            for position in range(len(self.splitmsg[parameter])):
                if self.splitmsg[parameter][position] =='0':
                    cksum += 10
                else:
                    cksum += int("0x"+self.splitmsg[parameter][position],16)
        cksum = 15 - (cksum%15)
        if cksum == 0x0:
            cksum = 0xf
        self.splitmsg[6]= '{:X}'.format(cksum)
    
    def _checksum(self):
        ret_checksum = 0
        for parameter in self.splitmsg:
            for position in range(len(parameter)):
                if parameter[position] == '0':
                    ret_checksum +=10
                else:
                    ret_checksum += int("0x"+parameter[position],16)
        ret_checksum %=15
        self.retchecksum = ret_checksum
    
    def _validatemessage(self):
        self.valid = True
        if len(self.message) < 1:
            self.valid = False
            self.log.error("Void message content")
            return
        self.splitmsg = self.message.split(self.separator)
        if len(self.splitmsg) == 6:
            self.splitmsg.insert(3,self.splitmsg[2])
            self.splitmsg[2] = self.splitmsg[2][0]
            self.splitmsg[3] = self.splitmsg[3][1:]
        elif len(self.splitmsg)==7:
            pass
        else:
            self.valid = False
            self.log.error("Message content error:: could not be splitted: Current {0}".format(self.message))
            return 

        for s in self.splitmsg:
            for c in s:
                if c not in self.allowedchar:
                    self.valid = False
                    self.log.error("Message content error:: Invalid characters: allowed: {0} Current {1} Error : {2}".format(self.allowedchar, self.message, c))
                    return
                
        if len(self.message) != self.expectedmsglen:
            #LONGITUD DE MENSAJE ERRONEO
            if self.loggerenabled is True:
                self.log.error("Message length error:: Expected {0} Current {1}".format(self.expectedmsglen, len(self.message)))
            self.valid = False
            
            
        if len(self.splitmsg[0]) != self.expectedaccountlen:
            #LONGITUD DE CUENTA ERRONEA
            if self.loggerenabled is True:
                self.log.error("Message account length error:: Expected {0} Current {1}".format(self.expectedaccountlen,len(self.splitmsg[0])))
            #raise Exception("Message account length error")  
            self.valid = False          
            
        if self.splitmsg[1] != self.expectedmessagetype:
            #EL TIPO DE MENSAJE ES ERRONEO
            if self.loggerenabled is True:
                self.log.error("Message type error:: Expected {0} Current {1}".format(self.expectedmessagetype, self.splitmsg[1]))
            #raise Exception("Message type error")
            self.valid = False

        if self.splitmsg[2] not in self.expectedqualifiers:
            #EL CALIFICADOR NO ESTA ACEPTADO
            if self.loggerenabled is True:
                self.log.error("Qualifier unknown:: Expected {0} Current {1}".format(str(self.expectedqualifiers), self.splitmsg[2]))
            #raise Exception("Qualifier unknown")
            self.valid = False
        
        if len(self.splitmsg[3]) != self.expectedeventlen:
            #LA LONGITUD DEL EVENTO NO ES VALIDA
            if self.loggerenabled is True:
                self.log.error("Message event length error:: Expected {0} Current 1".format(self.expectedeventlen,len(self.splitmsg[3])))
            #raise Exception("Message event length error")    
            self.valid = False
        if len(self.splitmsg[4]) != self.expectedpartitionlen:
            #LA LONGITUD DE PARTICION NO ES VALIDA
            if self.loggerenabled is True:
                self.log.error("Message partition length error:: Expected {0} Current {1}".format(self.expectedpartitionlen,len(self.splitmsg[4])))
            #raise Exception("Message partition length error")
            self.valid = False    
        if len(self.splitmsg[5]) != self.expecteduserlen:
            #LA LONGITUD DE USUARIO NO ES VALIDA
            if self.loggerenabled is True:
                self.log.error("Message user length error:: Expected {0} Current {1}".format(self.expecteduserlen,len(self.splitmsg[5])))
            #raise Exception("Message user length error")
            self.valid = False
        if self.generatorallowed is True and self.splitmsg[6] == "0":
            self._checksumgenerator()
        if self.checksumallowed is True:
            self._checksum()
            if self.retchecksum != 0 :
                #EL CHECKSUM ES INCORRECTO
                if self.loggerenabled is True: 
                    self.log.error("Wrong calculated checksum:: Expected 0 Current {}".format(self.retchecksum))
                #raise Exception("Wrong checksum")
                self.valid = False
    def processmessage(self, incmessage: str, separator :str = None ):
        """Proccess an incoming CID message.

        Args:
            incmessage (str): Incomming Contact ID message
                            Format: AAAA TT QEEE PP UUU S
                                    -> AAAA: account number (0-9, B-F)
                                    -> TT: Message type (CID = 18)
                                    -> Q: Qualifier  1 - New event / 3 - restoral / 6 - Previously reported condition still present
                                    -> EEE: Event code (3 Hex digits 0-9,B-F)
                                    -> PP: Group or Partition number (2 Hex digits 0-9, B-F). 00 indicate no specific group
                                    -> UUU: Zone number (Event reports) or User# (Open / Close reports ) (3 Hex digits 0-9,B-F ). 000 indicate no specific zone or user
                                    -> S: 1 Digit Hex checksum calculated such that: (Sum of all message digits + S) % 15
            separator (str, optional): Used to split string into parameters. Defaults to ' '.

        Returns:
            (dict | None) : If validation is true, returns a dictionary cointaining valid parameters, otherwhise returns None
        """
        self.message = incmessage.upper()
        self.retchecksum = None
        
        if separator is not None:
            self.allowedchar.remove(self.separator)
            self.separator = separator.upper()
            self.allowedchar.add(self.separator)
            self.expectedlength = 16 + len(separator)*5
        
        
        self._validatemessage()
        
        if self.valid is True:
            if self.loggerenabled is True:
                self.log.info("Validated message {}".format(str(self.splitmsg)))
            retdict = {
                'AccountNumber' : self.splitmsg[0],
                "MessageType" : self.splitmsg[1],
                "Qualifier" : self.splitmsg[2],
                "EventCode" : self.splitmsg[3],
                "PartitionNumber" : self.splitmsg[4],
                "ZoneUserNumber" : self.splitmsg[5],
                "Checksum" : self.splitmsg[6]
                }
            return retdict
        else:
            return None

if __name__ == "__main__":
    alogger = logging.getLogger("CID")
    formatter = logging.Formatter('%(module)s : %(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    alogger.addHandler(handler)
    alogger.setLevel(logging.DEBUG)
    
    ex = contact_id(allowchecksum= True, checksumgenerator= False, separator= " ", loggername= "CID")
    print("TEST -> OK MSG:")
    ret = ex.processmessage(incmessage= "1111 18 1401 01 001 E")
    print(str(ret))

    print("TEST -> Checksum generator:")
    ret = ex.processmessage(incmessage= "1111 18 1401 01 001 0")
    print(str(ret))

    print("TEST -> Wrong checksum:")
    ret = ex.processmessage(incmessage= "1111 18 1401 01 001 2")
    print(str(ret))

    print("TEST -> Wrong msg length, wrong Zone/user length:")
    ret = ex.processmessage(incmessage= "1111 18 1401 01 01 0")
    print(str(ret))

    print("TEST -> Wrong msg length, Wrong partition length")
    ret = ex.processmessage(incmessage= "1111 18 1401 1 001 0")
    print(str(ret))

    print("TEST -> Wrong msg length,  wrong event length")
    ret = ex.processmessage(incmessage= "1111 18 140 01 001 0")
    print(str(ret))

    print("TEST -> Wrong msg length, Wrong qualifier, wrong event length")
    ret = ex.processmessage(incmessage= "1111 18 401 01 001 0")
    print(str(ret))

    print("TEST -> Wrong msg length,  wrong msg type")
    ret = ex.processmessage(incmessage= "1111 8 1401 01 001 0")
    print(str(ret))

    print("TEST -> Wrong msg length,  wrong account length")
    ret = ex.processmessage(incmessage= "111 18 1401 01 001 0")
    print(str(ret))
    
    print("TEST -> Invalid characters")
    ret = ex.processmessage(incmessage= "rr11 18 1401 01 001 0")
    print(str(ret))
    
    print("TEST -> Split error")
    ret = ex.processmessage(incmessage= "1111aa18aa1602aa01aa001aab")
    print(str(ret))