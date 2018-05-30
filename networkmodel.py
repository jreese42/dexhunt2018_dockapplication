import peewee
import requests

db = peewee.SqliteDatabase('/dexhunt.db')

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class DeviceDatabase:
    def __init__(this):
        db.connect()
        db.create_tables[DeviceModel]

    def getDevice(this, rfidtoken):
        pass
    
class BaseModel(peewee.Model):
    class Meta:
        database = db

class DeviceModel(BaseModel):
    macaddr = peewee.CharField()
    ipaddr = peewee.CharField()
    rfidtoken = peewee.CharField()
    is_connected = peewee.BooleanField()

    class Meta:
        database = db

    def setGameStatus(this, ledNum, bool_value):
        enabledVal = "0"
        if bool_value:
            enabledVal = "1"
    
        if this.is_connected:
            try:
                r = requests.post("http://" + this.ipaddr + "/setEnabled", data={'ledNum': str(ledNum), 'enabled': enabledVal}, timeout=2)
                print(r.status_code, r.reason)
                print(r.text[:300])
            except:
                print("Connection Error")

    def setRGB(this, ledNum, r, g, b):
        print("http://" + this.ipaddr + "/setRGB")
        r = clamp(r, 0, 255)
        g = clamp(g, 0, 255)
        b = clamp(b, 0, 255)

        if this.is_connected:
            try:
                r = requests.post("http://" + this.ipaddr + "/setRGB", data={'ledNum': str(ledNum), 'r': str(r), 'g': str(g), 'b': str(b)}, timeout=2)
                print(r.status_code, r.reason)
                print(r.text[:300])
            except:
                print("Connection Error")

def create_tables():
    with db:
        db.create_tables([DeviceModel])

    
