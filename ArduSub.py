#===================================================================================#
# import section

from pymavlink import mavutil

from ms5837 import MS5837_30BA

from time import sleep

import Jetson.GPIO as GPIO

#===================================================================================#


#===================================================================================#
# description section
#===================================================================================#

#===================================================================================#
# coding section

motion_types = {
	'PITCH': 1,
	'ROLL':  2,
	'HEAVE': 3,
	'YAW':   4,
	'FORWARD':5,
	'LATERAL':6
		}

speeds = {
	 'MAX_POS':1900,
	 'MIN_POS':1600,
	 'KILL':   1500,
	 'MAX_NEG':1400,
	 'MIN_NEG':1100
	 }


class ArduSub(object):

	def __init__(self, mode, motion_type, speed):

		self.mode = mode
		self.motion_type = motion_type
		self.speed = speed

		global motion_types, speeds

		#Create connection            
		master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
		#Wait for heartbeat
		master.wait_heartbeat()
		
		# arming the thrusters
		master.arducopter_arm()
	
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(18, GPIO.IN)
		GPIO.setup(12, GPIO.OUT)
		GPIO.output(8)
		GPIO.input(7)
		GPIO.setwarnings(False)

		if mode not in master.mode_mapping():
			print('Unknown mode : {}'.format(self.mode))
			print('Try:', list(master.mode_mapping().keys()))
        
		mode_id = master.mode_mapping()[self.mode]
		
		master.mav.set_mode_send(
					master.target_system,
					mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
					mode_id
					)

	#---------------------------------------------------------------------------#

	@staticmethod
	def button():

		buttons = 1 + 1 << 3 + 1 << 7

		master.mav.manual_control_send(
						master.target_system,
						0,
						0,
						0,
						0,
						buttons
					       )

	def auvPwm(self):
	    #pwm
	    if motion_types[self.motion_type] < 1:
		return

	    if id < 9:
		rc_channel_values = [65535 for _ in range(8)]

		rc_channel_values[id - 1] = speeds[self.speed]

		master.mav.rc_channels_override_send(
						    master.target_system,
						    master.target_component,
						    *rc_channel_values
						    )

	#---------------------------------------------------------------------------#

	@staticmethod
	def auvDepth():

	sensor = MS5837_30BA()

		if not sensor.init():
		        exit(1)

		if not sensor.read():
		    exit(1)

		freshwaterDepth = sensor.depth()
		sensor.setFluidDensity(1000)
	    
	    return freshwaterDepth

	#---------------------------------------------------------------------------#

	@staticmethod
	def startMission():
	    while True:
	        if (GPIO.input(7)):
	            print('Activated!')
	        else:
	            sleep(1)

	#---------------------------------------------------------------------------#

	def __del__(self):
		
		#disarm
		#master.arducopter_disarm()

		print('Disarm!')


#===================================================================================#