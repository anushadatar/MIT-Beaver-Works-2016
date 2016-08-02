#!/usr/bin/env python
import rospy, math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Int32, Float32
from PID import PIDClass

class pidDriver:
    def __init__(self):		
		self.error = 0 # running error counter
		self.d_des = 0.5 # distance from wall
    
    self.start = True
		self.pidVal = 0
		self.scan1 = []
		self.scan2 = []
		
		rospy.init_node("wall_PID",  anonymous=False)
		self.sideFlag = 0
		self.pid = PIDController(rospy.Time.now().to_sec(), -1.0,0.0, 0.0)#0.00000001,0.12)

		rospy.Subscriber("/side", Int32, self.sideChange)
		rospy.Subscriber("/scan",  LaserScan,  self.callback)

		self.angle_pub = rospy.Publisher("/steer_angle_follow", Float32, queue_size = 1)
		
    def flag(self, msg):
	self.start = msg.data
    def sideChange(self, msg):
	self.sideFlag = msg.data
    def callback(self,msg):
		self.scan1 = []
		self.scan2 = []
		for i in range(895, 906):
			self.scan1.append(msg.ranges[i]) # gets 90 degree scans and adds them to scan1
		for i in range(855, 866):
			self.scan2.append(msg.ranges[i]) # gets 100 degree scans and adds them to scan2
		self.main(self.scan1, self.scan2)
    def scanangle(r1, r2, theta)
    		theta = theta * (math.pi/180)
		numerator = r1 * r2 * math.sin(theta)
		denom_wo_sqrt = r1 ** 2 + r2 ** 2 + (-2*r1*r2*math.cos(theta))
		denom = math.sqrt(denom_wo_sqrt)
		d = numerator / denom
		return d

    def main(self, scan1, scan2):
		    self.error = 0
		    total1 = 0 # total distance for averaging (from scan1)
		    total2 = 0 # total distance for averaging (from scan2)

		    meanD_x = 0 # average distance taken from scan1
		    meanD_y = 0 # average dist taken from scan2

		    for i in scan1: 
			total1 += i # adds each element of scan1 to total for averaging
		    for i in scan2:
			total2 += i # same as above but for scan2
		    meanD_x = total1/len(scan1) if len(scan1) > 0 else 0# average of scan1
		    meanD_y = total2/len(scan2) if len(scan2) > 0 else 0# average of scan2

		    if meanD_x != 0 and meanD_y != 0: # checks if vals are good
			#print ("started trig")
			d_actual = scanangle(meanD_x, meanD_y, 10)

		    else:
			return
	            print "d_actual: " + str(d_actual)
		    self.error = self.d_des - d_actual 
		    print "error: " + str(self.error)

		    self.pidVal = self.pid.update(self.error,  rospy.Time.now().to_sec())
		    self.pidVal = self.pidVal/abs(self.pidVal) * min(1.0,  abs(self.pidVal)) if self.pidVal!=0 else 0
		    
		    self.publisher()
		   

    def publisher(self):
		print("published angle")
		self.angle_pub.publish(self.pidVal)
		

if __name__ == "__main__":
	pidDriver()
	rospy.spin()
