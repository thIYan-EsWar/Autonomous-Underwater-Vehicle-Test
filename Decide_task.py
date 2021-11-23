#===================================================================================#
# import section

from Locomotion import Transition, Execution

from Post_Execution import PostExecution, PostEScanning

#===================================================================================#

#===================================================================================#
# Description section

# Getter:

'''Needs the final decision'''

# Setter:

'''
Assigns the mode and asks for the name of the task

states = {'S':'STABLIZE',
		 'A_H': 'ALTITUDE_HOLD'}

motion_types = {
	 'Pitch': 1,
	 'Roll':  2,
	 'Heave': 3,
	 'Yaw':   4,
	 'Forward': 5,
	 'Lateral': 6
			  }

speeds = {
	'Kill': 1500,
	'Max_forward': 1900,
	'Min_forward': 1600,
	'Max_reverse': 1400,
	'Min_reverse': 1100
	     }
''' 
#===================================================================================#

#===================================================================================#
# coding section

count = 0

perform = True
isContinueLoop = True

f = open('Transition_data.txt', 'r')
line_count = len(f.readlines())
f.close()


class DecideTask(object):
	"""docstring for DesideTask"""

	def __init__(self, mode):
		self.mode = mode
		self.arguments = None

		global perform, count 
		
		if self.mode == 'Transition':
			# call locomotion motion
			mode = 'Transition'
			print('I have been called! Gonna make the jump...')

			print('#---------------------------------------------------------------------------#')

			with open('Transition_data.txt', 'r') as f:

				global line_count, isContinueLoop

				for _ in range(line_count):
					self.arguments = f.readline()

					motion = Transition.fromData(self.arguments)

					perform = motion.performMotion()

					if not perform:
						
						'''
						while isContinueLoop:

							check = PostExecution.from_text(self.arguments)
							destiny = check.checkPosition()

							if destiny < 0.2:
								isContinueLoop = not isContinueLoop
						'''

						check = PostExecution.from_text(self.arguments)
						destiny = check.checkPosition()

						perform = not perform

					if count != 0 and count % 3 == 0:
						with open('Execution_data.txt', 'r') as l:
							contents = l.readline()

						self.assignAndGetTask(contents)

					count += 1

	#------------------------------------------------------------------------------#

	def assignAndGetTask(self, text):

		# assign and ask for the task from Task.py

		print('                + --------------------------------------- +')
		print('               |        Switching to Execution mode        |')
		print('                + --------------------------------------- +')

		execute = Execution.fromText(text)

		return


#===================================================================================#