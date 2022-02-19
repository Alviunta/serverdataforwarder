import sys, traceback, logging, logging.handlers, datetime, json
sys.path.append('./lib')
sys.path.append('./config')
from dc09_spt import dc09_spt as dc09
import contact_id as contactid
from config.config import settings
from paho.mqtt import client as mqtt_client

def setup_logger(config):
    config = config.get('logger')
    formatter = logging.Formatter('%(module)s : %(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
    if (config['output'] == "CONSOLE"):
        handler = logging.StreamHandler()
    elif (config.output == "FILE"):
        if config.rotating is False:
            handler = logging.FileHandler("log/"+config.filename)
        else:
            handler = logging.handlers.TimedRotatingFileHandler("log/"+config.filename, when=config.rotatingset[0], backupCount=int(config.rotatingset[1]))
    else:
        handler = logging.NullHandler()
    logger = logging.getLogger(config.name)
    logger.setLevel(config.level)
    logger.addHandler(handler)
    
    return logger

def callback(itype, idata):
    logger_SIA.info("Callback type " + itype + " data :"+ idata)

def setup_siaspt():
    spt = dc09.dc09_spt(DC09config['attributes']['account'])
    spt.set_callback(callback)
    spt.set_path(DC09config['endpoint']['mb'], DC09config['endpoint']['ps'], DC09config['endpoint']['address'], DC09config['endpoint']['port'], account = DC09config['attributes']['account'], receiver = DC09config['attributes']['receiver'], line = DC09config['attributes']['line'], type = DC09config['endpoint']['type'])
    spt.start_poll(DC09config['attributes']['heartbeat'], retry_delay= 10, ok_msg= {'code' : "YK"}, fail_msg= {'code' : 'YS'})
    spt.send_msg('SIA', {'code' : 'RR'})
    spt.start_routine([{'interval': DC09config['attributes']['heartbeat'],  'time':  'now', 'type': 'SIA-DCS',  'code': DC09config['attributes']['pollmsg']}])   
    return spt

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            logger_MQTT.error("Failed to connect, return code %d \n", rc)
    # Set connecting client ID
    client = mqtt_client.Client(client_id ="")
    client.username_pw_set(MQTTconfig.credentials.username, MQTTconfig.credentials.password)
    client.on_connect = on_connect
    client.connect(MQTTconfig.endpoint.address,MQTTconfig.endpoint.port)
    subscribe(client)

    return client

def subscribe (client: mqtt_client):
    def on_message(client, userdata, msg):
        print("~Payload format ", type(msg.payload))
        #print("Received ",msg.payload)
        print("From ",msg.topic)
        data_in=json.loads(msg.payload)
        print("~Datatype",type(data_in))
        for key, value in data_in.items():
            print(f' -> {key}={value}')
    client.subscribe(MQTTconfig.attributes.topic)
    client.on_message = on_message
    
def initializeconfig():
    global CIDconfig
    CIDconfig = settings.get("CID")
    global logger_CID 
    logger_CID = setup_logger(CIDconfig)
    
    global MQTTconfig
    MQTTconfig = settings.get("MQTT")
    global logger_MQTT
    logger_MQTT = setup_logger(MQTTconfig)
    #client = connect_mqtt()
    #client.loop_forever()
    #client.enable_logger(logger_MQTT)
    
    global logger_SIA 
    global DC09config
    DC09config= settings.get("DC09")
    logger_SIA = setup_logger(DC09config)
    global spt
    spt = setup_siaspt()

def loopmain():
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
                if spt.state()['main primary path ok'] is False:
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
        
        del processed_message

if __name__ == "__main__":
    initializeconfig()
    loopmain()