import elevator
import panel
import constants
import time
from threading import Thread
from threading import Lock


class ElevatorDriver:
	def __init__(self):
		self.elevator_interface = elevator.ElevInterface()
		self.panel_interface = panel.PanelInterface()
		self.queue_key = Lock()
		self.queue = [[0 for button in range(0,3)] for floor in range(0,constants.N_FLOORS)]
		self.thread_floor_queue = Thread(target = self.run_floor_queue, args = (),)
		self.thread_build_queue = Thread(target = self.run_build_queue, args = (),)


	def run_floor_queue(self):

		last_floor=2
		next_floor=2
		direction = "None"

		while True:
			time.sleep(0.001)

			floor_max = 0
			floor_min = constants.N_FLOORS-1

			for floor in range(0,constants.N_FLOORS):
				for button in range(0,3):
					if self.queue[floor][button] == 1:
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

			read_floor = self.elevator_interface.get_floor_sensor_signal()
			if read_floor >= 0:
				last_floor = read_floor

			self.set_indicator(last_floor,next_floor)
			self.go_to_floor(last_floor,next_floor)
			self.clear_floor_queue(last_floor,next_floor,direction)
			
			print self.queue


	def run_build_queue(self):
		while True:
			time.sleep(0.001)
			for floor in range (0,constants.N_FLOORS):
				for button in range(0,3):
					if (floor == 0 and button == 1) or (floor == 3 and button == 0):
						pass
					elif self.panel_interface.get_button_signal(button,floor):
						with self.queue_key:
							self.queue[floor][button]=1


	def clear_floor_queue(self,last_floor,next_floor,direction):
		if last_floor == next_floor:
			if direction == "None":
				with self.queue_key:
					self.queue[next_floor][0] = 0
					self.queue[next_floor][1] = 0
					self.queue[next_floor][2] = 0
			elif direction == "UP":
				with self.queue_key:
					self.queue[next_floor][0] = 0
					self.queue[next_floor][2] = 0
			elif direction == "DOWN":
				with self.queue_key:
					self.queue[next_floor][1] = 0
					self.queue[next_floor][2] = 0



	def set_indicator(self,last_floor,next_floor):
		for floor in range(0,constants.N_FLOORS):
				for button in range(0,3):
						if (floor == 0 and button == 1) or (floor == 3 and button == 0):
							pass
						elif self.queue[floor][button] == 1:
							self.panel_interface.set_button_lamp(button,floor,1)
						else:
							self.panel_interface.set_button_lamp(button,floor,0)
		
		if last_floor == next_floor:
			self.panel_interface.set_door_open_lamp(1)
		else:
			self.panel_interface.set_door_open_lamp(0)

		self.panel_interface.set_floor_indicator(last_floor)


	def go_to_floor(self,last_floor,next_floor):
		if last_floor == next_floor:
			self.elevator_interface.set_motor_direction(constants.DIRN_STOP)
			time.sleep(1)
		elif last_floor < next_floor:
			self.elevator_interface.set_motor_direction(constants.DIRN_UP)
		elif last_floor > next_floor:
			self.elevator_interface.set_motor_direction(constants.DIRN_DOWN)

	def start(self):
		self.thread_floor_queue.start()
		self.thread_build_queue.start()


def main():
	elevator_driver1 = ElevatorDriver()

	elevator_driver1.start()


if __name__ == "__main__":
    main()