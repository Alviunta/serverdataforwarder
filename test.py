import sys
sys.path.append('./config')
from config.config import settings, LOGGING_CONFIG
import logging, logging.config
from paho.mqtt import client as mqtt
from chirpstack_api.as_pb import integration
from google.protobuf.json_format import Parse

for key, value in settings.items() :
    print(key, value)
a = settings.get('MQTT')
print(a.get('credentials'))

print(a['credentials']['username'])
print(a.credentials.username)

logging.config.dictConfig(LOGGING_CONFIG)

for k,v in  logging.Logger.manager.loggerDict.items()  :
                print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) ) 
                if not isinstance(v, logging.PlaceHolder):
                    for h in v.handlers:
                        print('     +++',str(h.__class__)[8:-2] )
                        
log = logging.getLogger('CID')
log.debug('ASD')
log.info('def')
log.error('123')

loggers = list(LOGGING_CONFIG['loggers'].keys())
r =loggers.pop()
print(r)
print(loggers)
print(log.name)
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            logger_MQTT.error("Failed to connect, return code %d \n", rc)
    # Set connecting client ID
    client = mqtt.Client(client_id ="")
    client.username_pw_set(MQTTconfig.credentials.username, MQTTconfig.credentials.password)
    client.on_connect = on_connect
    client.connect(MQTTconfig.endpoint.address,MQTTconfig.endpoint.port)
    subscribe(client)

    return client
json_enabled = True
def unmarshal(body, pl):
    if json_enabled:
        return Parse(body, pl)
    pl.ParseFromString(body)
    return pl
def subscribe (client: mqtt):
    def on_message (client, userdata, msg):
        parsed_topic = msg.topic.split('/')

        print(parsed_topic)
        data = {
            "topic" : msg.topic,
            parsed_topic[0]: parsed_topic[1], 
            parsed_topic[2]: parsed_topic[3],
            parsed_topic[4]: parsed_topic[5],
            "payload_plain": msg.payload,
                
                }
        eventtype = data.get('event')
        if eventtype == 'up': 
            #Contains the data and meta-data for an uplink application payload.
            print("UP")
            up = unmarshal(msg.payload, integration.UplinkEvent())
            print("Uplink received from: %s with payload: %s" % (up.dev_eui.hex(), up.data.hex()))
            print("Dev_eui: %s" % (up.dev_eui.hex()))
            print("Data: %s" % (up.data.hex()))
            print("App id: %d" % (up.application_id))
            print("frec: %d" % up.tx_info.frequency)
        elif eventtype == 'status':
            #Event for battery and margin status received from devices.
            print("status")
        elif eventtype == 'join':
            #Event published when a device joins the network. Please note that this is sent after the first received uplink (data) frame.
            print("join")
        elif eventtype == 'ack':
            #Event published on downlink frame acknowledgements.
            print("ack")
        elif eventtype == 'txack':
            #Event published when a downlink frame has been acknowledged by the gateway for transmission.
            print("txack")
        elif eventtype == 'error':
            #Event published in case of an error related to payload scheduling or handling. E.g. in case when a payload could not be scheduled as it exceeds the maximum payload-size.
            print("error")
        else:
            print("ALGO SALIO MAL")
        
        print(str(data))
        # data_in=json.loads(msg.payload)
        
        # print("~Datatype",type(data_in))
        # for key, value in data_in.items():
        #     print(f' -> {key}={value}')
    client.subscribe(MQTTconfig.attributes.topic)
    client.on_message = on_message
MQTTconfig = settings.get("MQTT")
logger_MQTT = logging.getLogger('mqtt')
client = connect_mqtt()
client.enable_logger(logger_MQTT)
def on_message_up(client, userdata, msg):
#Contains the data and meta-data for an uplink application payload.
    print("UP1234")
    up = unmarshal(msg.payload, integration.UplinkEvent())
    print("Uplink received from: %s with payload: %s" % (up.dev_eui.hex(), up.data.hex()))
    print("Dev_eui: %s" % (up.dev_eui.hex()))
    print("Data: %s" % (up.data.hex()))
    print("App id: %d" % (up.application_id))
    print("frec: %d" % up.tx_info.frequency)
client.message_callback_add("application/+/device/+/event/up",on_message_up)

# client.loop_start()
client.loop_forever()
