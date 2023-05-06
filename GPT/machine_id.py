import datetime
import logging
import os
import platform

import uuid

def get_machine_unique_identifier():
    if platform.system() == "Windows":
        # Use the Windows Management Instrumentation (WMI) interface
        import wmi
        wmi_obj = wmi.WMI()
        for interface in wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            mac_address = interface.MACAddress
            break
    else:
        for line in os.popen("ifconfig" if platform.system() != "Linux" else "ip link"):
            if "ether" in line or "HWaddr" in line:
                mac_address = line.split()[1]
                break

    # Create a UUID based on the MAC address and a namespace
    namespace = uuid.UUID("a9b8c7d6-e5f4-3210-9876-5a4b3c2d1e0f")
    if type(mac_address) != str:
        mac_address = str(datetime.datetime.now())
    logging.info(f"machine identifier: {mac_address}")
    machine_unique_id = uuid.uuid5(namespace, mac_address)

    return machine_unique_id

if __name__ == '__main__':
    unique_id = get_machine_unique_identifier()
    print(f"Unique Identifier for this machine: {unique_id}")
