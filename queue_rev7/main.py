import elevator
import panel
import constants
import time
from threading import Thread
from threading import Lock


class ElevatorDriver:
	def __init__(self):
		self.__elevator_interface = elevator.ElevInterface()
		self.__panel_interface = panel.PanelInterface()
		self.__floor_queue_key = Lock()
		self.__buttons_to_master_key = Lock()
		self.__floor_queue = [[0 for button in range(0,3)] for floor in range(0,constants.N_FLOORS)]
		self.__buttons_to_master = []
		self.__thread_floor_queue = Thread(target = self.__run_floor_queue, args = (),)
		self.__thread_build_queue = Thread(target = self.__build_floor_queue, args = (),)


	def start(self):
		self.__thread_floor_queue.start()
		self.__thread_build_queue.start()

	def queue_floor_button(self,floor,button):
		with self.__floor_queue_key:
			self.__foor_queue[floor][button]=1

	def read_button_to_master(self):
		with self.__buttons_to_master_key:
			if self.__buttons_to_master:
				return self.__buttons_to_master.pop(0)
			else:
				return (None, None)


	def __run_floor_queue(self):

		last_floor=2
		next_floor=2
		direction = "None"

		while True:
			time.sleep(0.001)

			floor_max = 0
			floor_min = constants.N_FLOORS-1

			for floor in range(0,constants.N_FLOORS):
				for button in range(0,3):
					if self.__floor_queue[floor][button] == 1:
						floor_max = max(floor_max,floor)
						floor_min = min(floor_min,floor)
						if (last_floor == next_floor) and (direction != "DOWN") and (next_floor < floor_max):
							next_floor = floor
							direction = "UP"
						elif (last_floor == next_floor) and (direction != "UP") and (next_floor > floor_min):
							next_floor = floor
							direction = "DOWN"
						elif (last_floor < next_floor) and (floor < next_floor) and (floor > last_floor) and (button != 1):
							next_floor = floor
						elif (last_floor > next_floor) and (floor > next_floor) and (floor < last_floor) and (button != 0):
							next_floor = floor

			if (direction == "UP") and (floor_max <= last_floor):
				direction = "None"
			elif (direction == "DOWN") and (floor_min >= last_floor):
				direction = "None"

			read_floor = self.__elevator_interface.get_floor_sensor_signal()
			if read_floor >= 0:
				last_floor = read_floor

			self.__set_indicator(last_floor,next_floor)
			self.__go_to_floor(last_floor,next_floor)
			self.__clear_floor_queue(last_floor,next_floor,direction)
			
			#print self.__floor_queue


	def __build_floor_queue(self):
		while True:
			time.sleep(0.001)
			for floor in range (0,constants.N_FLOORS):
				for button in range(0,3):
					if (floor == 0 and button == 1) or (floor == 3 and button == 0):
						pass
					elif self.__panel_interface.get_button_signal(button,floor):
						if button == 2:
							with self.__floor_queue_key:
								self.__floor_queue[floor][button]=1
						else:
							with self.__buttons_to_master_key:
								self.__buttons_to_master.append((floor,button))



	def __clear_floor_queue(self,last_floor,next_floor,direction):
		if last_floor == next_floor:
			if direction == "None":
				with self.__floor_queue_key:
					self.__floor_queue[next_floor][0] = 0
					self.__floor_queue[next_floor][1] = 0
					self.__floor_queue[next_floor][2] = 0
			elif direction == "UP":
				with self.__floor_queue_key:
					self.__floor_queue[next_floor][0] = 0
					self.__floor_queue[next_floor][2] = 0
			elif direction == "DOWN":
				with self.__floor_queue_key:
					self.__floor_queue[next_floor][1] = 0
					self.__floor_queue[next_floor][2] = 0



	def __set_indicator(self,last_floor,next_floor):
		for floor in range(0,constants.N_FLOORS):
				for button in range(0,3):
						if (floor == 0 and button == 1) or (floor == 3 and button == 0):
							pass
						elif self.__floor_queue[floor][button] == 1:
							self.__panel_interface.set_button_lamp(button,floor,1)
						else:
							self.__panel_interface.set_button_lamp(button,floor,0)
		
		if last_floor == next_floor:
			self.__panel_interface.set_door_open_lamp(1)
		else:
			self.__panel_interface.set_door_open_lamp(0)

		self.__panel_interface.set_floor_indicator(last_floor)


	def __go_to_floor(self,last_floor,next_floor):
		if last_floor == next_floor:
			self.__elevator_interface.set_motor_direction(constants.DIRN_STOP)
			time.sleep(1)
		elif last_floor < next_floor:
			self.__elevator_interface.set_motor_direction(constants.DIRN_UP)
		elif last_floor > next_floor:
			self.__elevator_interface.set_motor_direction(constants.DIRN_DOWN)



def main():
	elevator_driver = ElevatorDriver()
	elevator_driver.start()
	while True:

		(master_floor, master_button) = elevator_driver.read_button_to_master()
		if (master_floor and master_button) is not None:
			print (master_floor, master_button)


if __name__ == "__main__":
    main()