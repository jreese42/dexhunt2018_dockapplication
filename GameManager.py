
from RFIDTracker import TickableRFIDTracker as RFIDTracker
import ntplib, time
from networkmodel import DeviceModel
from GameTime import CountdownClock

class GameManager:
    '''this class contains all the game logic, mostly just to keep the main file cleaner'''
    def __init__(self):
        self.gameTime = CountdownClock()
        self.rfidTracker = RFIDTracker()
        self.tickCount = 0

    def consumePassword(self, password):
        '''if the password is OK, then notify the device'''
        passwords = [p.lower().replace(' ','') for p in ["cosmic", "exoplanet", "symbiosis", "stardust", "castor", "starbucks", "hyperspace", "triangulum"]]
        normalized_password = password.lower().replace(' ', '').strip()
        try:
            device = DeviceModel.get(is_connected = True, rfidtoken=self.rfidTracker.getActiveUid())
            if normalized_password in passwords:
                device.setGameStatus(passwords.index(normalized_password), 1)
                return True
            
        except DeviceModel.DoesNotExist:
            #TODO: Deal with device not found
            print("Active Device not found")
        
        return False

    def getActiveDeviceScore(self):
        try:
            device = DeviceModel.get(is_connected = True, rfidtoken=self.rfidTracker.getActiveUid())
            score = device.getScore()
            if score is None:
                return 0
            return score
            
        except DeviceModel.DoesNotExist:
            #TODO: Deal with device not found
            print("Active Device not found")
        
        return 0

    def tick(self, ms):
        #tick the RFId tracker every 1s
        self.tickCount += ms
        if self.tickCount > 1000:
            self.tickCount -= 1000 
            self.rfidTracker.tick()
