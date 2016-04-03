from constants import N_ELEVATORS, N_FLOORS, DIRN_DOWN, DIRN_STOP, DIRN_UP, LAST_FLOOR, NEXT_FLOOR, DIRECTION
from threading import Thread, Lock
from thread import interrupt_main
from random import randint
import time


class MasterDriver:
	def __init__(self):
		self.__elevator_positions = [[0 for position in range(0,3)] for elevator in range(0,N_ELEVATORS)]
		self.__button_orders = [0 for floor in range(0,N_FLOORS*2)]
		self.__elevator_orders = [0 for button in range(0,N_FLOORS*2)]
		self.__elevator_online = [1 for elevator in range(0,N_ELEVATORS)]


	def order_elevator(self, button_orders, elevator_positions, elevator_online):
		self.__button_orders = button_orders
		self.__elevator_positions = elevator_positions
		self.__elevator_online = elevator_online
					
		# UP button calls
		for floor in range(0,N_FLOORS):
			if self.__button_orders[floor] == 0:
				self.__elevator_orders[floor] = 0
			if (self.__button_orders[floor] == 1) and ((self.__elevator_orders[floor] == 0) or (self.__elevator_online[self.__elevator_orders[floor]-1] == 0)):
				elevator_priority = [0 for elevator in range(0,N_ELEVATORS)]
				for elevator in range(0,N_ELEVATORS):
					if self.__elevator_online[elevator] == 0:
						elevator_priority[elevator] = 0
					elif (self.__elevator_positions[elevator][LAST_FLOOR] == floor) and (self.__elevator_positions[elevator][NEXT_FLOOR] == floor) and ((self.__elevator_positions[elevator][DIRECTION] == DIRN_STOP) or (self.__elevator_positions[elevator][DIRECTION] == DIRN_DOWN)):
						elevator_priority[elevator] = 19
					elif (floor < N_FLOORS) and (self.__elevator_positions[elevator][LAST_FLOOR] < floor) and (self.__elevator_positions[elevator][DIRECTION] == DIRN_UP):
						elevator_priority[elevator] = 15 + (3 - abs(self.__elevator_positions[elevator][LAST_FLOOR]-floor))					
					elif (self.__elevator_positions[elevator][DIRECTION] == DIRN_STOP):
						elevator_priority[elevator] = 11 + (3 - abs(self.__elevator_positions[elevator][LAST_FLOOR]-floor))
					else:
						elevator_priority[elevator] = 1 + randint(0,9)
				print ("Up button calls floor: %i" % floor)
				print elevator_priority
				for elevator in range(0,N_ELEVATORS):
					if elevator == 0:
						if (self.__elevator_online[elevator] == 1):
							self.__elevator_orders[floor] = elevator+1
					elif (elevator_priority[elevator] > elevator_priority[elevator-1]) and (self.__elevator_online[elevator] == 1):
						self.__elevator_orders[floor] = elevator+1


				
		# DOWN button calls
		for floor in range(N_FLOORS,N_FLOORS*2):
			if self.__button_orders[floor] == 0:
				self.__elevator_orders[floor] = 0

			if (self.__button_orders[floor] == 1) and  ((self.__elevator_orders[floor] == 0) or (self.__elevator_online[self.__elevator_orders[floor]-1] == 0)):
				elevator_priority = [0 for elevator in range(0,N_ELEVATORS)]
				for elevator in range(0,N_ELEVATORS):
					if self.__elevator_online[elevator] == 0:
						elevator_priority[elevator] = 0
					elif (self.__elevator_positions[elevator][LAST_FLOOR] == floor-N_FLOORS) and (self.__elevator_positions[elevator][NEXT_FLOOR] == floor-N_FLOORS) and ((self.__elevator_positions[elevator][DIRECTION] == DIRN_STOP) or (self.__elevator_positions[elevator][DIRECTION] == DIRN_DOWN)):
						elevator_priority[elevator] = 19
					elif (floor-N_FLOORS > N_FLOORS) and (self.__elevator_positions[elevator][LAST_FLOOR] > floor-N_FLOORS) and (self.__elevator_positions[elevator][DIRECTION] == DIRN_DOWN):
						elevator_priority[elevator] = 15 + (3 - abs(self.__elevator_positions[elevator][LAST_FLOOR]-floor-N_FLOORS))	
					elif (self.__elevator_positions[elevator][DIRECTION] == DIRN_STOP):
						elevator_priority[elevator] = 11 + (3 - abs(self.__elevator_positions[elevator][LAST_FLOOR]-floor-N_FLOORS))	
					else:
						elevator_priority[elevator] = 1 + randint(0,9)
				print ("Down button calls floor: %i" % (floor-N_FLOORS))
				print elevator_priority
				for elevator in range(0,N_ELEVATORS):
					if elevator == 0:
						if (self.__elevator_online[elevator] == 1):
							self.__elevator_orders[floor] = elevator+1
					elif (elevator_priority[elevator] > elevator_priority[elevator-1]) and (self.__elevator_online[elevator] == 1):
						self.__elevator_orders[floor] = elevator+1

		return self.__elevator_orders

		