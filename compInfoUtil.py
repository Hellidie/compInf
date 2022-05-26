import socket
import uuid
import wmi
import re
import requests
import json
import os
from dataclasses import dataclass

@dataclass
class recieve_info():
    
    def get_Username():
        return os.environ.get('USERNAME')
    
    def get_NamePC():
        namePC = socket.gethostname()
        return namePC

    def get_Mac():
        macAddr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))         # получаем mac-адресс
        return macAddr

    def get_IP():
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            userIP = st.getsockname()[0]
        except Exception:
            userIP = '127.0.0.1'
        finally:
            st.close()
        return userIP

    def get_ProcInfo():
        computer = wmi.WMI()
        proc_info = computer.Win32_Processor()[0]
        return proc_info.Name

    def get_MotherBoard():
        computer = wmi.WMI()
        mBoard_Info = computer.Win32_BaseBoard()[0].Model
        return mBoard_Info
    
    def get_SysRamInfo():
        computer = wmi.WMI()
        os_info = computer.Win32_OperatingSystem()[0]
        system_ram = float(os_info.TotalVisibleMemorySize) / 1048576
        system_ram = int(system_ram * 100) / 100
        return system_ram

    def get_GPUinfo():
        computer = wmi.WMI()
        gpu_info = computer.Win32_VideoController()[0]
        return gpu_info.Name

    def get_SysStorModel():
        computer = wmi.WMI()
        [system_storage] = computer.Win32_DiskDrive(Index=0)
        return system_storage.Model

    def get_SysMemSize():
        computer = wmi.WMI()
        [system_storage] = computer.Win32_DiskDrive(Index=0)
        return int(int(system_storage.size) / 1024**3)

params = {'CurrentUsername' : recieve_info.get_Username(), 'Name' : recieve_info.get_NamePC(), 'IP-adress' : recieve_info.get_IP(),
            'Mac-adress' : recieve_info.get_Mac(), 'Processor' : recieve_info.get_ProcInfo(), 'Motherboard' : recieve_info.get_MotherBoard(),
            'RAM' : str(recieve_info.get_SysRamInfo()) + 'GB', 'GPU' : recieve_info.get_GPUinfo(),
            'StorageModel' : recieve_info.get_SysStorModel(), 'StorageSize' : str(recieve_info.get_SysMemSize()) + 'GB'}

# json_params = json.dumps(params)

print(params)

# url = 'http://portal.cso.com/compinfo'
# resp = requests.post(url, data = json_params)

# if resp.ok:
#    exit()
