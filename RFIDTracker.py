import sched
from RecurringTask import RecurringTask
import MFRC522

class RFIDTracker:
    def __init__(self):
        '''init'''
        self.rfidReader = MFRC522.MFRC522()  
        readTask = RecurringTask(0.25, readFromRfid, [self])
        self.activeUid = None
    def getActiveUid(self):
        '''return the active UID'''
        return self.activeUid
    def rfidTagIsActive(self):
        '''return if an RFID tag is currently readable'''
        return self.activeUid is not None
    def readFromRfid(self):
        # (status,TagType) = self.rfidReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll() 
        if status == MIFAREReader.MI_OK:
            # Print UID
            self.activeUid = ''.join(str(x) for x in uid)
            print "Card read UID: %s" % (self.activeUid)
        else:
            print "status is " + str(status)