
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
    validators = [
        #MQTT VALIDATORS ----------------------
        Validator('MQTT', must_exist=True),
        Validator('MQTT.endpoint', must_exist=True),
        Validator('MQTT.attributes', must_exist = True),
        Validator('MQTT.credentials', must_exist = True), 
        #   Endpoint
        Validator('MQTT.endpoint.address',is_type_of = str, default= "127.0.0.1"),
        Validator('MQTT.endpoint.port', is_type_of = int, lte = 65535, default = 1883),
        #   Credentials
        Validator('MQTT.credentials.username', is_type_of = str, must_exist = True),
        Validator('MQTT.credentials.password', is_type_of = str, must_exist = True),
        #   Attributes
        Validator('MQTT.attributes.qos', is_type_of = int, gte = 0, lte = 3),
        Validator('MQTT.attributes.marshaler', is_type_of = bool, must_exist = True),
        #CID VALIDATORS -----------------------
        Validator('CID', must_exist = True),
        Validator('CID.attributes', must_exist = True),
        #   Attributes
        Validator("CID.attributes.enablecheksumvalidation", is_type_of = bool, default = True),
        Validator('CID.attributes.enablecheksumgenerator', is_type_of = bool, default = False),
        Validator('CID.attributes.separator', is_type_of = str, default = " "),
        #DC09 VALIDATORS ----------------------
        Validator('DC09', must_exist=True),
        Validator('DC09.endpoint', must_exist=True),
        Validator('DC09.attributes', must_exist = True),
        #   Endpoint
        Validator('DC09.endpoint.address', is_type_of = str, default="127.0.0.1"),
        Validator('DC09.endpoint.port', is_type_of = int, lte = 65535, default = 2000),
        Validator('DC09.endpoint.type', is_in = ("udp", "UDP", "tcp", "TCP"), default= "UDP"),
        Validator('DC09.endpoint.mb', is_type_of = str, is_in = ("main", "back-up")),
        Validator('Dc09.endpoint.ps', is_type_of = str, is_in = ("primary", "secondary")),
        #   Attributes
        Validator('DC09.attributes.account', must_exist = True, is_type_of = str),
        Validator('DC09.attributes.line', must_exist = True, is_type_of = int),
        Validator('DC09.attributes.receiver', must_exist = True, is_type_of = int),
        Validator('DC09.attributes.heartbeat', must_exist = True, is_type_of = int),
        Validator('DC09.attributes.pollmsg', must_exist = True, is_type_of = str),
        #   Encryption
        Validator('DC09.encryption.enable', is_type_of = bool),
        Validator('DC09.encryption.key', is_type_of = str),
    ]
)

LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'WARNING',
            'handlers': ['debug_console_handler'],
        },
        'contact_id': {
            'level': 'INFO',
            'propagate': False,
            'handlers': [
                'debug_console_handler', 
                'info_timed_rotating_file_handler',
                'error_rotating_file_handler',
                'critical_file_handler',
                ],
        },
        'dc09_spt': {
            'level': 'INFO',
            'propagate': False,
            'handlers': [
                'debug_console_handler', 
                'info_timed_rotating_file_handler',
                'error_rotating_file_handler',
                'critical_file_handler',
                ],
        },
        'mqtt': {
            'level': 'INFO',
            'propagate': False,
            'handlers': [
                'debug_console_handler', 
                'info_timed_rotating_file_handler',
                'error_rotating_file_handler',
                'critical_file_handler',
                ],
        },
    },
    'handlers': {
        'debug_console_handler': {
            'level': 'DEBUG',
            'formatter': 'journal',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_timed_rotating_file_handler' : {  #Info logs to files up to one week old separated by day
            'level' : 'INFO',
            'formatter' : 'info',
            'class' : 'logging.handlers.TimedRotatingFileHandler',
            'filename' : './log/info.log',
            'when' : 'midnight',
            'backupCount' : 7,
            'utc' : True,
            
            },
        'error_rotating_file_handler': {    #Error logs to 10 fixed size files
            'level': 'ERROR',
            'formatter': 'error',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './log/error.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'critical_file_handler': {  #Critical logs to file
            'level': 'CRITICAL',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': './log/critical.log',
            'mode': 'a',
        },
        'null_handler': {
            'class': 'logging.NullHandler',
        },
    },
    'formatters': {
        'error': {
            'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
        },
        'debug': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s'
        },
        'info':{
            'format': '%(asctime)s-%(levelname)s-%(name)s::%(message)s'
        },
        'journal':{
            'format': '%(module)s|%(lineno)s %(message)s'
        },
    },
}
