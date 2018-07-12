
#from RFIDTracker import RFIDTracker
import ntplib, time
#import RFIDTracker
from networkmodel import DeviceModel

class CountdownClock:
    def __init__(self):
        self.expiretime = 0
        self.synctime = 0

        try:
            ntpClient = ntplib.NTPClient()
            r = ntpClient.request('pool.ntp.org')
            self.synctime = r.tx_time
        except:
            try:
                ntpClient = ntplib.NTPClient()
                r = ntpClient.request('0.pool.ntp.org')
                self.synctime = r.tx_time
            except:
                self.synctime = int(time.time())

        self.expiretime = self.synctime + 60

    def isExpired(self):
        return (int(time.time()) > this.expiretime) or (self.synctime is 0)

class GameManager:
    '''this class contains all the game logic, mostly just to keep the main file cleaner'''
    def __init__(self):
        self.gameTime = CountdownClock()
        #self.rfidTracker = RFIDTracker()

    def consumePassword(self, password):
        '''if the password is OK, then notify the device'''
        passwords = ["cosmic", "exoplanet"]
        try:
            #device = DeviceModel.get(is_connected = True, rfidtoken=self.rfidTracker.getActiveUid())
            if password.lower() in passwords:
                #device.setGameStatus(passwords.index(password.lower()), 1)
                return True
            
        except DeviceModel.DoesNotExist:
            #TODO: Deal with device not found
            print("Active Device not found")
        
        return False