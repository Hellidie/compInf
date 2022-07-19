import socket
from wmi import WMI
from requests import post
from json import dumps
from os import environ
from dataclasses import dataclass
from getmac import get_mac_address as gma

@dataclass
class recieve_info():
    
    def get_Username():
        return environ.get('USERNAME')
    
    def get_NamePC():
        namePC = socket.gethostname()
        return namePC

    def get_Mac():
        macaddr = gma()
        return macaddr

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

    def get_HardwareInfo():
        computer = WMI()
        proc_info = computer.Win32_Processor()[0]
        mBoard_Info = computer.Win32_BaseBoard()[0].Product
        os_info = computer.Win32_OperatingSystem()[0]
        system_ram = float(os_info.TotalVisibleMemorySize) / 1048576
        system_ram = int(system_ram * 100) / 100
        gpu_info = computer.Win32_VideoController()[0]
        [system_storage] = computer.Win32_DiskDrive(Index=0)
        return {'Processor' : proc_info.Name, 'Motherboard' : mBoard_Info, 'RAM' : str(system_ram) + 'GB', \
            'GPU' : gpu_info.Name, 'StorageModel' :  system_storage.Model, \
            'StorageSize' : str(int(int(system_storage.Size) / 1024**3)) + 'GB'}


hardwareReturn = recieve_info.get_HardwareInfo()
params = {'CurrentUsername' : recieve_info.get_Username(), 'Name' : recieve_info.get_NamePC(), 'IPadress' : recieve_info.get_IP(),
            'MacAdress' : recieve_info.get_Mac()}
params.update(hardwareReturn)

json_params = dumps(params)
url = 'http://portal.cso.com/compinfo'
resp = post(url, data = json_params)

if resp.ok:
   exit()
