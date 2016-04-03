from master_driver import MasterDriver
import time
from random import randint


def main():
	#try:
		#time.sleep(3)
	driver = MasterDriver()
	button_orders = [0,0,0,0,0,0,0,0]
	elevator_positions = [[0,0,0],[0,0,0],[0,0,0]]
	elevator_orders = [0,0,0,0,0,0,0,0]
	elevator_online = [0,0,0]
	while True:
		
		for elevator in range(0,3):
			elevator_online[elevator]=randint(0,1)
			elevator_positions[elevator][0]=randint(0,3)
			elevator_positions[elevator][1]=randint(0,3)
			elevator_positions[elevator][2]=randint(0,2)
			if (elevator_positions[elevator][0] > elevator_positions[elevator][1]) and (elevator_positions[elevator][2]==2):
				elevator_positions[elevator][2]=0
			if (elevator_positions[elevator][0] < elevator_positions[elevator][1]) and (elevator_positions[elevator][2]==0):
				elevator_positions[elevator][2]=2
			if elevator_positions[elevator][2] == 1:
				elevator_positions[elevator][0]=elevator_positions[elevator][1]
			if (elevator_positions[elevator][0] == 0) and (elevator_positions[elevator][2] == 0):
				elevator_positions[elevator][2] == 1
			if (elevator_positions[elevator][0] == 3) and (elevator_positions[elevator][2] == 2):
				elevator_positions[elevator][2] == 1


		for order in range(0,8):
			button_orders[order]=randint(0,1)
			button_orders[3]=0
			button_orders[4]=0

		elevator_orders = driver.order_elevator(button_orders, elevator_positions, elevator_online)

		print "elevator_online"
		print elevator_online
		print "elevator_positions:"
		print elevator_positions
		print "button_orders:"
		print button_orders
		
		print "elevator_orders:"
		print elevator_orders
		print "\n"
		#print driver.read_position()

	#except KeyboardInterrupt:
	#	pass
	#except StandardError as error:
	#	print error
	#finally:
	#	print "exiting main"
		

if __name__ == "__main__":
		main()
	
		
