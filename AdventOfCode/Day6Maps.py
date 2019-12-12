def split_input(orbit_map):
    # Splits an input (assumed a multiline string) into objects, and things orbiting those objects
    # Doesn't do anything more than split the strings
    line_by_line = orbit_map.split('\n')
    first_argument = [x.split(')')[0] for x in line_by_line]
    second_argument = [x.split(')')[1] for x in line_by_line]

    # Outputs later refered to as orbitee, orbiter
    return first_argument, second_argument


def find_central_orbit(orbitee, orbiter):
    central_orbiter_list = [x for x in orbitee if x not in orbiter]
    if len(central_orbiter_list) == 1:
        return central_orbiter_list[0]


def find_all_orbiters(planet, orbitee, orbiter):
    # finds all objects that orbit planet
    return [x for n, x in enumerate(orbiter) if orbitee[n] == planet]


## Main script
def count_orbits(orbit_map):
    orbitee, orbiter = split_input(orbit_map)

    # orbiter is the 'correct' length and contains all the element of interest, so we will use it to store distances
    all_planets = orbiter.copy()
    all_planets.insert(0, find_central_orbit(orbitee, orbiter))

    num_connections = [-1 for _ in all_planets]
    num_connections[0] = 0 # Central orbiter is not connected to anything

    idx = 0
    while min(num_connections) == -1:
        if num_connections[idx] != -1:
            # This planet has been assigned a distance
            orbiting_planets = find_all_orbiters(all_planets[idx], orbitee, orbiter)
            for n, x in enumerate(all_planets):
                if x in orbiting_planets:
                    num_connections[n] = num_connections[idx] + 1

        idx += 1
        if idx == len(num_connections):
            idx = 0

    return num_connections


def find_orbitee(planet, orbitee, orbiter):
    # Finds thing which planet is orbiting
    return orbitee[next(n for n, x in enumerate(orbiter) if x == planet)]


def trace_to_center(planet, orbitee, orbiter):
    central_planet = find_central_orbit(orbitee, orbiter)
    trace = [planet]

    while trace[-1] != central_planet:
        trace = trace + [find_orbitee(trace[-1], orbitee, orbiter)]

    return trace


def path_length(planet1, planet2, orbit_map):
    orbitee, orbiter = split_input(orbit_map)

    trace1 = trace_to_center(planet1, orbitee, orbiter)
    trace2 = trace_to_center(planet2, orbitee, orbiter)

    unique1 = [x for x in trace1 if x not in trace2]
    unique2 = [x for x in trace2 if x not in trace1]

    # This cuts out the intersection point and includes the end points, so need: (note, counting transfers)
    return len(unique1) + len(unique2) - 2