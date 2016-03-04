import comedi as c
import constants as const

#in port 4
PORT_4_SUBDEVICE = 3
PORT_4_CHANNEL_OFFSET = 16
PORT_4_DIRECTION = c.INPUT
OBSTRUCTION = (0x300+23)
STOP = (0x300+22)
BUTTON_COMMAND1 = (0x300+21)
BUTTON_COMMAND2 = (0x300+20)
BUTTON_COMMAND3 = (0x300+19)
BUTTON_COMMAND4 = (0x300+18)
BUTTON_UP1 = (0x300+17)
BUTTON_UP2 = (0x300+16)

#in port 1
PORT_1_SUBDEVICE = 2
PORT_1_CHANNEL_OFFSET = 0
PORT_1_DIRECTION = c.INPUT
BUTTON_DOWN2 = (0x200+0)
BUTTON_UP3 = (0x200+1)
BUTTON_DOWN3 = (0x200+2)
BUTTON_DOWN4 = (0x200+3)
SENSOR_FLOOR1 = (0x200+4)
SENSOR_FLOOR2 = (0x200+5)
SENSOR_FLOOR3 = (0x200+6)
SENSOR_FLOOR4 = (0x200+7)

#out port 3
PORT_3_SUBDEVICE = 3
PORT_3_CHANNEL_OFFSET = 8
PORT_3_DIRECTION = c.OUTPUT
MOTORDIR = (0x300+15)
LIGHT_STOP = (0x300+14)
LIGHT_COMMAND1 = (0x300+13)
LIGHT_COMMAND2 = (0x300+12)
LIGHT_COMMAND3 = (0x300+11)
LIGHT_COMMAND4 = (0x300+10)
LIGHT_UP1 = (0x300+9)
LIGHT_UP2 = (0x300+8)

#out port 2
PORT_2_SUBDEVICE = 3
PORT_2_CHANNEL_OFFSET = 0
PORT_2_DIRECTION = c.OUTPUT
LIGHT_DOWN2 = (0x300+7)
LIGHT_UP3 = (0x300+6)
LIGHT_DOWN3 = (0x300+5)
LIGHT_DOWN4 = (0x300+4)
LIGHT_DOOR_OPEN = (0x300+3)
LIGHT_FLOOR_IND2 = (0x300+1)
LIGHT_FLOOR_IND1 = (0x300+0)

#out port 0
MOTOR =  (0x100+0)

#non-existing ports (for alignment)
BUTTON_DOWN1 = -1
BUTTON_UP4 = -1
LIGHT_DOWN1 =  -1
LIGHT_UP4 = -1



button_channel_matrix = [[0 for x in range(const.N_BUTTONS)] for x in range(const.N_FLOORS)]
lamp_channel_matrix = [[0 for x in range(const.N_BUTTONS)] for x in range(const.N_FLOORS)]


button_channel_matrix[0][0] = BUTTON_UP1
button_channel_matrix[0][1] = BUTTON_DOWN1
button_channel_matrix[0][2] = BUTTON_COMMAND1
button_channel_matrix[1][0] = BUTTON_UP2
button_channel_matrix[1][1] = BUTTON_DOWN2
button_channel_matrix[1][2] = BUTTON_COMMAND2
button_channel_matrix[2][0] = BUTTON_UP3
button_channel_matrix[2][1] = BUTTON_DOWN3
button_channel_matrix[2][2] = BUTTON_COMMAND3
button_channel_matrix[3][0] = BUTTON_UP4
button_channel_matrix[3][1] = BUTTON_DOWN4
button_channel_matrix[3][2] = BUTTON_COMMAND4

lamp_channel_matrix[0][0] = LIGHT_UP1
lamp_channel_matrix[0][1] = LIGHT_DOWN1
lamp_channel_matrix[0][2] = LIGHT_COMMAND1
lamp_channel_matrix[1][0] = LIGHT_UP2
lamp_channel_matrix[1][1] = LIGHT_DOWN2
lamp_channel_matrix[1][2] = LIGHT_COMMAND2
lamp_channel_matrix[2][0] = LIGHT_UP3
lamp_channel_matrix[2][1] = LIGHT_DOWN3
lamp_channel_matrix[2][2] = LIGHT_COMMAND3
lamp_channel_matrix[3][0] = LIGHT_UP4
lamp_channel_matrix[3][1] = LIGHT_DOWN4
lamp_channel_matrix[3][2] = LIGHT_COMMAND4