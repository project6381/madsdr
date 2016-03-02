import panel
import elevator
import constants
import time
from threading import Thread
from threading import Lock


queueKey = Lock()
queue = [[0 for y in range(0,3)] for x in range(0,constants.N_FLOORS)]
goFloor = 2


def queue_floor():
	global goFloor
	lastFloor = 2
	direction = "None"
	while True:
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

		checkFloor = elevator.last_floor()
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
				time.sleep(1)
			elif (direction == "DOWN"):
				with(queueKey):
					queue[goFloor][1] = 0
					queue[goFloor][2] = 0
				time.sleep(1)


def set_queue():
	while True:
		(floor,button) = panel.read_buttons()
		if (floor >= 0) and (button >= 0):
			queueKey.acquire()
			queue[floor][button]=1
			queueKey.release()

def go_queue():
	global goFloor
	while True:
		elevator.go_to_floor(goFloor)


def main():
	thread_1 = Thread(target = queue_floor, args = (),)
	thread_2 = Thread(target = set_queue, args = (),)
	thread_3 = Thread(target = go_queue, args = (),)

	thread_1.start()
	thread_2.start()
	thread_3.start()

	thread_1.join()
	thread_2.join()
	thread_3.join()


if __name__ == "__main__":
    main()