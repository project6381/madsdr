import PanelInterface

panel = PanelInterface.PanelInterface()

def read_buttons():

	for floor in range (0,4):
		for button in range(0,3):
			if (floor == 0 and button == 1) or (floor == 3 and button == 0):
				pass
			elif panel.get_button_signal(button,floor):
				lastFloor = floor
				return floor