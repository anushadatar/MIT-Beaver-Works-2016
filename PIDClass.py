class PIDClass:
	def __init__(self,time, Kp=0, Ki=0, Kd=0):
		#init constants
		self._Kp = Kp
		self._Kd = Kd
		self._Ki = Ki

        #init timer
		self._integrator = 0
		self._error=0
		self._pastTime = time
		self._startTime = time
	def update(self, error, time):
        #strart proportional
		P = self._Kp * error


		dt = float(time - self._pastTime)
        #start integral
		self._integrator += error * dt
		I = self._integrator * self._Ki
		#start derivative
		errDiff = error - self._error
		diff = errDiff/dt if dt != 0 else 0
		D = self._Kd * diff
		PID = P + I + D
		timeSince = time - self._startTime
		self.logError(error, timeSince)
		self._pastTime = time

		self._error = error

		return PID
	def logError(self, error, time):
		self._logHandle.write(str(time) + "," + str(error) + "\n")
