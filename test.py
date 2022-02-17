import sys
sys.path.append('./config')
from config.config import settings

for key, value in settings.items() :
    print(key, value)
    
a = settings.get('MQTT')
print(a.get('credentials'))

print(a['credentials']['user'])