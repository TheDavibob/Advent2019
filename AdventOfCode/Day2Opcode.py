def analyse_opcode(opcode):
    lead_position = 0
    while lead_position < len(opcode)-3:
        idx_1 = opcode[lead_position + 1]
        idx_2 = opcode[lead_position + 2]
        update_idx = opcode[lead_position + 3]
        if update_idx > len(opcode) - 1:
            print("invalid code")
            return opcode

        if opcode[lead_position] == 1:
            opcode[update_idx] = opcode[idx_1] + opcode[idx_2]
            lead_position = lead_position + 4
        elif opcode[lead_position] == 2:
            opcode[update_idx] = opcode[idx_1] * opcode[idx_2]
            lead_position = lead_position + 4
        elif opcode[lead_position] == 99:
            return opcode
        else:
            print("invalid code found")
            return opcode

    return opcode


opcode_to_use = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,19,5,23,2,6,23,27,1,6,27,31,2,31,9,35,1,35,6,39,1,10,39,43,2,9,43,47,1,5,47,51,2,51,6,55,1,5,55,59,2,13,59,63,1,63,5,67,2,67,13,71,1,71,9,75,1,75,6,79,2,79,6,83,1,83,5,87,2,87,9,91,2,9,91,95,1,5,95,99,2,99,13,103,1,103,5,107,1,2,107,111,1,111,5,0,99,2,14,0,0]
opcode_to_use[1] = 12
opcode_to_use[2] = 2

opcode = analyse_opcode(opcode_to_use)

def index_0(index_1, index_2):
    opcode_to_use = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 19, 5, 23, 2, 6, 23, 27, 1, 6, 27,
                     31, 2, 31, 9, 35, 1, 35, 6, 39, 1, 10, 39, 43, 2, 9, 43, 47, 1, 5, 47, 51, 2, 51, 6, 55, 1, 5, 55,
                     59, 2, 13, 59, 63, 1, 63, 5, 67, 2, 67, 13, 71, 1, 71, 9, 75, 1, 75, 6, 79, 2, 79, 6, 83, 1, 83, 5,
                     87, 2, 87, 9, 91, 2, 9, 91, 95, 1, 5, 95, 99, 2, 99, 13, 103, 1, 103, 5, 107, 1, 2, 107, 111, 1,
                     111, 5, 0, 99, 2, 14, 0, 0]
    opcode_to_use[1] = index_1
    opcode_to_use[2] = index_2

    opcode = analyse_opcode(opcode_to_use)
    return opcode[0]

for index_1 in range(99):
    for index_2 in range(99):
        if index_0(index_1, index_2) == 19690720:
            print(index_1, index_2)
            break
