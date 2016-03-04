import ElevInterface
import PanelInterface
import constants
import time
from threading import Thread
from threading import Lock

elevator = ElevInterface.ElevInterface()
panel = PanelInterface.PanelInterface()

queue_key = Lock()
queue = [[0 for button in range(0,3)] for floor in range(0,constants.N_FLOORS)]


def run_floor_queue():
	last_floor=2
	next_floor=2
	direction = "None"
	while True:
		time.sleep(0.001)

		floor_max = 0
		floor_min = constants.N_FLOORS-1

		for floor in range(0,constants.N_FLOORS):
			for button in range(0,3):
				if queue[floor][button] == 1:
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

		read_floor = elevator.get_floor_sensor_signal()
		if read_floor >= 0:
			last_floor = read_floor

		set_indicator(last_floor,next_floor)
		go_to_floor(last_floor,next_floor)
		clear_floor_queue(last_floor,next_floor,direction)
		
		print queue


def run_build_queue():
	while True:
		time.sleep(0.001)
		for floor in range (0,constants.N_FLOORS):
			for button in range(0,3):
				if (floor == 0 and button == 1) or (floor == 3 and button == 0):
					pass
				elif panel.get_button_signal(button,floor):
					with queue_key:
						queue[floor][button]=1

def clear_floor_queue(last_floor,next_floor,direction):
	if (last_floor == next_floor):
		if (direction == "None"):
			with(queue_key):
				queue[next_floor][0] = 0
				queue[next_floor][1] = 0
				queue[next_floor][2] = 0
		elif (direction == "UP"):
			with(queue_key):
				queue[next_floor][0] = 0
				queue[next_floor][2] = 0
		elif (direction == "DOWN"):
			with(queue_key):
				queue[next_floor][1] = 0
				queue[next_floor][2] = 0



def set_indicator(last_floor,next_floor):
	for floor in range(0,constants.N_FLOORS):
			for button in range(0,3):
					if (floor == 0 and button == 1) or (floor == 3 and button == 0):
						pass
					elif queue[floor][button] == 1:
						panel.set_button_lamp(button,floor,1)
					else:
						panel.set_button_lamp(button,floor,0)
	
	if last_floor == next_floor:
		panel.set_door_open_lamp(1)
	else:
		panel.set_door_open_lamp(0)

	panel.set_floor_indicator(last_floor)


def go_to_floor(last_floor,next_floor):
	if last_floor == next_floor:
		elevator.set_motor_direction(constants.DIRN_STOP)
		time.sleep(1)
	elif last_floor < next_floor:
		elevator.set_motor_direction(constants.DIRN_UP)
	elif last_floor > next_floor:
		elevator.set_motor_direction(constants.DIRN_DOWN)




def main():
	thread_1 = Thread(target = run_floor_queue, args = (),)
	thread_2 = Thread(target = run_build_queue, args = (),)

	thread_1.start()
	thread_2.start()


if __name__ == "__main__":
    main()