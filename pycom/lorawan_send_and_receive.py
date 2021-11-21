from network import LoRa
import socket
import time
import pycom
import binascii
import BME280
import kpn_senml.cbor_encoder as cbor
from machine import I2C

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
#
mac = lora.mac()
print ('devEUI: ',  binascii.hexlify(mac))

# create an OTAA authentication parameters
app_eui = binascii.unhexlify(
     # '70B3D57ED0033AE3'.replace(' ',''))
    '0000000000000000'.replace(' ',''))

app_key = binascii.unhexlify(
     #'B0923EE49E056F29C1482EE5846FADF4'.replace(' ',''))  # TTN
     #'11223344556677881122334455667788'.replace(' ',''))   # Acklio
     '05111995110719980509200020112021'.replace(' ',''))   # Acklio personalized cause the order one doesnt worked
     # '11 00 22 00 33 00 44 00 55 00 66 00 77 00 88 00'.replace(' ',''))   # chirpstack

pycom.heartbeat(False)
pycom.rgbled(0x101010) # white

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key),  timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

pycom.rgbled(0x000000) # black

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setsockopt(socket.SOL_LORA,  socket.SO_CONFIRMED,  False)

NB_ELEMENT = 3
t_history = []

i2c = I2C(0, I2C.MASTER, baudrate=400000)
print (i2c.scan())

bme = BME280.BME280(i2c=i2c)

pycom.rgbled(0x000010) # blue
while True:
    t = int(bme.read_temperature()*100)

    # No more room to store value, send it.
    if len(t_history) == 0:
        t_history = [t]
    elif len(t_history) >= NB_ELEMENT:
        print ("send")
        pycom.rgbled(0x100000) # red
        s.setblocking(True)
        s.settimeout(10)
        try:
            s.send(cbor.dumps(t_history))
        except:
            print ('timeout in sending')
        pycom.rgbled(0x000010) # blue
        t_history = [t]
    else:
        t_history.append(t-prev)

    prev = t

    print (len(t_history), len(cbor.dumps(t_history)), t_history)

    time.sleep(10)
