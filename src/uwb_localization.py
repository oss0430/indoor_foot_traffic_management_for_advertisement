from ctypes import byref
from bluepy import btle
import binascii
import struct
import time

def localization():

    ble_connect_flag = False

    # https://ianharvey.github.io/bluepy-doc/peripheral.html
    # The Peripheral class
    for i in range(100):
        print("Connecting...")
        try:
            dev = btle.Peripheral('F4:F7:59:60:19:72')
            print("Connected")
            ble_connect_flag = True
            break
        except:
            time.sleep(0.1)
            
    if ble_connect_flag is False:
        print("Failed to connect to peripheral")
        raise

    locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
    readdata = btle.UUID("003bbdf2-c634-4b3d-ab56-7ec889b89a37")
    locService = dev.getServiceByUUID(locuuid)
    n_id = [0]*4
    n_dis = [0]*4

    try:
        ch = locService.getCharacteristics(readdata)[0]
        print("ch : ")
        print(ch)
        if(ch.supportsRead()):
            while 1:
                val = binascii.b2a_hex(ch.read())
                x_pos = bytearray(ch.read()[1:5])
                y_pos = bytearray(ch.read()[5:9])
                z_pos = bytearray(ch.read()[9:13])
                
                x_pos = struct.unpack('<i', x_pos)[0]
                y_pos = struct.unpack('<i', y_pos)[0]
                z_pos = struct.unpack('<i', z_pos)[0]
                print('x=',(x_pos/1000), 'm   y=', (y_pos/1000), 'm   z=', (z_pos/1000), 'm')
                
                print(ch.read())
                if len(ch.read()) == 43:
                    for j in range(4):
                        n_id[j] = bytearray(ch.read()[j*7+15:j*7+17])
                        n_dis[j] = bytearray(ch.read()[17+j*7:21+j*7])
                        n_id[j] = hex(struct.unpack('<H', n_id[j])[0])
                        n_dis[j] = struct.unpack('<i', n_dis[j])[0]
                        print((n_id[j]), ':', (n_dis[j]/1000), '      ', end ='')
                    print('\n')
                    print('\n')
                
                    
    finally:
        dev.disconnect()