from driver import Driver
import time

def main():
	try:
		time.sleep(3)
		driver = Driver()
		while True:
			(master_floor, master_button) = driver.pop_floor_panel_queue()
			if (master_floor != None) and (master_button != None):
				driver.queue_elevator_run(master_floor, master_button)
			print driver.read_position()
	except:
		driver.stop()
		execfile("main.py")

if __name__ == "__main__":
		main()
	
		
