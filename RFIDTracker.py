import sched
from RecurringTask import RecurringTask
import MFRC522

class RFIDTracker:
    def __init__(self):
        '''init'''
        self.rfidReader = MFRC522.MFRC522()  
	print "Starting RFID Reader"
        self.readTask = RecurringTask(1, self.readFromRfid, [self])
	self.readTask.start()
        self.activeUid = None
        self.dissapearTicksStart = 1
	self.dissapearTicks = self.dissapearTicksStart
    def getActiveUid(self):
        '''return the active UID'''
        return self.activeUid
    def rfidTagIsActive(self):
        '''return if an RFID tag is currently readable'''
        return self.activeUid is not None
    def readFromRfid(self):
        (status,TagType) = self.rfidReader.MFRC522_Request(self.rfidReader.PICC_REQIDL)    
        # Get the UID of the card
        (status,uid) = self.rfidReader.MFRC522_Anticoll()
        if status == self.rfidReader.MI_OK:
            self.dissapearTicks = self.dissapearTicksStart
            # Print UID
            if self.activeUid is None:
                self.activeUid = ''.join(str(x) for x in uid)
                print "Card read UID: %s" % (self.activeUid)
        elif status == self.rfidReader.MI_ERR:
            if self.dissapearTicks == 0 and self.activeUid is not None:
                self.dissapearTicks = self.dissapearTicksStart
                self.activeUid = None
                print "RFID Tag went away"
            elif self.activeUid is not None:	
                self.dissapearTicks = self.dissapearTicks-1
	def stop(self):
		self.readTask.cancel()
