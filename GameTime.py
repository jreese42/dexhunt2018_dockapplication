import datetime
import time

class CountdownClock:
    def __init__(self, expiredatetime=None):
        self.expiretime = 0
        self.synctime = 0
	self.expiredatetime = expiredatetime

        if self.expiredatetime is None:
            self.expiredatetime = datetime.datetime.strptime("2018-08-07 17:30", "%Y-%m-%d %H:%M")

        #try:
            #ntpClient = ntplib.NTPClient()
            #r = ntpClient.request('pool.ntp.org')
            #self.synctime = r.tx_time
        #except:
            #try:
               # ntpClient = ntplib.NTPClient()
                #r = ntpClient.request('0.pool.ntp.org')
                #self.synctime = r.tx_time
            #except:
             #self.synctime = int(time.time())
	#epoch = datetime.datetime(1970,1,1)
	#self.synctime = (datetime.datetime.now() - epoch).total_seconds()

        #td = expiredatetime - datetime.datetime.now()
        #self.expiretime = self.synctime + td.seconds

    def isExpired(self):
        #return (int(time.time()) > this.expiretime) or (self.synctime is 0)
	td = self.expiredatetime - datetime.datetime.now()
	return td.seconds > 0

    def remainingSeconds(self):
	now = datetime.datetime.now()
	td = self.expiredatetime - datetime.datetime.now()
	t = 0
	if now < self.expiredatetime:
		t = td.seconds
	print("Remaining Time: " + str(t))
	return t
