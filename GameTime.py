import datetime
import time

class CountdownClock:
    def __init__(self, expiredatetime=None):
        self.expiretime = 0
        self.synctime = 0

        if expiredatetime is None:
            expiredatetime = datetime.datetime(2018,7,21, 14,30)

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

        td = expiredatetime - datetime.datetime.now()
        self.expiretime = self.synctime + td.seconds

    def isExpired(self):
        return (int(time.time()) > this.expiretime) or (self.synctime is 0)

    def remainingSeconds(self):
        currtime = int(time.time())
        if (currtime > this.expiretime or self.synctime is 0):
            return 0
        else:
            return this.expiretime - currtime