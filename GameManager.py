
#from RFIDTracker import RFIDTracker
import ntplib

class GameManager:
    '''this class contains all the game logic, mostly just to keep the main file cleaner'''
    def __init__(self):
        #self.rfidTracker = RFIDTracker() #does this need to be threaded?
        pass
        
    def consumePassword(self, password):
        '''if the password is OK, then notify the device'''
        try:

            device = DeviceModel.get(is_connected = True)
            if password.lower() in colors.colornames:
                r,g,b = colors.colornames[password.lower()]
                device.setRGB(0,r,g,b)
                device.setRGB(1,r,g,b)
            if password == "ON1":
                device = DeviceModel.get(is_connected=True)
                device.setGameStatus(0, 1)
            if password == "OFF1":
                device = DeviceModel.get(is_connected=True)
                device.setGameStatus(0, 0)
            if password == "ON2":
                device = DeviceModel.get(is_connected=True)
                device.setGameStatus(1, 1)
            if password == "OFF2":
                device = DeviceModel.get(is_connected=True)
                device.setGameStatus(1, 0)
        except DeviceModel.DoesNotExist:
            print("No Connected Devices")

    def updateTimer(self):
        ntpClient = ntplib.NTPClient()
        r = ntpClient.request('pool.ntp.org', version=3)
        #r.tx_time
        #perform NTP Sync
        #calculate time remaining until finishline
        #send remaining time to all connected nodes