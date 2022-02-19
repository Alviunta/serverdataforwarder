
from dynaconf import Dynaconf, Validator
"""
En este archivo se importa la configuracion contenida en los archivos .toml

Ademas se hacen validaciones para evitar errores.
NO MODIFICAR ESTE ARCHIVO, CAMBIAR VALORES EN ARCHIVOS .toml
"""
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
    validators = [
        #MQTT VALIDATORS
        Validator('MQTT', must_exist=True),
        #   Endpoint
        Validator('MQTT.endpoint', must_exist=True),
        Validator('MQTT.endpoint.address',is_type_of = str, default= "127.0.0.1"),
        Validator('MQTT.endpoint.port', is_type_of = int, lte = 65535, default = 1883),
        #   Logger
        Validator('MQTT.logger', must_exist = True),
        Validator('MQTT.logger.name', is_type_of = str, default = "MQTT"),
        Validator('MQTT.logger.level', is_in = (10, 20, 30, 40, 50)),
        Validator('MQTT.logger.output', is_in =("FILE", "CONSOLE")),
        Validator('MQTT.logger.filename', is_type_of= str),
        #   Credentials
        Validator('MQTT.credentials', must_exist = True), 
        Validator('MQTT.credentials.username', is_type_of = str, must_exist = True),
        Validator('MQTT.credentials.password', is_type_of = str, must_exist = True),
        #   Attributes
        Validator('MQTT.attributes', must_exist = True),
        Validator('MQTT.attributes.qos', is_type_of = int, gte = 0, lte = 3),
        #DC09 VALIDATORS
        Validator('DC09', must_exist=True),
        #   Endpoint
        Validator('DC09.endpoint.address', is_type_of = str, default="127.0.0.1"),
        Validator('DC09.endpoint.port', is_type_of = int, lte = 65535, default = 62000),
        Validator('DC09.endpoint.type', is_in = ("udp", "UDP", "tcp", "TCP"), default= "UDP"),
        Validator('DC09.endpoint.mb', is_type_of = str, is_in = ("main", "back-up")),
        Validator('Dc09.endpoint.ps', is_type_of = str, is_in = ("primary", "secondary")),
        #   Attributes
        Validator('DC09.attributes.account', must_exist = True, is_type_of = str),
        Validator('DC09.attributes.line', must_exist = True, is_type_of = int),
        Validator('DC09.attributes.receiver', must_exist = True, is_type_of = int),
        #   Encryption
        Validator('DC09.encryption', must_exist= True),
        Validator('DC09.encryption.enable', is_type_of = bool),
        Validator('DC09.encryption.key', is_type_of = str)
    ]
)
