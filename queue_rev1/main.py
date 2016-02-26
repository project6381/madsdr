import panel
import elevator
import constants
import time
from threading import Thread
from threading import Lock


mutexKey = Lock()
queue = {}

for x in range(0, constants.N_FLOORS):
	queue[x] = 0
print queue


def set_floor():
	goFloor = 1
	while True:
		mutexKey.acquire()
		for x in range(0,constants.N_FLOORS):
			if (x in queue) and queue[x] == 1:
				if lastFloor == goFloor:
					goFloor = x
					print (goFloor, 1)
				elif (lastFloor < goFloor) and (x < goFloor) and (x > lastFloor):
					goFloor = x
					print (goFloor, 2)
				elif (lastFloor > goFloor) and (x > goFloor) and (x < lastFloor):
					goFloor = x
					print (goFloor, 3)
		mutexKey.release()

		checkFloor = elevator.last_floor()
		if checkFloor >= 0:
			lastFloor = checkFloor 

		elevator.go_to_floor(goFloor)

		if (lastFloor == goFloor):
			mutexKey.acquire()
			queue[goFloor] = 0
			time.sleep(1)
			mutexKey.release()


		#mutexKey.acquire()	
		#print (queue)
		#mutexKey.release()


def set_queue():

	while True:
		
		nextFloor = panel.read_buttons()
		if nextFloor >= 0:
			mutexKey.acquire()
			queue[nextFloor]=1
			mutexKey.release()



def main():
	thread_1 = Thread(target = set_floor, args = (),)
	thread_2 = Thread(target = set_queue, args = (),)

	thread_1.start()
	thread_2.start()

	thread_1.join()
	thread_2.join()


if __name__ == "__main__":
    main()