from bluepy import btle
import binascii
import struct
import time

def device_setting():
    MAC_dict = {
        'DWCCB6' : 'ED:8F:E6:7D:0C:E0', 
        'DW1D02' : 'E1:AD:E3:0A:98:37', 
        'DW8797' : 'FB:C8:08:B9:DB:9F',
        'DWCF23' : 'C0:AF:50:DB:25:6F',
        'DW962E' : 'F4:F7:59:60:19:72'
    }
    MAC_array = ['ED:8F:E6:7D:0C:E0', 'E1:AD:E3:0A:98:37', 'FB:C8:08:B9:DB:9F'
                , 'C0:AF:50:DB:25:6F', 'F4:F7:59:60:19:72']

    pos_x = [0,0,100000,100000]
    pos_y = [0,50000,0,50000]
    pos_z = [0,0,0,0]

    count = 0
    for MAC in MAC_array:
        ble_connect_flag = False
        
        for i in range(100):
            print("Connected to " ,(MAC))
            try:
                dev = btle.Peripheral(MAC)
                print("Connected")
                ble_connect_flag = True
                break
            except:
                time.sleep(0.3)
        
        if ble_connect_flag is False:
            print("Failed to connect to peripheral ",(MAC))
            raise
        
        locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
        panuuid = btle.UUID("80f9d8bc-3bff-45bb-a181-2d6a37991208")
        opuuid = btle.UUID("3f0afd88-7770-46b0-b5e7-9fc099598964")
        posuuid = btle.UUID("f0f26c9b-2c8c-49ac-ab60-fe03def1b40c")
        
        locService = dev.getServiceByUUID(locuuid)
        
        # struct.pack(format, v1, v2, ...)
        # v1, v2, … 값을 포함하고 포맷 문자열 format에 따라 패킹 된 바이트열 객체를 반환합니다. 인자는 포맷이 요구하는 값과 정확히 일치해야 합니다.
        # H : unsigned short(C언어) -> 정수 (파이썬)
        if count == 0:
            opcode = struct.pack(">H", 0b1101110110000000)
            poscode = struct.pack("<iiib", pos_x[count], pos_y[count], pos_z[count],100)
        elif count == 4:
            opcode = struct.pack(">H", 0b0101110100100000)
        else:
            opcode = struct.pack(">H", 0b1101110100000000)
            poscode = struct.pack("<iiib",pos_x[count], pos_y[count], pos_z[count],100)
        
        print(poscode)
        try:
            if count != 4:
                ch = locService.getCharacteristics(opuuid)[0]
                dev.writeCharacteristic(ch.valHandle, opcode)
                print('s opcode : ', (opcode))
                ch1 = locService.getCharacteristics(posuuid)[0]
                dev.writeCharacteristic(ch1.valHandle, poscode) 
            else:
                ch = locService.getCharacteristics(opuuid)[0]
                dev.writeCharacteristic(ch.valHandle, opcode)
                print('s opcode : ', (opcode))
        finally:
            dev.disconnect()
            print((MAC), 'is disconnected')
        count = count +1
        
device_setting()