
from RFIDTracker import RFIDTracker
import ntplib, time
from networkmodel import DeviceModel
from GameTime import CountdownClock

class GameManager:
    '''this class contains all the game logic, mostly just to keep the main file cleaner'''
    def __init__(self):
        self.gameTime = CountdownClock()
        self.rfidTracker = RFIDTracker()

    def consumePassword(self, password):
        '''if the password is OK, then notify the device'''
        passwords = ["cosmic", "exoplanet", "terraform", "stardust", "castor", "starbucks", "sentient", "puzzle8"]
        normalized_password = password.lower().replace(' ', '')
        try:
            device = DeviceModel.get(is_connected = True, rfidtoken=self.rfidTracker.getActiveUid())
            if normalized_password in passwords:
                device.setGameStatus(passwords.index(normalized_password, 1))
                return True
            
        except DeviceModel.DoesNotExist:
            #TODO: Deal with device not found
            print("Active Device not found")
        
        return False

    def getActiveDeviceScore(self):
        try:
            device = DeviceModel.get(is_connected = True, rfidtoken=self.rfidTracker.getActiveUid())
            if password.lower() in passwords:
                score = device.getScore()
                return score
            
        except DeviceModel.DoesNotExist:
            #TODO: Deal with device not found
            print("Active Device not found")
        
        return 0
