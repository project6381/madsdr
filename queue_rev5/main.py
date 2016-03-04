import ElevInterface
import PanelInterface
import constants
import time
from threading import Thread
from threading import Lock

elevator = ElevInterface.ElevInterface()
panel = PanelInterface.PanelInterface()

queueKey = Lock()
queue = [[0 for y in range(0,3)] for x in range(0,constants.N_FLOORS)]
goFloor = 2
lastFloor = 2


def queue_floor():
	global goFloor
	global lastFloor
	direction = "None"
	while True:
		time.sleep(0.001)
		x_max = 0
		x_min = constants.N_FLOORS-1

		for x in range(0,constants.N_FLOORS):
			for y in range(0,3):
				if queue[x][y] == 1:
					x_max = max(x_max,x)
					x_min = min(x_min,x)
					if (lastFloor == goFloor) and (direction != "DOWN") and (goFloor < x_max):
						goFloor = x
						direction = "UP"
					elif (lastFloor == goFloor) and (direction != "UP") and (goFloor > x_min):
						goFloor = x
						direction = "DOWN"
					elif (lastFloor < goFloor) and (x < goFloor) and (x > lastFloor) and (y!=1):
						goFloor = x
					elif (lastFloor > goFloor) and (x > goFloor) and (x < lastFloor) and (y!=0):
						goFloor = x

		if (direction == "UP") and (x_max <= lastFloor):
			direction = "None"
		elif (direction == "DOWN") and (x_min >= lastFloor):
			direction = "None"

		checkFloor = elevator.get_floor_sensor_signal()
		if checkFloor >= 0:
			lastFloor = checkFloor

		print queue
		if (lastFloor == goFloor):
			if (direction == "None"):
				with(queueKey):
					queue[goFloor][0] = 0
					queue[goFloor][1] = 0
					queue[goFloor][2] = 0
			elif (direction == "UP"):
				with(queueKey):
					queue[goFloor][0] = 0
					queue[goFloor][2] = 0
			elif (direction == "DOWN"):
				with(queueKey):
					queue[goFloor][1] = 0
					queue[goFloor][2] = 0


def read_buttons_to_queue():
	while True:
		time.sleep(0.001)
		for floor in range (0,constants.N_FLOORS):
			for button in range(0,3):
				if (floor == 0 and button == 1) or (floor == 3 and button == 0):
					pass
				elif panel.get_button_signal(button,floor):
					with(queueKey):
						queue[floor][button]=1

def indicators():
	while True:
		time.sleep(0.001)
		for floor in range(0,constants.N_FLOORS):
				for button in range(0,3):
						if (floor == 0 and button == 1) or (floor == 3 and button == 0):
							pass
						elif queue[floor][button] == 1:
							panel.set_button_lamp(button,floor,1)
						else:
							panel.set_button_lamp(button,floor,0)
		
		if lastFloor == goFloor:
			panel.set_door_open_lamp(1)
		else:
			panel.set_door_open_lamp(0)

		panel.set_floor_indicator(lastFloor)


def go_to_floor():
	while True:
		time.sleep(0.001)
		if lastFloor >= 0:
			if lastFloor == goFloor:
				elevator.set_motor_direction(constants.DIRN_STOP)
				time.sleep(1)
			elif lastFloor < goFloor:
				elevator.set_motor_direction(constants.DIRN_UP)
			elif lastFloor > goFloor:
				elevator.set_motor_direction(constants.DIRN_DOWN)




def main():
	thread_1 = Thread(target = queue_floor, args = (),)
	thread_2 = Thread(target = read_buttons_to_queue, args = (),)
	thread_3 = Thread(target = indicators, args = (),)
	thread_6 = Thread(target = go_to_floor, args = (),)

	thread_1.start()
	thread_2.start()
	thread_3.start()
	thread_6.start()

	thread_1.join()
	thread_2.join()
	thread_3.join()
	thread_6.join()


if __name__ == "__main__":
    main()