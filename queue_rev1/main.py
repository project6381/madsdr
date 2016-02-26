import panel
import elevator

def main():
	#floorDestination = int(raw_input("->"))

	goFloor = 1

	while True:
	
		#lastFloor = elevator.last_floor()
		nextFloor = panel.read_buttons()
		if nextFloor >= 0:
			goFloor = nextFloor
		elevator.go_to_floor(goFloor)

		

if __name__ == "__main__":
    main()