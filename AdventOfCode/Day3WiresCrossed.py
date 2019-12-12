## Will proceed by storing all previous positions

def move(pos_list, movestring):
    # Adds positions to pos_list according to movestring

    # pos_list a list of complex numbers
    current_pos = pos_list[-1]  # a complex number

    shift = int(movestring[1:])
    if movestring[0] == 'R':
        shift_list = [current_pos + x + 1 for x in range(shift)]
    elif movestring[0] == 'L':
        shift_list = [current_pos - x - 1 for x in range(shift)]
    elif movestring[0] == 'U':
        shift_list = [current_pos + 1j * (x + 1) for x in range(shift)]
    elif movestring[0] == 'D':
        shift_list = [current_pos - 1j * (x + 1) for x in range(shift)]

    return pos_list + shift_list


def full_move(movelist):
    pos_list = [0]
    for movestring in movelist:
        pos_list = move(pos_list, movestring)

    return (pos_list)


def intersections(movelist1, movelist2):
    positions1 = full_move(movelist1)
    positions2 = full_move(movelist2)
    return list(set(positions1) & set(positions2))


def min_intersection(movelist1, movelist2):
    intersects = intersections(movelist1, movelist2)
    distances = [abs(x.real) + abs(x.imag) for x in intersects]
    return min([distance for distance in distances if distance > 0])


text_import = open('Day3Input.txt')
imported_text = text_import.readlines()
movelist1 = imported_text[0].split(',')
movelist2 = imported_text[1].split(',')
min_intersection(movelist1, movelist2)


def timed_intersections(movelist1, movelist2):
    positions1 = full_move(movelist1)
    positions2 = full_move(movelist2)

    intersection_list = list(set(positions1) & set(positions2))
    pos_time = [next(n for n, x in enumerate(positions1) if x == intersection)
                + next(n for n, x in enumerate(positions2) if x == intersection)
                for intersection in intersection_list]

    return min(pos_time[1:])

print(timed_intersections(movelist1, movelist2))

