import numpy as np

## Sanitise input to something we actually like
def convert_map_to_array(asteroid_map):
    # Converts input to array of zeros and ones
    rows = asteroid_map.split('\n')
    height = len(rows)
    width = len(rows[0])

    # initialise array
    map_array = np.zeros([height, width])

    for idx_h in range(height):
        for idx_w in range(width):
            if rows[idx_h][idx_w] == '#':
                map_array[idx_h, idx_w] = 1

    return map_array


def is_blocked(map_array, idx_1, idx_2):
    # Checks if there are any asteroids in a line between idx_1 and idx_2
    displacement = [y - x for x, y in zip(idx_1, idx_2)]
    # Find any minimal steps
    divisor = np.gcd(displacement[0], displacement[1])
    step = displacement/divisor
    # This is a 'unit step' in the direction from idx_1 to idx_2

    blockage = False
    for step_idx in range(1,divisor):
        x_idx = int(idx_1[0] + step_idx*step[0])
        y_idx = int(idx_1[1] + step_idx * step[1])
        if map_array[x_idx, y_idx] == 1:
            blockage = True
            break

    return blockage


def blockage_count(map_array, idx):
    # Counts number of visible asteroids from asteroid at idx
    width = map_array.shape[1]
    height = map_array.shape[0]

    counter = np.zeros([height, width])

    if map_array[idx[0], idx[1]] == 0:
        # This is not an asteroid
        return counter

    for idx_w in range(width):
        for idx_h in range(height):
            if idx_h == idx[0] and idx_w == idx[1]:
                # Same position as one we want, ignore
                pass
            elif map_array[idx_h, idx_w] == 0:
                # Don't care, no asteroid
                pass
            else:
                counter[idx_h, idx_w] = not is_blocked(map_array, idx, [idx_h, idx_w])

    return counter


def count_over_map(map_array):
    width = map_array.shape[1]
    height = map_array.shape[0]

    counter = np.zeros([height, width])

    for idx_w in range(width):
        for idx_h in range(height):
            counter[idx_h, idx_w] = np.sum(blockage_count(map_array,[idx_h, idx_w]))

    return counter


def find_best_position(asteroid_map):
    map_array = convert_map_to_array(asteroid_map)
    map_counter = count_over_map(map_array)
    position = np.where(map_counter == np.amax(map_counter))
    print('x position = ' + str(int(position[1])) + ' and y position = ' + str(int(position[0])) + '. Number of asteroids visible = ' + str(int(np.amax(map_counter))))

    return position, map_counter

input_string = '''....#.....#.#...##..........#.......#......
.....#...####..##...#......#.........#.....
.#.#...#..........#.....#.##.......#...#..#
.#..#...........#..#..#.#.......####.....#.
##..#.................#...#..........##.##.
#..##.#...#.....##.#..#...#..#..#....#....#
##...#.............#.#..........#...#.....#
#.#..##.#.#..#.#...#.....#.#.............#.
...#..##....#........#.....................
##....###..#.#.......#...#..........#..#..#
....#.#....##...###......#......#...#......
.........#.#.....#..#........#..#..##..#...
....##...#..##...#.....##.#..#....#........
............#....######......##......#...#.
#...........##...#.#......#....#....#......
......#.....#.#....#...##.###.....#...#.#..
..#.....##..........#..........#...........
..#.#..#......#......#.....#...##.......##.
.#..#....##......#.............#...........
..##.#.....#.........#....###.........#..#.
...#....#...#.#.......#...#.#.....#........
...####........#...#....#....#........##..#
.#...........#.................#...#...#..#
#................#......#..#...........#..#
..#.#.......#...........#.#......#.........
....#............#.............#.####.#.#..
.....##....#..#...........###........#...#.
.#.....#...#.#...#..#..........#..#.#......
.#.##...#........#..#...##...#...#...#.#.#.
#.......#...#...###..#....#..#...#.........
.....#...##...#.###.#...##..........##.###.
..#.....#.##..#.....#..#.....#....#....#..#
.....#.....#..............####.#.........#.
..#..#.#..#.....#..........#..#....#....#..
#.....#.#......##.....#...#...#.......#.#..
..##.##...........#..........#.............
...#..##....#...##..##......#........#....#
.....#..........##.#.##..#....##..#........
.#...#...#......#..#.##.....#...#.....##...
...##.#....#...........####.#....#.#....#..
...#....#.#..#.........#.......#..#...##...
...##..............#......#................
........................#....##..#........#'''

find_best_position(input_string)



## moving on to part 2

def assign_range_and_angle(map_array, idx):
    # Given initial asteroid location, computes range and inclination of all other asteroids
    width = map_array.shape[1]
    height = map_array.shape[0]

    ranges = np.zeros([height, width])
    angles = np.zeros([height, width])

    for idx_w in range(width):
        for idx_h in range(height):
            if map_array[idx_h, idx_w] == 0:
                ranges[idx_h, idx_w] = -100
                angles[idx_h, idx_w] = -100
            elif idx_h == idx[0] and idx_w == idx[1]:
                ranges[idx_h, idx_w] = -100
                angles[idx_h, idx_w] = -100
            else:
                rel_position = [
                    idx_h - idx[0],
                    idx_w - idx[1]
                ]
                ranges[idx_h, idx_w] = rel_position[0]**2 + rel_position[1]**2
                angles[idx_h, idx_w] = round(np.pi - np.arctan2(rel_position[1], rel_position[0]),5)

    return ranges, angles


def sort_by_angle_then_range(map_array, ranges, angles):
    range_list = ranges.flatten().tolist()
    angles_list = angles.flatten().tolist()

    position_list = len(angles_list)*[0]
    for idx in range(len(position_list)):
        if angles_list[idx] == -100:
            position_list[idx] = -1

    angles_set = list(set(angles_list))
    angles_set.sort()
    if angles_set[0] == -100:
        angles_set.pop(0)

    position = 1

    while 0 in position_list:
        for angle in angles_set:
            # Find angles in angles_list
            ang_idx = [n for n, list_angle in enumerate(angles_list) if list_angle == angle]
            if len(ang_idx) > 0:
                list_ranges = [range for n, range in enumerate(range_list) if n in ang_idx]
                min_range_idx = ang_idx[np.argmin(list_ranges)]
                position_list[min_range_idx] = position
                range_list[min_range_idx] = -100
                angles_list[min_range_idx] = -100
                position += 1

    return np.asarray(position_list).reshape(ranges.shape)


def find_nth_asteroid(asteroid_map, idx, n):
    map_array = convert_map_to_array(asteroid_map)
    ranges, angles = assign_range_and_angle(map_array, idx)

    position_array = sort_by_angle_then_range(map_array, ranges, angles)

    coordinate = np.where(position_array == n)
    print('(' + str(int(coordinate[1])) + ',' + str(int(coordinate[0])) + ')')

    return coordinate