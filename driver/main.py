from slave_driver import SlaveDriver
from constants import N_FLOORS
import time
import subprocess
import sys
from random import randint



def main():
	master_queue = [0 for floor in range(0,N_FLOORS*2)]
	try:
		time.sleep(0.01)
		driver = SlaveDriver()
		while True:
			(master_floor, master_button) = driver.pop_floor_panel_queue()
			#master_floor = None
			#master_button = None
			if (master_floor != None) and (master_button != None):
				if (master_button == 0) and (master_queue[master_floor] == 0):
					master_queue[master_floor] = randint(1,3)
					#master_queue[master_floor] = 1
				if (master_button == 1) and (master_queue[master_floor+N_FLOORS] == 0):
					master_queue[master_floor+N_FLOORS] = randint(1,3)
					#master_queue[master_floor+N_FLOORS] = 1
			driver.master_queue_elevator_run(master_queue)
			#else:
			#for floor in range(0,N_FLOORS*2):


			print driver.read_saved_master_queue()
			(last_floor, next_floor, direction) = driver.read_position()
			if last_floor == next_floor:
				if direction == 0:
					master_queue[next_floor+N_FLOORS]=0
				elif direction == 2:
					master_queue[next_floor]=0
				else:
					master_queue[next_floor+N_FLOORS]=0
					master_queue[next_floor]=0


	except KeyboardInterrupt:
		pass
	except StandardError as error:
		print error
	finally:
		print "exiting main"
		

if __name__ == "__main__":
		main()
	
		
