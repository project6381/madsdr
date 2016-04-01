from slave_driver import SlaveDriver
import time
import subprocess
import sys

def main():
	try:
		#time.sleep(3)
		driver = SlaveDriver()
		while True:
			(master_floor, master_button) = driver.pop_floor_panel_queue()
			if (master_floor != None) and (master_button != None):
				driver.queue_elevator_run(master_floor, master_button)
			#print driver.read_position()

	except KeyboardInterrupt:
		pass
	except StandardError as error:
		print error
	finally:
		print "exiting main"
		

if __name__ == "__main__":
		main()
	
		
