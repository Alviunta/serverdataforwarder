import sys
import traceback
import logging
import logging.handlers
sys.path.append('./lib')
import contact_id as contactid
from dc09_spt import dc09_spt as dc09
sys.path.append('./config')
from config.config import settings

def callback(itype, idata):
    print("Callback type " + itype + " data :")
    print(idata)

def setup_siaspt():
    spt = dc09.dc09_spt(DC09config['attributes']['account'])
    #spt.set_callback(callback)
    spt.set_path(DC09config['endpoint']['mb'], DC09config['endpoint']['ps'], DC09config['endpoint']['address'], DC09config['endpoint']['port'], account = DC09config['attributes']['account'], receiver = DC09config['attributes']['receiver'], line = DC09config['attributes']['line'], type = DC09config['endpoint']['type'])
    spt.start_poll(DC09config['attributes']['heartbeat'], retry_delay= 10, ok_msg= {'code' : "YK"}, fail_msg= {'code' : 'YS'})
    spt.send_msg('SIA', {'code' : 'RR'})
    spt.start_routine([{'interval': DC09config['attributes']['heartbeat'],  'time':  'now', 'type': 'SIA-DCS',  'code': DC09config['attributes']['pollmsg']}])   
    return spt

#LOGGER CONFIGURATION
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    formatter = logging.Formatter('%(module)-12s : %(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
    handler = logging.FileHandler(log_file)        
    #handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount= 7, atTime= datetime.time(hour=0, minute=0))
    #handler = logging.handlers.SysLogHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def initialize_config():
    global MQTTconfig
    MQTTconfig = settings.get("MQTT")
    global DC09config
    DC09config= settings.get("DC09")
    global logger_CID 
    logger_CID = setup_logger('CID_LOG', 'log/logfile_CID.log', logging.DEBUG)
    global logger_SIA 
    logger_SIA = setup_logger('SIA_LOG', 'log/logfile_SIA.log', logging.DEBUG)
    global spt 
    spt = None
    spt = setup_siaspt()

def mainFunc():
    while True:
        print("Ingrese CID formato: AAAA TT QEEE PP UUU S")
        recived_CID = input()
        if recived_CID == "State":
            print(spt.state())
        elif recived_CID == "exit":
            exit()
        elif recived_CID == "logger":
            for k,v in  logging.Logger.manager.loggerDict.items()  :
                print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) ) 
                if not isinstance(v, logging.PlaceHolder):
                    for h in v.handlers:
                        print('     +++',str(h.__class__)[8:-2] )
        try:
            processed_message = contactid.process_incomming_CID(recived_CID)
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
                    spt = setup_siaspt()
                elif spt.state()['main primary path ok'] is False:
                    del spt
                    spt = setup_siaspt()
                spt.send_msg('ADM-CID', {'account':  processed_message["AccountNumber"], 'q': processed_message["Qualifier"], 'code': processed_message["EventCode"], 'area':processed_message["PartitionNumber"], 'zone': processed_message["ZoneUserNumber"]}) 
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
            del processed_message

if __name__ == "__main__":
    mainFunc()
    