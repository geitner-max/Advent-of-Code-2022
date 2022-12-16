

__author__ = "Maximilian Geitner"
__date__ = "16.12.2022"


class Valve:

    def __init__(self, name, flow_rate, dest_valves):
        self.name = name
        self.flow_rate = flow_rate
        self.dest = dest_valves  # neighbouring valves
        # contains closed valves and amount of hops
        self.visited = False
        self.dists = {}
