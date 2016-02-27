import panel
import elevator
import constants
import time
from threading import Thread
from threading import Lock


queueKey = Lock()
queue = {}


def queue_floor():
	goFloor = 2
	lastFloor = 2
	direction = "None"
	while True:
		x_max = 0
		x_min = constants.N_FLOORS-1

		for x in range(0,constants.N_FLOORS):
			if (x in queue) and queue[x] == 1:
				x_max = max(x_max,x)
				x_min = min(x_min,x)
				if (lastFloor == goFloor) and (direction != "DOWN") and (goFloor < x_max):
					goFloor = x
					direction = "UP"
				elif (lastFloor == goFloor) and (direction != "UP") and (goFloor > x_min):
					goFloor = x
					direction = "DOWN"
				elif (lastFloor < goFloor) and (x < goFloor) and (x > lastFloor):
					goFloor = x
				elif (lastFloor > goFloor) and (x > goFloor) and (x < lastFloor):
					goFloor = x
			else:
				queueKey.acquire()
				queue[x]=0
				queueKey.release()

		if (direction == "UP") and (x_max <= lastFloor):
			direction = "None"
		elif (direction == "DOWN") and (x_min >= lastFloor):
			direction = "None"

		checkFloor = elevator.last_floor()
		if checkFloor >= 0:
			lastFloor = checkFloor 

		elevator.go_to_floor(goFloor)

		if (lastFloor == goFloor):
			queueKey.acquire()
			queue[goFloor] = 0
			queueKey.release()
			time.sleep(1)


def set_queue():

	while True:
		
		nextFloor = panel.read_buttons()
		if nextFloor >= 0:
			queueKey.acquire()
			queue[nextFloor]=1
			queueKey.release()



def main():
	thread_1 = Thread(target = queue_floor, args = (),)
	thread_2 = Thread(target = set_queue, args = (),)

	thread_1.start()
	thread_2.start()

	thread_1.join()
	thread_2.join()


if __name__ == "__main__":
    main()