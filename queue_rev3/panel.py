import PanelInterface
import constants

panel = PanelInterface.PanelInterface()

def read_buttons():

	for floor in range (0,constants.N_FLOORS):
		for button in range(0,3):
			if (floor == 0 and button == 1) or (floor == 3 and button == 0):
				pass
			elif panel.get_button_signal(button,floor):
				return (floor,button)
	return (-1,-1)