import time

import snap7
import struct
import pandas as pd
import os
import glob
import threading
from datetime import datetime
from real_convert import real_convert

# todo connect to plc
client_dryer = snap7.client.Client()
client_dryer.connect("172.20.2.1", 0, 2)
status = client_dryer.get_connected()
print(status)
client_refiner = snap7.client.Client()
client_refiner.connect("172.20.2.5", 0, 3)
print(client_refiner.get_connected())
# dummy = null
dummy = "null"
# dryer
temp_2420_te9360_pc = 0
temp_2420_te1360_pc = 0
moisture_2425y0101 = 0
# refiner
v_04065hs2 = 0


def connect_dryer():
    global moisture_2425y0101, temp_2420_te9360_pc, temp_2420_te1360_pc, v_04065hs2

    while True:
        time.sleep(2)
        temp_2420_te9360_pc = real_convert(client_dryer.db_read(400, 1180, 4))
        temp_2420_te1360_pc = real_convert(client_dryer.db_read(400, 24, 4))
        moisture_2425y0101 = real_convert(client_dryer.db_read(400, 44, 4))

        v_04065hs2 = real_convert(client_refiner.db_read(60, 400, 4))


dryer_thread = threading.Thread(target=connect_dryer)
dryer_thread.start()
# data = client.db_read(100,4,2)
# print(data)
# dataint = int.from_bytes(data,"big")
# print(dataint)
# datafl = client.db_read(100,10,4)
#
# print("fl",datafl)
#
# real = struct.unpack('>f',struct.pack('4B',*datafl))[0]
# print(real)
#
# real2 = real_convert(datafl) # todo method convert byte to real
# print(real2)
# todo test excel
time.sleep(5)
date_current = datetime.today().strftime('%Y %m %d %H %M %S')
path_excel = './dataTest' + str(date_current) + '.xlsx'
df = pd.DataFrame({'Test': ['Test 1', 'Test 2', 'Test 3', 'Sample 4'],
                   'Data': [dummy, dummy, dummy, dummy],
                   'Dryer': [temp_2420_te9360_pc, moisture_2425y0101, temp_2420_te1360_pc, dummy],
                   'Refiner': [v_04065hs2, dummy, dummy, dummy]})
df.to_excel(path_excel)
# os.system('start "excel" "C:\\Users\\ASUTP\\PycharmProjects\\pythonProject\\%s"'%path_excel)


dir_file = glob.glob("C:\\Users\\ASUTP\\PycharmProjects\\pythonProject\\*.xlsx")
print(dir_file)
print(dir_file[0])
if len(dir_file) > 5:
    for i in range(5):
        os.remove(dir_file[i])
# todo terminal environment

