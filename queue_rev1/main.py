import panel
import elevator

def main():
	#floorDestination = int(raw_input("->"))

	nextFloor=1
	lastFloor=1

	while True:
	
		lastFloor = elevator.last_floor()
		if panel.read_buttons() >= 0:
			nextFloor = panel.read_buttons()
			elevator.go_to_floor(nextFloor)
		print 'Next floor %i, Last floor %i' % (nextFloor, lastFloor)




		


if __name__ == "__main__":
    main()