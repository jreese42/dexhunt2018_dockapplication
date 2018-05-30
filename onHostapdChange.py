import sys
import peewee
from networkmodel import DeviceModel

db = peewee.SqliteDatabase('dexhunt.db')

print(sys.argv)

if sys.argv[2] == "AP-STA-CONNECTED":
    with db.atomic():
        try:
            device = DeviceModel.get(DeviceModel.macaddr == sys.argv[3])
            device.ipaddr = sys.argv[1]
            device.is_connected = True
            numModified = device.save()
            print("Updated DeviceModel with MAC({}) to IP({}), affecting {} rows".format(sys.argv[3],sys.argv[1],numModified))
        except DeviceModel.DoesNotExist:
            device = DeviceModel.create(macaddr=sys.argv[3], ipaddr=sys.argv[1], rfidtoken="", is_connected=True)
            print("Created New DeviceModel with MAC({}), IP({})".format(sys.argv[3],sys.argv[1]))

elif sys.argv[2] == "AP-STA-DISCONNECTED":
    with db.atomic():
        try:
            device = DeviceModel.get(DeviceModel.macaddr == sys.argv[3])
            device.is_connected = False
            numModified = device.save()
            print("Disconnected DeviceModel with MAC({}) IP({}), affecting {} rows".format(sys.argv[3],sys.argv[1],numModified))
        except DeviceModel.DoesNotExist:
            print("Unknown DeviceModel Disconnected MAC({}) IP({})".format(sys.argv[3],sys.argv[1]))