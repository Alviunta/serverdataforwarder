import sys, traceback
import logging, logging.config
sys.path.append('./lib')
sys.path.append('./config')
from dc09_spt import dc09_spt as dc09
from contact_id import contact_id as contactid
from paho.mqtt import client as mqtt
from config.config import settings, LOGGING_CONFIG
from chirpstack_api.as_pb import integration
from google.protobuf.json_format import Parse

#MQTT FUNC

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            logger_MQTT.error("Failed to connect, return code %d \n", rc)
    def on_message_up(client, userdata, msg):
        #Contains the data and meta-data for an uplink application payload.
        up_msg= unmarshal(msg.payload, integration.UplinkEvent())
        logger_MQTT.info("Uplink Event:: App: {0}[{1}] :: Device: {2}[{3}] :: Data {4}".format(up_msg.application_name, up_msg.application_id, up_msg.device_name, up_msg.dev_eui.hex(), up_msg.data.hex()))

        processed_message = cid.processmessage(up_msg.data.hex())
        if processed_message is None:
            logger_CID.error("Error processing CID message {}".format(up_msg.data.hex())) 
        else:

            try:
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
                logger_SIA.critical("Exception type : %s Exception message : %s Stack Trace %s" % (ex_type.__name__, ex_value, stack_trace))
            else:
                logger_SIA.info("SIA msg sended:: Origin : {0} Msg: {1}".format(msg.topic, str(processed_message)))        

        del processed_message
    def on_message_status(client, userdata, msg):
        #Event for battery and margin status received from devices.
        status_msg= unmarshal(msg.payload, integration.StatusEvent())
        logger_MQTT.info("Status Event :: App: {0}[{1}] :: Device: {2}[{3}] :: Status: margin {4}dB - Ext. power source {5} - Bat. Level {6}".format(status_msg.application_name, status_msg.application_id, status_msg.device_name, status_msg.dev_eui.hex(), status_msg.margin, status_msg.external_power_source, status_msg.battery_level))
    def on_message_join(client, userdata, msg):
        #Event published when a device joins the network. Please note that this is sent after the first received uplink (data) frame.
        join_msg= unmarshal(msg.payload, integration.JoinEvent())
        logger_MQTT.info("Join Event :: App: {0}[{1}] :: Device: {2}[{3}] :: Gateway: {4}".format(join_msg.application_name, join_msg.application_id, join_msg.device_name, join_msg.dev_eui.hex(), join_msg.rx_info[0].gateway_id.hex()))
        
    def on_message_ack(client, userdata, msg):
        #Event published on downlink frame acknowledgements.
        ack_msg= unmarshal(msg.payload, integration.AckEvent())
        logger_MQTT.info("Ack Event :: App: {0}[{1}] :: Device: {2}[{3}] :: ACK: {4}".format(ack_msg.application_name, ack_msg.application_id, ack_msg.device_name, ack_msg.dev_eui.hex(), ack_msg.acknowledged))
    def on_message_txack(client, userdata, msg):
        #Event published when a downlink frame has been acknowledged by the gateway for transmission.
        txack_msg= unmarshal(msg.payload, integration.TxAckEvent())
        logger_MQTT.info("TxAck Event :: App: {0}[{1}] :: Device: {2}[{3}] :: Gateway: {4} :: Ack: Downlink Frame Counter {5}".format(txack_msg.application_name, txack_msg.application_id, txack_msg.device_name, txack_msg.dev_eui.hex(), txack_msg.tx_info[0].gateway_id.hex(), txack_msg.f_cnt))
    def on_message_error(client, userdata, msg):
        #Event published in case of an error related to payload scheduling or handling. E.g. in case when a payload could not be scheduled as it exceeds the maximum payload-size.
        error_msg= unmarshal(msg.payload, integration.ErrorEvent())
        logger_MQTT.error("Error Event :: App: {0}[{1}] :: Device {2}[{3}] :: Error: {4}".format(error_msg.application_name, error_msg.application_id, error_msg.device_name, error_msg.dev_eui.hex(), error_msg.error))
    def on_message(client, userdata, msg):
        #Default message, no event-topic match. ???????
        logger_MQTT.warning("No event-topic match :: Topic: {0} :: Payload: {1} :: Qos: {2}".format(msg.topic, msg.payload, msg.qos))
    def unmarshal(body, pl):
        if MQTTconfig.attributes.marshaler:
            return Parse(body,pl)
        pl.ParseFromString(body)
        return pl

    def configure_client(client : mqtt):
        client.message_callback_add("application/+/device/+/event/up",on_message_up)
        client.message_callback_add("application/+/device/+/event/status",on_message_status)
        client.message_callback_add("application/+/device/+/event/join",on_message_join)
        client.message_callback_add("application/+/device/+/event/ack",on_message_ack)
        client.message_callback_add("application/+/device/+/event/txack",on_message_txack)
        client.message_callback_add("application/+/device/+/event/error",on_message_error)
        client.on_message = on_message
    
    
    client = mqtt.Client(client_id ="")
    client.enable_logger(logger_MQTT)
    client.username_pw_set(MQTTconfig.credentials.username, MQTTconfig.credentials.password)
    client.on_connect = on_connect
    client.connect(MQTTconfig.endpoint.address,MQTTconfig.endpoint.port)
    client.subscribe(MQTTconfig.attributes.topic)
    configure_client(client)
    return client


def callback_siaspt(itype, idata):
    logger_SIA.info("Callback type " + itype + " data :"+ str(idata))

def setup_siaspt():
    spt = dc09.dc09_spt(DC09config.attributes.account)
    spt.set_callback(callback_siaspt)
    spt.set_path(DC09config.endpoint.mb, DC09config.endpoint.ps, DC09config.endpoint.address, DC09config.endpoint.port, account = DC09config.attributes.account, receiver = DC09config.attributes.receiver, line = DC09config.attributes.line, type = DC09config.endpoint.type)
    spt.start_poll(DC09config.attributes.heartbeat, retry_delay= 10, ok_msg= {'code' : "YK"}, fail_msg= {'code' : 'YS'})
    spt.send_msg('SIA', {'code' : 'RR'})
    spt.start_routine([{'interval': DC09config.attributes.heartbeat,  'time':  'now', 'type': 'SIA-DCS',  'code': DC09config.attributes.pollmsg}])   
    return spt


def startmain():
    
    global CIDconfig, MQTTconfig, DC09config
    CIDconfig = settings.get("CID")
    MQTTconfig = settings.get("MQTT")
    DC09config= settings.get("DC09")

    logging.config.dictConfig(LOGGING_CONFIG)
    global logger_CID, logger_MQTT, logger_SIA 
    logger_CID = logging.getLogger('contact_id')
    logger_MQTT = logging.getLogger('mqtt')
    logger_SIA = logging.getLogger('dc09_spt')

    global spt
    spt = setup_siaspt()
    
    global cid
    cid = contactid(allowchecksum= CIDconfig.attributes.enablecheksumvalidation, checksumgenerator= CIDconfig.attributes.enablecheksumgenerator, loggername= 'contact_id', separator= CIDconfig.attributes.separator)

    client = connect_mqtt()
    client.loop_start()

if __name__ == "__main__":
    startmain()