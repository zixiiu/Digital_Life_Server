import datetime
import logging
import os
import platform

import uuid


def get_machine_unique_identifier():
    if platform.system() == "Windows":
        # 使用Windows Management Instrumentation (WMI) 接口
        import wmi
        wmi_obj = wmi.WMI()
        for interface in wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            mac_address = interface.MACAddress
            break
    else:
        # 使用ifconfig或ip link命令获取MAC地址
        for line in os.popen("ifconfig" if platform.system() != "Linux" else "ip link"):
            if "ether" in line or "HWaddr" in line:
                mac_address = line.split()[1]
                break

    # 根据MAC地址和命名空间创建UUID
    namespace = uuid.UUID("a9b8c7d6-e5f4-3210-9876-5a4b3c2d1e0f")
    if type(mac_address) != str:
        mac_address = str(datetime.datetime.now())
    logging.info(f"机器标识符: {mac_address}")
    machine_unique_id = uuid.uuid5(namespace, mac_address)

    return machine_unique_id


if __name__ == '__main__':
    unique_id = get_machine_unique_identifier()
    print(f"该机器的唯一标识符: {unique_id}")