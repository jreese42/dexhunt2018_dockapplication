#!/usr/bin/env python
import sys
import peewee
from networkmodel import DeviceModel
import subprocess
from GameTime import CountdownClock

db = peewee.SqliteDatabase('/dexhunt.db')
gameTime = CountdownClock()

print(sys.argv)

if sys.argv[2] == "AP-STA-CONNECTED":
    with db.atomic():
        ip_address = subprocess.check_output("ip neighbor | grep \"{}\" | cut -d\" \" -f1".format(sys.argv[3]), shell=True)[:-1]
        try:
            device = DeviceModel.get(DeviceModel.macaddr == sys.argv[3])
            device.ipaddr = ip_address
            device.is_connected = True
            numModified = device.save()
            print("Updated DeviceModel with MAC({}) to IP({}), affecting {} rows".format(sys.argv[3],ip_address,numModified))
            device.setTimeRemaining(gameTime.remainingSeconds())
        except DeviceModel.DoesNotExist:
            device = DeviceModel.create(macaddr=sys.argv[3], ipaddr=ip_address, rfidtoken="", is_connected=True)
            print("Created New DeviceModel with MAC({})".format(sys.argv[3]))
            device.setTimeRemaining(gameTime.remainingSeconds())

elif sys.argv[2] == "AP-STA-DISCONNECTED":
    with db.atomic():
        try:
            device = DeviceModel.get(DeviceModel.macaddr == sys.argv[3])
            device.is_connected = False
            numModified = device.save()
            print("Disconnected DeviceModel with MAC({}), affecting {} rows".format(sys.argv[3],numModified))
        except DeviceModel.DoesNotExist:
            print("Unknown DeviceModel Disconnected MAC({})".format(sys.argv[3]))
