import ElevInterface
import PanelInterface
import constants

elevator = ElevInterface.ElevInterface()
panel = PanelInterface.PanelInterface()

def go_to_floor(nextFloor):
	
	lastFloor = elevator.get_floor_sensor_signal()

	if lastFloor >= 0:
		if lastFloor == nextFloor:
			elevator.set_motor_direction(constants.DIRN_STOP)
			#print 'you reached your destination'
			panel.set_door_open_lamp(1)
			return 0
		elif lastFloor < nextFloor:
			panel.set_door_open_lamp(0)
			elevator.set_motor_direction(constants.DIRN_UP)
			#print 'goin up to %i, last floor is %i' % (nextFloor, lastFloor) 
		elif lastFloor > nextFloor:
			panel.set_door_open_lamp(0)
			elevator.set_motor_direction(constants.DIRN_DOWN)
			#print 'goin down to %i, last floor is %i' % (nextFloor, lastFloor)
		else:
			elevator.set_motor_direction(constants.DIRN_UP)

	if panel.get_stop_signal() == 1:
		elevator.set_motor_direction(constants.DIRN_STOP)
		return 0	
		
def last_floor():
	return elevator.get_floor_sensor_signal()
