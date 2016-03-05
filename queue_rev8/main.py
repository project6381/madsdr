from elevator import ElevatorInterface
from panel import PanelInterface
from constants import N_FLOORS, DIRN_STOP, DIRN_UP, DIRN_DOWN
from threading import Thread, Lock
import time
import pickle


class ElevatorDriver:
	def __init__(self):
		self.__ElevatorInterface = ElevatorInterface()
		self.__PanelInterface = PanelInterface()
		self.__floor_queue_key = Lock()
		self.__button_queue_key = Lock()
		self.__floor_queue = [[0 for button in range(0,3)] for floor in range(0,N_FLOORS)]
		self.__button_queue = []
		self.__position = (0,0,"None")
		self.__thread_run_floor_queue = Thread(target = self.__run_floor_queue, args = (),)
		self.__thread_build_queues = Thread(target = self.__build_queues, args = (),)
		self.__thread_set_indicator = Thread(target = self.__set_indicator, args = (),)
		self.__thread_save_floor_queue = Thread(target = self.__save_floor_queue, args = (),)


	def start(self):

		check_floor = self.__ElevatorInterface.get_floor_sensor_signal()
		turn_time = time.time() + 10

		while check_floor < 0:
			if turn_time > time.time():
				self.__ElevatorInterface.set_motor_direction(DIRN_UP)
			else:
				self.__ElevatorInterface.set_motor_direction(DIRN_DOWN)
			check_floor = self.__ElevatorInterface.get_floor_sensor_signal()

		self.__ElevatorInterface.set_motor_direction(DIRN_STOP)

		self.__load_floor_queue()
		self.__thread_run_floor_queue.start()
		self.__thread_build_queues.start()
		self.__thread_set_indicator.start()
		self.__thread_save_floor_queue.start()


	def queue_floor_button_run(self,floor,button):
		with self.__floor_queue_key:
			self.__floor_queue[floor][button]=1


	def pop_button_queue(self):
		with self.__button_queue_key:
			if self.__button_queue:
				return self.__button_queue.pop(0)
			else:
				return (None, None)


	def read_position(self):
		return self.__position


	def __run_floor_queue(self):

		last_floor = 0
		next_floor = 0
		direction = "None"

		while True:
			time.sleep(0.001)

			floor_max = 0
			floor_min = N_FLOORS-1

			for floor in range(0,N_FLOORS):
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

			read_floor = self.__ElevatorInterface.get_floor_sensor_signal()
			if read_floor >= 0:
				last_floor = read_floor

			self.__position = (last_floor,next_floor,direction)
			self.__go_to_floor(last_floor,next_floor,direction)
			

	def __build_queues(self):
		while True:
			time.sleep(0.001)
			for floor in range (0,N_FLOORS):
				for button in range(0,3):
					if (floor == 0 and button == 1) or (floor == 3 and button == 0):
						pass
					elif self.__PanelInterface.get_button_signal(button,floor):
						if button == 2:	
							with self.__floor_queue_key:
								self.__floor_queue[floor][button]=1			
						elif (floor,button) not in self.__button_queue:
							with self.__button_queue_key:
								self.__button_queue.append((floor,button))


	def __set_indicator(self):

		saved_floor_queue = [[0 for button in range(0,3)] for floor in range(0,N_FLOORS)]

		while True:
			time.sleep(0.001)
			
			if self.__floor_queue != saved_floor_queue: 
				with self.__floor_queue_key:
					queue_file = open("queue_file", "rb")
					saved_floor_queue = pickle.load(queue_file)
					queue_file.close()

				for floor in range(0,N_FLOORS):
						for button in range(0,3):
								if (floor == 0 and button == 1) or (floor == 3 and button == 0):
									pass
								elif saved_floor_queue[floor][button] == 1:
									self.__PanelInterface.set_button_lamp(button,floor,1)
								else:
									self.__PanelInterface.set_button_lamp(button,floor,0)
			
			(last_floor, next_floor, direction) = self.__position
			
			if last_floor == next_floor:
				self.__PanelInterface.set_door_open_lamp(1)
			else:
				self.__PanelInterface.set_door_open_lamp(0)

			self.__PanelInterface.set_floor_indicator(last_floor)


	def __save_floor_queue(self):

		saved_floor_queue = [[0 for button in range(0,3)] for floor in range(0,N_FLOORS)]

		while True:
			time.sleep(0.001)
			if self.__floor_queue != saved_floor_queue:
				with self.__floor_queue_key:
					queue_file = open("queue_file", "wb")
					pickle.dump(self.__floor_queue, queue_file)
					queue_file.close()
				queue_file = open("queue_file", "rb")
				saved_floor_queue = pickle.load(queue_file)
				queue_file.close()


	def __load_floor_queue(self):
		queue_file = open("queue_file", "rb")
		self.__floor_queue = pickle.load(queue_file)
		queue_file.close()


	def __go_to_floor(self,last_floor,next_floor,direction):
		if last_floor == next_floor:
			self.__ElevatorInterface.set_motor_direction(DIRN_STOP)
			self.__clear_floor_queue(next_floor,direction)
			time.sleep(1)
		elif last_floor < next_floor:
			self.__ElevatorInterface.set_motor_direction(DIRN_UP)
		elif last_floor > next_floor:
			self.__ElevatorInterface.set_motor_direction(DIRN_DOWN)


	def __clear_floor_queue(self,next_floor,direction):
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


def main():
	elevator_driver = ElevatorDriver()
	elevator_driver.start()
	while True:

		(master_floor, master_button) = elevator_driver.pop_button_queue()
		if (master_floor != None) and (master_button != None):
			elevator_driver.queue_floor_button_run(master_floor, master_button)
		#print elevator_driver.read_position()


if __name__ == "__main__":
    main()