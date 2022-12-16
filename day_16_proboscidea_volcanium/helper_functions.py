
__author__ = "Maximilian Geitner"
__date__ = "16.12.2022"

from day_16_proboscidea_volcanium.valve import Valve


def bfs(start, dest, dict_v):
    queue_current = [start]
    list_visited = []
    queue_next = []
    dist_inner = 0
    # print("Start: ", start, dest)
    while len(queue_current) > 0:
        for cur in queue_current:
            # print("Found, ", cur)
            if cur == dest:
                # print("Found, ", start, dest, cur)
                return dist_inner
            # process neighbors and put them in the next queue
            for neighbor in dict_v[cur].dest:
                if neighbor not in list_visited:
                    list_visited.append(neighbor)
                    queue_next.append(neighbor)
        # iteration completed
        # print("Inc", queue_next)
        dist_inner += 1
        queue_current = queue_next
        queue_next = []
    print("Calc error")
    return -1


def func_backtrack(dict_valves, cur, list_valves, list_visited, released_pressure, cur_flow_rate,
                   time_steps, time_limit):
    # at current value, search for next important valve and call function recursively
    # Exit Condition 1: Next valve cannot be reached in time to be opened
    # Exit Condition 2: Next valve is opened in the last timestep before the timelimit is reached
    # Exit Condition 3: All valves have been opened and there is time left
    # Otherwise: Call recursive function
    max_released_pressure = released_pressure  # highest observed pressure after 30 time steps
    route = []                                 # route taken, will be constructed from return values
    for i in range(len(list_visited)):
        if not list_visited[i]:
            name = list_valves[i]
            # visit this valve and set it to True
            list_visited[i] = True
            # distance from current to next valve
            dist = dict_valves[cur].dists[name]  # add one additional timestep for opening valve
            if time_steps + dist >= time_limit:
                # cannot reach destination in time
                released_pressure_next = released_pressure + (time_limit - time_steps - 1) * cur_flow_rate
                if released_pressure_next > max_released_pressure:
                    max_released_pressure = released_pressure_next
                    route = [cur,  "time ran out"]
            elif time_steps + dist + 1 == time_limit:
                # open valve at time_step time_limit
                # time_limit - time_steps - 1
                # this part not validated
                released_pressure_next = released_pressure + (dist - 1) * cur_flow_rate \
                                         + (cur_flow_rate + dict_valves[name].flow_rate)
                if released_pressure_next > max_released_pressure:
                    max_released_pressure = released_pressure_next
                    # route = [name + "_" + str(max_released_pressure) + "_" + str(released_pressure) + "_" + str(dist)
                    #          + "_" + str(dict_valves[name].flow_rate) + "_exact"]
                    route = [name, "time_limit_reached"]
            else:
                # call function for next value
                all_visited = True

                for z in range(len(list_visited)):
                    if not list_visited[z]:
                        all_visited = False
                        break
                if all_visited:
                    # calculate total amount of released_pressure
                    released_pressure_next = released_pressure + dist * cur_flow_rate + \
                                             (time_limit - time_steps - dist - 1) \
                                             * (cur_flow_rate + dict_valves[name].flow_rate)
                    if released_pressure_next > max_released_pressure:
                        max_released_pressure = released_pressure_next
                        # route = [name + "_all_visited_" + str(released_pressure_next) + "_"
                        #           + str(time_steps) + "_" + str(dist)]
                        route = [name, "all visited"]
                else:
                    # can visit another valve, recursive function call
                    released_pressure_next, route_next = func_backtrack(dict_valves, name, list_valves, list_visited,
                                                                        released_pressure + dist * cur_flow_rate
                                                                        + cur_flow_rate
                                                                        + dict_valves[name].flow_rate,
                                                                        cur_flow_rate + dict_valves[name].flow_rate,
                                                                        time_steps + dist + 1, time_limit)
                    # revert list change

                    if released_pressure_next > max_released_pressure:
                        # save highest found value
                        max_released_pressure = released_pressure_next
                        route = route_next
            # revert change
            list_visited[i] = False
    # return max_released_pressure, [cur + "_" + str(time_steps) + "_" + str(cur_flow_rate) + "_" + str(
    #    released_pressure)] + route
    return max_released_pressure, [cur] + route

def read_input(filename):
    dict_valves = {}
    important_valves = []
    file = open(filename, 'r')
    for line in file:
        line = line.replace("\n", "").replace("Valve ", "").replace(" has flow rate=", " ") \
            .replace("; tunnels lead to valves ", " ").replace("; tunnel leads to valve ", " ").replace(", ", ",")

        parts = line.split(" ")
        # print(parts)
        name = parts[0]
        flow_rate = int(parts[1])
        dest_nodes = parts[2].split(",")
        valve = Valve(name, flow_rate, dest_nodes)
        dict_valves[name] = valve
        if flow_rate > 0:
            important_valves.append(name)
    file.close()
    return dict_valves, important_valves


def calculate_distances(dict_valves, important_valves, start_node):
    for i in range(len(important_valves)):
        dist_from_start = bfs(start_node, important_valves[i], dict_valves)
        dict_valves[start_node].dists[important_valves[i]] = dist_from_start
        # calculate distance between important valves
        for j in range(i + 1, len(important_valves)):
            dist = bfs(important_valves[i], important_valves[j], dict_valves)
            dict_valves[important_valves[i]].dists[important_valves[j]] = dist
            dict_valves[important_valves[j]].dists[important_valves[i]] = dist
            # print(important_valves[i], important_valves[j], dist)
