import panel
import elevator

def main():
	#floorDestination = int(raw_input("->"))

	nextFloor = 1
	lastFloor = 1
	goFloor = 1
	printFloor = 1


	while True:
	
		#lastFloor = elevator.last_floor()
		nextFloor = panel.read_buttons()
		if nextFloor >= 0:
			goFloor = nextFloor
			if nextFloor != printFloor:
				print (goFloor, lastFloor)
				printFloor = goFloor
		elevator.go_to_floor(goFloor)
		


if __name__ == "__main__":
    main()