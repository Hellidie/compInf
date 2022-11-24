#encoding: utf-8
import socket
from wmi import WMI
from requests import post
from json import dumps
from os import environ
from dataclasses import dataclass
from getmac import get_mac_address as gma
from loguru import logger

logger.add("C:\Windows\Temp\debug.log", format="{time} {level} {message}", level="DEBUG")

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

    def get_HDI():
        computer = WMI()
        for physical_disk in computer.Win32_DiskDrive(Index=0):
            diskDrive_0 = {'StorageModel' : physical_disk.caption, 'StorageSize' : str(int(int(physical_disk.Size) / 1024**3)) + 'GB'}
        if computer.Win32_DiskDrive(Index=1):
            for physical_disk1 in computer.Win32_DiskDrive(Index=1):
                diskDrive_1 = {'StorageModel' : physical_disk1.caption, 'StorageSize' : str(int(int(physical_disk1.Size) / 1024**3)) + 'GB'}
            return {"Disks":[diskDrive_0, diskDrive_1]}
        if computer.Win32_DiskDrive(Index=2):
            for physical_disk2 in computer.Win32_DiskDrive(Index=2):
                diskDrive_2 = {'StorageModel' : physical_disk2.caption, 'StorageSize' : str(int(int(physical_disk2.Size) / 1024**3)) + 'GB'}
            return {"Disks":[diskDrive_0, diskDrive_1, diskDrive_2]}
        else:
            return {"Disks":[diskDrive_0]}

    def get_HardwareInfo():
        computer = WMI()
        proc_info = computer.Win32_Processor()[0]
        mBoard_Info = computer.Win32_BaseBoard()[0].Product
        os_info = computer.Win32_OperatingSystem()[0]
        system_ram = float(os_info.TotalVisibleMemorySize) / 1048576
        system_ram = int(system_ram * 100) / 100
        gpu_info = computer.Win32_VideoController()[0]
        return {'Processor' : proc_info.Name, 'Motherboard' : mBoard_Info, 'RAM' : str(system_ram) + 'GB', \
            'GPU' : gpu_info.Name}

@logger.catch
def main():
    hardwareReturn = recieve_info.get_HardwareInfo()
    DiskDrives = recieve_info.get_HDI()
    params = {'CurrentUsername' : recieve_info.get_Username(), 'Name' : recieve_info.get_NamePC(), 'IPadress' : recieve_info.get_IP(),
            'MacAdress' : recieve_info.get_Mac()}
    params.update(hardwareReturn)
    params.update(DiskDrives)

    json_params = dumps(params)
    print(json_params)
    url = ''
    resp = post(url, data = json_params)

    if resp.ok:
        exit()

main()
