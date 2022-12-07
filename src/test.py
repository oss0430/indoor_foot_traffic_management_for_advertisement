#from setting import Device_setting, Network_setting
import uwb_localization
import 

#Device_setting.device_setting()          # -> 시작할때 한번만 하기 (networkd 세팅은 no)
tem = uwb_localization.localization()
print(tem)
print(tem[0])
print(tem[1])
print(tem[2])


'''
(x= 0.027 m   y= -0.044 m   z= 0.121 m)                             (x= 0.028 m   y= 2.66 m   z= 0.036 m)
                                    DWCCB6 ---450mm * 6block--- DW1002
                                    |                                |
                                    |                                |
                                    |                                |
                                    |                                |
                                    |               |                |
                                              450mm * 10block
                                    |               |                |
                                    |                                |
                                    |                                |
                                    |                                |
                                    |                                |
                                    DW8797 ---450mm * 6block--- DWCF23
x= 4.533 m   y= 0.114 m   z= -0.152 m                               x= 4.461 m   y= 3.001 m   z= -0.082 m
'''

