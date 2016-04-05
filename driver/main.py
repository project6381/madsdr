from slave_driver import SlaveDriver
from constants import N_FLOORS
import time
import subprocess
import sys
from random import randint



def main():
	master_queue = [0 for floor in range(0,N_FLOORS*2)]
	try:
		#time.sleep(3)
		driver = SlaveDriver()
		while True:
			(master_floor, master_button) = driver.pop_floor_panel_queue()
			if (master_floor != None) and (master_button != None):
				if master_button = 0:
					master_queue[master_floor] = randint(1,3)
				if master_button = 1:
					master_queue[master_floor] = randint(1,3)
				driver.master_queue_elevator_run(master_queue)

			print driver.read_saved_master_queue()
			#print driver.read_position()

	except KeyboardInterrupt:
		pass
	except StandardError as error:
		print error
	finally:
		print "exiting main"
		

if __name__ == "__main__":
		main()
	
		
