#===================================================================================#
# import  section

from Locomotion import Transition

#===================================================================================#

#===================================================================================#
# description section
#===================================================================================#

#===================================================================================#
# coding section

count = 3

class PostExecution(object):
	"""docstring for PostExecution"""
	motion_type = None

	def __init__(self, pos, motion_type, direction=True):
		
		self.pos = pos
		self.motion_type = motion_type
		self.direction = direction

		print('Validating the execution.')


	#---------------------------------------------------------------------------#

	def checkPosition(self):
		# checks whether the vehicle travelled the given distance

		result = None

		# should get a value from double integrating file
		'''calls a double integrating python file'''

		# reading = None 
		# getter from BNO 055 
		reading = 5

		# cross validating
		self.result = abs(reading - self.pos)

		if self.result != 0: 

			if self.motion_type == 'LATERAL':	# to check the direction
				# to move right side
				if not(self.direction):
					# to move right 

					print('Moving rightward {} meters'.format(self.result))
					move_again = Transition(state = 'S', pos = self.result,
											motion_type = self.motion_type, left_r_right = self.direction, 
											speed = 'MIN_NEG', e_time = None)

					move_again.performMotion()	

					return self.result

				else:
					# to move left side

					print('Moving leftward {} metes'.format(self.result))
					move_again = Transition(state = 'S', pos = self.result,
											motion_type = self.motion_type, left_r_right = self.direction, 
											speed = 'MIN_POS', e_time = None)

					move_again.performMotion()

					return self.result

		#---------------------------------------------------------------------------#	

			if self.motion_type == 'FORWARD':

				# to move forward

				print('Moving forward {} metes'.format(self.result))
				move_again = Transition(state = 'S', pos = self.result, motion_type = self.motion_type,
										left_r_right = self.direction, speed = 'MIN_POS', e_time = None)

				move_again.performMotion()

				return self.result


			if self.motion_type == 'HEAVE' or self.motion_type == 'YAW':
					
				print('Validation not available! Sorry.')
				print('#---------------------------------------------------------------------------#')

				return 0

		else:
			print('Destination reached!')
			print('#---------------------------------------------------------------------------#')

			return self.result

	#---------------------------------------------------------------------------#

	@classmethod
	def from_text(cls, text):
		_, pos, motion_type, direction, _, _ = text.split(',')

		pos = float(pos)
		
		if direction == 'True':
			direction = True

		else:
			direction = False

		return cls(pos, motion_type, direction) 

	#------------------------------------------------------------------------------#

class PostEScanning(object):
	"""docstring for PostEScanning"""
	def __init__(self, pos, direction):
		super(PostEScanning, self).__init__(pos, direction)
		
		pass
			
		
#===================================================================================#