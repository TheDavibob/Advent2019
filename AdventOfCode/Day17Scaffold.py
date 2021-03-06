import IntcodeComputer as ic
import numpy as np
import matplotlib.pyplot as plt

class Scaffold():
    def __init__(self):
        self.map_string = ''
        self.map = []
        self.camera = []

    def initialise_camera(self, camera_string):
        self.camera = ic.IntCode(camera_string)

    def run_camera(self):
        # Runs the camera, generating a map string
        while not self.camera.is_finished:
            output = self.camera.process_until_output()
            if self.camera.is_finished:
                break
            self.map_string = self.map_string + chr(output)

    def convert_mapstring_to_map(self):
        string_list = self.map_string.split('\n')
        width = len(string_list[0])
        height = len(string_list)
        self.map = -1*np.ones([height, width])
        for row, _ in enumerate(string_list):
            for column, _ in enumerate(string_list[row]):
                character = string_list[row][column]
                if character == '.':
                    continue
                elif character == '#':
                    self.map[row, column] = 0
                elif character == '^':
                    self.map[row, column] = 1
                elif character == '>':
                    self.map[row, column] = 2
                elif character == '<':
                    self.map[row, column] = 3
                elif character == 'v':
                    self.map[row, column] = 4

    def find_intersection(self):
        # Assumes a populated map
        logical_map = self.map > -1
        adjacent_map = np.zeros(logical_map.shape)
        adjacent_map[1:-2, 1:-2] = \
            logical_map[1:-2, 1:-2] * \
            logical_map[0:-3, 1:-2] * \
            logical_map[2:-1, 1:-2] * \
            logical_map[1:-2, 0:-3] * \
            logical_map[1:-2, 0:-3]

        return np.argwhere(adjacent_map)

    def return_intersection_output(self):
        intersection_list = self.find_intersection()
        return sum([intersection[0]*intersection[1] for intersection in intersection_list])

    def plot_map(self):
        plt.imshow(self.map)
        plt.show()

    def wake_robot(self, int_string):
        string_list = [letter for letter in int_string]
        string_list[0] = str(2)
        new_string = ''.join(string_list)
        self.initialise_camera(new_string)

    def convert_string_to_input(self, input_string):
        # Converts a string to an ASCII thing
        # String: 'a,b,c,...'
        return [ord(letter) for letter in input_string]

    def set_main_movement_routine(self, main_routine_string):
        self.main_movement_routine = self.convert_string_to_input(main_routine_string)
        self.main_movement_routine.append(10)

    def set_movement_functions(self, a_string, b_string, c_string):
        self.movement_A = self.convert_string_to_input(a_string)
        self.movement_B = self.convert_string_to_input(b_string)
        self.movement_C = self.convert_string_to_input(c_string)
        self.movement_A.append(10)
        self.movement_B.append(10)
        self.movement_C.append(10)

    def setup_computer(self, camera_string, main_routine_string, a_string, b_string, c_string, visualise = False):
        self.wake_robot(camera_string)
        self.set_main_movement_routine(main_routine_string)
        self.set_movement_functions(a_string, b_string, c_string)
        if visualise:
            self.visualise = [ord('y')]
        else:
            self.visualise = [ord('n')]

    def run_computer(self):
        # Assumes computer set up as previous
        self.camera.inputs = (
                self.main_movement_routine +
                self.movement_A +
                self.movement_B +
                self.movement_C +
                self.visualise
                )

        return self.camera.process_until_output()


test = Scaffold()
camera_string = '1,330,331,332,109,3546,1101,1182,0,15,1101,1439,0,24,1002,0,1,570,1006,570,36,1001,571,0,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,15,1,15,1008,15,1439,570,1006,570,14,21101,0,58,0,1105,1,786,1006,332,62,99,21102,1,333,1,21102,73,1,0,1106,0,579,1101,0,0,572,1101,0,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1001,574,0,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1105,1,81,21102,340,1,1,1105,1,177,21101,0,477,1,1106,0,177,21102,514,1,1,21101,0,176,0,1105,1,579,99,21101,184,0,0,1106,0,579,4,574,104,10,99,1007,573,22,570,1006,570,165,102,1,572,1182,21102,375,1,1,21101,0,211,0,1106,0,579,21101,1182,11,1,21101,0,222,0,1106,0,979,21101,0,388,1,21102,233,1,0,1105,1,579,21101,1182,22,1,21101,244,0,0,1105,1,979,21102,1,401,1,21101,0,255,0,1106,0,579,21101,1182,33,1,21102,266,1,0,1106,0,979,21102,414,1,1,21102,1,277,0,1105,1,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21101,0,1182,1,21102,1,313,0,1106,0,622,1005,575,327,1101,1,0,575,21101,327,0,0,1106,0,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,22,42,0,109,4,1201,-3,0,587,20101,0,0,-1,22101,1,-3,-3,21102,1,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1105,1,597,109,-4,2106,0,0,109,5,2101,0,-4,629,21002,0,1,-2,22101,1,-4,-4,21101,0,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21002,0,1,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21102,1,702,0,1105,1,786,21201,-1,-1,-1,1105,1,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21102,731,1,0,1106,0,786,1105,1,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21101,756,0,0,1105,1,786,1105,1,774,21202,-1,-11,1,22101,1182,1,1,21102,1,774,0,1106,0,622,21201,-3,1,-3,1105,1,640,109,-5,2106,0,0,109,7,1005,575,802,21002,576,1,-6,21002,577,1,-5,1106,0,814,21102,1,0,-1,21101,0,0,-5,21102,0,1,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,49,-3,22201,-6,-3,-3,22101,1439,-3,-3,1201,-3,0,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21101,0,1,-1,1105,1,924,1205,-2,873,21102,1,35,-4,1105,1,924,2102,1,-3,878,1008,0,1,570,1006,570,916,1001,374,1,374,2102,1,-3,895,1102,2,1,0,1201,-3,0,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,921,21001,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,49,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,43,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1102,1,1,575,21101,0,973,0,1105,1,786,99,109,-7,2106,0,0,109,6,21101,0,0,-4,21102,0,1,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1106,0,1041,21102,1,-4,-2,1106,0,1041,21102,1,-5,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,1202,-2,1,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,2102,1,-2,0,1106,0,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1105,1,989,21102,1,439,1,1106,0,1150,21101,477,0,1,1106,0,1150,21101,0,514,1,21101,0,1149,0,1106,0,579,99,21101,1157,0,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,2102,1,-5,1176,2102,1,-4,0,109,-6,2105,1,0,26,5,44,1,3,1,44,1,3,1,44,1,3,1,44,1,3,1,44,1,3,1,44,7,46,1,1,1,44,11,38,1,1,1,1,1,5,1,28,13,1,1,5,1,28,1,9,1,3,1,5,1,28,1,9,7,3,1,28,1,13,1,1,1,3,1,28,1,13,1,1,1,3,1,28,1,13,1,1,1,3,1,16,13,13,1,1,1,3,1,16,1,25,1,1,1,3,1,10,11,21,7,10,1,5,1,3,1,23,1,14,1,5,1,3,1,23,1,3,7,4,1,5,1,3,1,23,1,3,1,5,1,4,7,3,1,23,1,3,1,5,1,14,1,23,1,3,1,5,1,14,1,23,11,14,1,27,1,20,1,27,1,3,7,10,1,27,1,3,1,5,1,10,1,25,5,1,1,5,1,10,1,25,1,1,1,1,1,1,1,5,1,10,7,19,1,1,11,16,1,19,1,3,1,1,1,22,1,13,13,22,1,13,1,5,1,3,1,24,1,13,1,5,1,3,1,24,1,13,1,9,1,24,1,13,1,9,1,24,1,13,1,9,1,24,1,13,11,24,1,48,1,48,1,48,7,26'
test.initialise_camera(camera_string)
test.run_camera()
test.convert_mapstring_to_map()

# Needs figuring out
main_routine_string = 'A,B,C,A,B,C,A'
A_string = 'L,6,R,12,L,6'
B_string = 'R,12,L,10'
C_string = 'L,4,L,6'

test.setup_computer(camera_string, main_routine_string, A_string, B_string, C_string, True)
print(test.run_computer())