import panel
import elevator
import constants
from threading import Thread
from threading import Lock

queue = {}

mutexKey = Lock()

def set_floor():
	goFloor = 1
	while True:
		#mutexKey.acquire()
		for x in range(0,constants.N_FLOORS):
			if (x in queue) and queue[x] == 1:
				if lastFloor == goFloor:
					goFloor = x
					print (goFloor)
				elif (x < goFloor) and (lastFloor < goFloor):
					goFloor = x
					print (goFloor)
				elif (x > goFloor) and (lastFloor > goFloor):
					goFloor = x
					print (goFloor)
		#mutexKey.release()

		elevator.go_to_floor(goFloor)

		lastFloor = elevator.last_floor()
		if (lastFloor == goFloor):
			#mutexKey.acquire()
			queue[goFloor] = 0
			#mutexKey.release()

		#mutexKey.acquire()	
		#print (queue)
		#mutexKey.release()


def set_queue():

	#mutexKey.acquire()
	for x in range(0, constants.N_FLOORS):
		queue[x] = 0
	print queue
	#mutexKey.release()
	while True:
		
		nextFloor = panel.read_buttons()
		if nextFloor >= 0:
			#mutexKey.acquire()
			queue[nextFloor]=1
			#mutexKey.release()



def main():
	thread_1 = Thread(target = set_floor, args = (),)
	thread_2 = Thread(target = set_queue, args = (),)

	thread_1.start()
	thread_2.start()

	thread_1.join()
	thread_2.join()


if __name__ == "__main__":
    main()