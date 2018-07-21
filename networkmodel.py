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

    def getGameStatus(this):
        return "five"

    def setGameStatus(this, ledNum, bool_value):
        enabledVal = "0"
        if bool_value:
            enabledVal = "1"
    
        if this.is_connected:
            try:
                r = requests.post("http://" + this.ipaddr + "/setEnabled", data={'ledNum': str(ledNum), 'enabled': enabledVal}, timeout=10)
                print(r.status_code, r.reason)
                print(r.text[:300])
            except:
                print("Connection Error")

    def setGameTimer(self, secondsRemaining):
        raise NotImplementedError("Game Timer Control is not implemented in networkmodel.py")

    def setTimeRemaining(this, seconds):
        print("http://" + this.ipaddr + "/setTimeRemaining")

        if this.is_connected:
            try:
                r = requests.post("http://" + this.ipaddr + "/setTimeRemaining", data={'seconds': str(seconds)}, timeout=10)
                print(r.status_code, r.reason)
                print(r.text[:300])
            except:
                print("Connection Error")


    def getScore(this):
        print("http://" + this.ipaddr + "/getGameStatus")

        if this.is_connected:
            try:
                r = requests.post("http://" + this.ipaddr + "/getGameStatus", timeout=10)
                print(r.status_code, r.reason)
                print(r.text[:300])
                return int(r.text)
            except:
                print("Connection Error")

def create_tables():
    with db:
        db.create_tables([DeviceModel])

    
