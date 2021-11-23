#===================================================================================#
# import section

import datetime

#===================================================================================#

#===================================================================================#
# Descritpion section

# Getter

'''Gets types of movements to perform a certain motion'''

# Setter 

''''''
#===================================================================================#

#===================================================================================#
# coding section

states = {'S':'STABLIZE',
		 'A_H': 'ALTITUDE_HOLD'}

motion_types = {
	 'PITCH': 1,
	 'ROLL':  2,
	 'HEAVE': 3,
	 'YAW':   4,
	 'FORWARD': 5,
	 'LATERAL': 6
			  }

speeds = {
	'KILL': 1500,
	'MAX_POS': 1900,
	'MIN_POS': 1600,
	'MAX_NEG': 1400,
	'MIN_NEG': 1100
	     }

#----------------------------------------------------------------------------------#


class Locomotion(object):
	"""docstring for Locomotion"""
	direct = 0

	def __init__(self):

		print('Hi, there! I am the locomotory body...')

	#------------------------------------------------------------------------------#

	'''run the motion python file with parameters'''

	def giveMotion(self):

		def forwardMotion(self, x, speed, time):
			# to perform forward motion
			print('Moving forward {} meters.'.format(x))

		#---------------------------------------------------------------------------#

		def leftwardMotion(self, y, speed, time):
			# to perform leftward motion
			print('Moving leftward {} meters.'.format(y))

		#---------------------------------------------------------------------------#

		def rightwardMotion(self, y, speed, time):
			# to perform rightward motion
			print('Moving rightward {} meters.'.format(y))

		#---------------------------------------------------------------------------#

		def heaveMotion(self, z, speed):
			# to depth hold the vehicle
			print('Moving down {} meters.'.format(z))

		return forwardMotion, leftwardMotion, rightwardMotion, heaveMotion


#----------------------------------------------------------------------------------#


class Transition(Locomotion):
	"""docstring for Transition"""

	def __init__(self, state, pos, motion_type, 
				left_r_right, speed, e_time):
		
		super(Transition, self).__init__()

		self.state = state
		self.pos = pos
		self.motion_type = motion_type
		self.left_r_right = left_r_right
		self.speed = speed
		self.e_time = e_time # elapsed time

		print('I am gonna perform the {} mode in just a bit'.format(states[self.state]))

		# to arm the vehicle 
		'''call arm.py'''
		print('The thrusters are amred too. Let\'s go yeah!')

		# to call mission starter
		'''call mission_starter.py'''
		print('The mission begins')

	#---------------------------------------------------------------------------#.

	# to evaluate time consumed
	@staticmethod
	def clock():
		pass

	#---------------------------------------------------------------------------#

	def performMotion(self):
		# should set the type of motion for the vehicle
		'''
		1 -> Pitch
		2 -> Roll
		3 -> Heave
		4 -> Yaw
		5 -> Forward
		6 -> Lateral
		'''
		f, l, r, h = super(Transition, self).giveMotion()

		if self.speed != 'KILL':

			print('Performing {}'.format(self.motion_type))			
			
			if self.motion_type == 'FORWARD':
				# to move forward
				f(self, self.pos, self.speed, None)

			if self.motion_type == 'LATERAL':

				if self.left_r_right:
					l(self, self.pos, self.speed, None)

				else:
					r(self, self.pos, self.speed, None)

			if self.motion_type == 'HEAVE':

				self.speed = 'MIN_POS'
				h(self, self.pos, self.speed)

		# should set the speed of the thrusters
		'''
		1500 -> Stop
		1600, 1900 -> Forward maximum and minimum respectively
		1100, 1400 -> Reverse maximum and minimum respectively 
		'''
		if self.speed != 'KILL':
			print('The vehicle is moving {} with the speed of {}'.format(self.motion_type, 
																		 speeds[self.speed]))

		else:
			print('The thrusters have been killed!')


		print('#---------------------------------------------------------------------------#')

		return False

	#---------------------------------------------------------------------------#

	@classmethod
	def fromData(cls, text):
		cls.text = text
		state, pos, motion_type, left_r_right, speed, e_time = cls.text.split(',')

		if e_time == 'None':
			e_time = None

		left_r_right = bool(left_r_right)

		pos = float(pos)

		return cls(state, pos, motion_type, left_r_right, speed, e_time)


#----------------------------------------------------------------------------------# 


class Execution(Transition):
	"""docstring for Execution"""
	count = None
	move = None

	global states, motion_types, speeds

	def __init__(self, state, pos, motion_type, left_r_right, speed, e_time):

		self.state = state
		self.pos = pos
		self.motion_type = motion_type
		self.left_r_right = left_r_right
		self.speed = speed
		self.e_time = e_time

		self.count = 1
		self.move = 1
		
		print('Execution task...')

		#---------------------------------------------------------------------------#

		while True:

			dist, speed_, dir = self.performSway(self.move, self.speed, self.left_r_right)

			if self.count % 2 == 0:

				super(Execution, self).__init__(self.state, self.move, self.motion_type,
												self.left_r_right, self.speed, self.e_time
												)

				super(Execution, self).performMotion()

				self.move = dist(self)
				self.speed = speed_(self)
				self.left_r_right = dir(self)

				self.count += 1

			elif self.count % 2 != 0:

				super(Execution, self).__init__(self.state, self.move, self.motion_type,
												self.left_r_right, self.speed, self.e_time
												)

				super(Execution, self).performMotion()

				self.move = dist(self)
				self.speed = speed_(self)
				self.left_r_right = dir(self)

				self.count += 1

			if self.count >= 10:
				break

	#---------------------------------------------------------------------------#

	def performSway(self, move, speed, left_r_right):

		def changeDistance(self):

			if left_r_right:
				return move + 1

			else:
				return move + 1

		def changeSpeed(self):
			if speed == 'MIN_POS':
				return 'MIN_NEG'

			return 'MIN_POS'

		def changeDirection(self):
			return not left_r_right

		return changeDistance, changeSpeed, changeDirection

	#---------------------------------------------------------------------------#

	@classmethod
	def fromText(cls, text):

		state, pos, motion_type, left_r_right_list, speed_list, e_time = text.split(',')

		cls.state = state
		cls.pos = pos
		cls.motion_type = motion_type
		cls.e_time = e_time

		try:
			left_r_right_unpack = map(bool, left_r_right_list.split('-'))
			speed_list_unpack = speed_list.split('-')

		except Exception as e:
			print(str(e))

		for left_r_right, speed in zip(left_r_right_unpack, speed_list_unpack):

			return cls(cls.state, cls.pos, cls.motion_type, left_r_right, speed, cls.e_time)


#===================================================================================#