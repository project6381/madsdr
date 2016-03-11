from driver import Driver

def main():
	__Driver = Driver()
	while True:

		(master_floor, master_button) = __Driver.pop_floor_panel_queue()
		if (master_floor != None) and (master_button != None):
			__Driver.queue_elevator_run(master_floor, master_button)
		print __Driver.read_position()


if __name__ == "__main__":
    main()