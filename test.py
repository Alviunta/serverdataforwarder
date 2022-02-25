import sys
sys.path.append('./config')

from config.config import settings, LOGGING_CONFIG

import logging, logging.config

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