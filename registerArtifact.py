#!/usr/bin/env python3

import GameManager
from networkmodel import DeviceModel
from RFIDTracker import RFIDTracker

from random import randint
import random
import os
import sys



def main():
    rfidTracker = RFIDTracker()
    input("Ready. Turn on stone and wait for it to connect to the network (~20sec), then press any key.")
    try:
        devicecount = DeviceModel.select.where(is_connected = True, rfidtoken = "").count()
        if devicecount > 1:
            print("Found multiple connected devices. Quitting without associating.")
            sys.exit(1)
        elif devicecount is 1:
            device = DeviceModel.get(is_connected = True, rfidtoken = "")
            print("Found device. Scan RFID Tag to associate.")
            while not rfidTracker.rfidTagIsActive():
                pass
            device.rfidtoken = rfidTracker.getActiveUid()
            numModified = device.save()
            print("Device associated. Modified " + str(numModified) + " rows, \tMAC=" + str(device.macaddr) + "\tTOKEN=" + str(device.rfidtoken))
            sys.exit(0)
        
    except DeviceModel.DoesNotExist:
        #TODO: Deal with device not found
        print("Active Device not found")

    sys.exit(1)

        

if __name__=="__main__":
    main()
