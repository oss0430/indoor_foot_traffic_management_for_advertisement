from bluepy import btle
import binascii
import struct
import time

def network_setting():

    MAC_array = ['ED:8F:E6:7D:0C:E0', 'E1:AD:E3:0A:98:37', 
                'FB:C8:08:B9:DB:9F','C0:AF:50:DB:25:6F', 'F4:F7:59:60:19:72']

    # ED:8F:E6:7D:0C:E0 DWCCB6
    # E1:AD:E3:0A:98:37 DW1D02
    # FB:C8:08:B9:DB:9F DW8797
    # C0:AF:50:DB:25:6F DWCF23
    # F4:F7:59:60:19:72 DW962E

    for MAC in MAC_array:
        ble_connect_flag = False
        for i in range(100):
            print("Connect to ", (MAC))
            try:
                dev = btle.Peripheral(MAC)
                print("Connected")
                ble_connect_flag = True
                break
            except:
                time.sleep(0.2)
                
        if ble_connect_flag is False:
            print("Failded to connect to peripheral", (MAC))
            raise
        
        locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
        panuuid = btle.UUID("80f9d8bc-3bff-45bb-a181-2d6a37991208")
        locService = dev.getServiceByUUID(locuuid)
        
        panid = struct.pack(">H", 101)
        
        try:
            ch = locService.getCharacteristics(panuuid)[0]
            dev.writeCharacteristic(28, panid)
            print((MAC), 's panid : ',(panid))
        finally:
            dev.disconnect()
            print((MAC), 'is disconnected')