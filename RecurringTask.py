from threading import Timer,Thread,Event

class RecurringTask():

   def __init__(self,t,hFunction, args):
      self.t=t
      self.hFunction = hFunction
      self.args = args
      self.thread = Timer(self.t,self.handle_function, self.args)
      self.thread.daemon = True

   def handle_function(self, kwargs):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function, self.args)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()
