import sys
sys.path.append('./lib')
import traceback
import logging
import contact_id as contactid
from dc09_spt import dc09_spt as dc09

def callback(itype, idata):
    print("Callback type " + itype + " data :")
    print(idata)

def connectspt(sptaccount):
#Use config file!
    spt = dc09.dc09_spt(sptaccount)
    spt.set_callback(callback)
    spt.set_path("main", "primary", "172.31.224.218",  62000 , account = sptaccount, receiver = 0, line = 0, type = 'udp')
    spt.start_poll(600, retry_delay= 10, ok_msg= {'code' : "YK"}, fail_msg= {'code' : 'YS'})
    spt.send_msg('SIA', {'code' : 'RR'})
    spt.start_routine([{'interval':  600,  'time':  'now', 'type': 'SIA-DCS',  'code':  'RP'}])   
    return spt

#LOGGER CONFIGURATION
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    #Use config file!
    formatter = logging.Formatter('%(module)-12s : %(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def mainFunc():
    logger_CID = setup_logger('CID_LOG', 'log/logfile_CID.log', logging.DEBUG)
    logger_SIA = setup_logger(__name__, 'log/logfile_SIA.log', logging.DEBUG)
    spt = None
    while True:
        print("Ingrese CID formato: AAAA TT QEEE PP UUU S")
        recived_CID = input()
        if recived_CID == "State" and spt.state()['main primary path ok'] is False:
            print(spt.state())
        elif recived_CID == "exit":
            exit()
        try:
            proceced_message = contactid.process_incomming_CID(recived_CID)
        except Exception as ex:
            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()
            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)
            # Format stacktrace
            stack_trace = list()
            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
            logger_CID.exception("Exception type : %s Exception message : %s Stack Trace %s" % (ex_type.__name__, ex_value, stack_trace))
            #logger_CID.exception(ex)
        else:
            try:
                if spt is None:
                    spt = connectspt('FFFF')
                elif spt.state()['main primary path ok'] is False:
                    spt = connectspt('FFFF')
                spt.send_msg('ADM-CID', {'account':  proceced_message["AccountNumber"], 'q': proceced_message["Qualifier"], 'code': proceced_message["EventCode"], 'area':proceced_message["PartitionNumber"], 'zone': proceced_message["ZoneUserNumber"]}) 
            except Exception as ex:
                # Get current system exception
                ex_type, ex_value, ex_traceback = sys.exc_info()
                # Extract unformatter stack traces as tuples
                trace_back = traceback.extract_tb(ex_traceback)
                # Format stacktrace
                stack_trace = list()
                for trace in trace_back:
                    stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
                logger_SIA.exception("Exception type : %s Exception message : %s Stack Trace %s" % (ex_type.__name__, ex_value, stack_trace))
                #logger_SIA.exception(ex)   
            del proceced_message

if __name__ == "__main__":
    mainFunc()