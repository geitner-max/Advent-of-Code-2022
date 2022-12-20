
__author__ = "Maximilian Geitner"
__date__ = "19.12.2022"


class Blueprint:

    def __init__(self, str_input):
        # constants
        self.ORE = 0
        self.CLAY = 1
        self.OBSIDIAN = 2
        self.GEODE = 3
        # robots
        self.blueprint_id = int(str_input[0])
        self.ore_robot_cost = int(str_input[1])  # cost in ore
        self.clay_robot_cost = int(str_input[2])  # cost in ore
        self.obsidian_robot_o = int(str_input[3])  # cost in ore
        self.obsidian_robot_c = int(str_input[4])  # cost in clay
        self.geode_robot_ore = int(str_input[5])  # cost in ore
        self.geode_robot_obs = int(str_input[6])  # cost in obsidian

        self.max_ore = max(self.ore_robot_cost, self.clay_robot_cost, self.obsidian_robot_o, self.geode_robot_ore)
        self.max_clay = self.obsidian_robot_c
        self.max_obs = self.geode_robot_obs

    def comp_collected_geodes_start(self, timelimit, enable_clay_first=False):
        amount_robots = [0] * 4  # ore, clay, obsidian, geode
        amount_robots[self.ORE] = 1  # start with one ore collecting robot
        collected_resources = [0] * 4  # ore, clay, obsidian, geode
        max_geodes_collected, max_rob, max_res, max_log = self.comp_collected_geodes(0, timelimit, amount_robots,
                                                                                     collected_resources, self.ORE)

        if enable_clay_first:
            # block only relevant for part one
            max_geodes_collected2, max_rob2, max_res2, max_log2 = self.comp_collected_geodes(0, timelimit,
                                                                                             amount_robots,
                                                                                             collected_resources,
                                                                                             self.CLAY)
            if max_geodes_collected > max_geodes_collected2:
                return max_geodes_collected, max_rob, max_res, max_log
            else:
                return max_geodes_collected2, max_rob2, max_res2, max_log2
        else:
            # in part two: always add one ore robot as first action
            return max_geodes_collected, max_rob, max_res, max_log

    def simulate_build_robot(self, robot_id, cost_ore, cost_clay, cost_obsidian, cur_robots, cur_resources, timestep,
                             timelimit, next_buy, max_geodes, max_rob, max_res, max_log):
        # can build robot
        cur_robots[robot_id] += 1
        cur_resources[self.ORE] -= cost_ore
        cur_resources[self.CLAY] -= cost_clay
        cur_resources[self.OBSIDIAN] -= cost_obsidian
        next_geodes_collect, next_amount_rob, next_amount_res, next_log = self.comp_collected_geodes(timestep + 1,
                                                                                                     timelimit,
                                                                                                     cur_robots,
                                                                                                     cur_resources,
                                                                                                     next_buy)
        # revert changes
        cur_robots[robot_id] -= 1
        cur_resources[self.ORE] += cost_ore
        cur_resources[self.CLAY] += cost_clay
        cur_resources[self.OBSIDIAN] += cost_obsidian

        if next_geodes_collect > max_geodes:
            return next_geodes_collect, next_amount_rob, next_amount_res, str(robot_id) + ", " + next_log
        else:
            return max_geodes, max_rob, max_res, max_log

    # Return value:
    # - geodes opened
    # - amount of robots and resources at the end
    # - the robot build plan for the solution containing decision which robot has been built at each timestep
    #   Numerical value (0 to 3) represents type of robot
    def comp_collected_geodes(self, timestep, timelimit, amount_robots, collected_resources, next_buy):
        max_geodes_collected = -1
        max_rob = []
        max_res = []
        max_log = ""

        # timelimit = 24 for part one
        if timestep == timelimit:
            # if collected_resources[self.GEODE] > 0:
            #    print(collected_resources[self.GEODE], collected_resources, "Robots: ", amount_robots)
            return collected_resources[self.GEODE], amount_robots, collected_resources, ""
        else:
            # if timestep == 2:
            # print("timestep: ", timestep)
            # Step 1: Copy robots
            cur_collected_res = collected_resources.copy()
            cur_robots = amount_robots.copy()
            # Step 2: check if robot can be built
            can_built_robot = [False] * (len(amount_robots))

            # ore robot
            can_built_robot[self.ORE] = cur_collected_res[self.ORE] >= self.ore_robot_cost \
                and cur_robots[self.ORE] < self.max_ore
            # clay robot
            can_built_robot[self.CLAY] = cur_collected_res[self.ORE] >= self.clay_robot_cost \
                and cur_robots[self.CLAY] < self.max_clay
            # obsidian robot
            can_built_robot[self.OBSIDIAN] = cur_collected_res[self.ORE] >= self.obsidian_robot_o \
                and cur_collected_res[self.CLAY] >= self.obsidian_robot_c and cur_robots[self.OBSIDIAN] < self.max_obs
            # geode robot
            can_built_robot[self.GEODE] = cur_collected_res[self.ORE] >= self.geode_robot_ore \
                and cur_collected_res[self.OBSIDIAN] >= self.geode_robot_obs and timestep <= timelimit - 2

            # Step 3: increase amount of resources by amount of robots
            for idx in range(len(cur_robots)):
                cur_collected_res[idx] += cur_robots[idx]
            # Step 4: Decide next step depending on current configuration
            #
            # Ore Robot built in this timestep, Possible routes:
            # --> Consider Ore Robot, Clay Robot or obsidian robot (requires 1+ clay robots) for next construction
            # Clay Robot built in this timestep, Possible routes:
            # --> Consider Ore Robot (requires max. 2 Clay Robots), Clay Robot, Obsidian Robot
            #     or Geode Robot (requires 1+ obsidian robot)
            # Obsidian Robot built in this timestep, Possible routes:
            # --> Consider Ore Robot, Clay Robot, Obsidian Robot or Geode Robot for next construction
            # Geode Robot built in this timestep, Possible routes:
            # --> Consider Clay Robot (requires max. 1 Geode Robot), Obsidian Robot or Geode Robot for next construction
            # No Robot built in this timestep --> Continue with next timestep
            #
            #
            # Use backtracking for analyzing different build choices
            #
            # Exit Condition: timestep equals the timelimit (24 step in part one and 32 steps in part two)
            #

            if can_built_robot[self.ORE] and next_buy == self.ORE:
                # build ore robot next, if there haven't any clay robots been built yet
                if cur_robots[self.CLAY] < 1:
                    max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.ORE,
                                                                                                self.ore_robot_cost, 0,
                                                                                                0,
                                                                                                cur_robots,
                                                                                                cur_collected_res,
                                                                                                timestep,
                                                                                                timelimit, self.ORE,
                                                                                                max_geodes_collected,
                                                                                                max_rob,
                                                                                                max_res, max_log)
                # build clay next
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.ORE,
                                                                                            self.ore_robot_cost, 0, 0,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit,
                                                                                            self.CLAY,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                # try building obsidian robot if there is at least one existing clay robot
                if cur_robots[self.CLAY] >= 1:
                    max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.ORE,
                                                                                                self.ore_robot_cost, 0,
                                                                                                0,
                                                                                                cur_robots,
                                                                                                cur_collected_res,
                                                                                                timestep,
                                                                                                timelimit,
                                                                                                self.OBSIDIAN,
                                                                                                max_geodes_collected,
                                                                                                max_rob,
                                                                                                max_res, max_log)
            elif can_built_robot[self.CLAY] and next_buy == self.CLAY:
                # build clay next
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.CLAY,
                                                                                            self.clay_robot_cost, 0, 0,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.CLAY,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                # build ore next
                if cur_robots[self.CLAY] <= 2:
                    max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.CLAY,
                                                                                                self.clay_robot_cost, 0,
                                                                                                0,
                                                                                                cur_robots,
                                                                                                cur_collected_res,
                                                                                                timestep,
                                                                                                timelimit, self.ORE,
                                                                                                max_geodes_collected,
                                                                                                max_rob,
                                                                                                max_res, max_log)
                # build obsidian next
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.CLAY,
                                                                                            self.clay_robot_cost, 0, 0,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.OBSIDIAN,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                if cur_robots[self.OBSIDIAN] >= 1:
                    max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.CLAY,
                                                                                                self.clay_robot_cost, 0,
                                                                                                0,
                                                                                                cur_robots,
                                                                                                cur_collected_res,
                                                                                                timestep,
                                                                                                timelimit,
                                                                                                self.GEODE,
                                                                                                max_geodes_collected,
                                                                                                max_rob,
                                                                                                max_res, max_log)
            elif can_built_robot[self.OBSIDIAN] and next_buy == self.OBSIDIAN:
                # build obsidian
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.OBSIDIAN,
                                                                                            self.obsidian_robot_o,
                                                                                            self.obsidian_robot_c, 0,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.OBSIDIAN,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                # build clay
                if cur_robots[self.OBSIDIAN] <= 3:
                    max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.OBSIDIAN,
                                                                                                self.obsidian_robot_o,
                                                                                                self.obsidian_robot_c,
                                                                                                0,
                                                                                                cur_robots,
                                                                                                cur_collected_res,
                                                                                                timestep,
                                                                                                timelimit, self.CLAY,
                                                                                                max_geodes_collected,
                                                                                                max_rob,
                                                                                                max_res, max_log)
                # build geode
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.OBSIDIAN,
                                                                                            self.obsidian_robot_o,
                                                                                            self.obsidian_robot_c, 0,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.GEODE,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                # build ore robot
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.OBSIDIAN,
                                                                                            self.obsidian_robot_o,
                                                                                            self.obsidian_robot_c, 0,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.ORE,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
            elif can_built_robot[self.GEODE] and next_buy == self.GEODE:
                # geode
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.GEODE,
                                                                                            self.geode_robot_ore,
                                                                                            0, self.geode_robot_obs,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.GEODE,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                # obsidian
                max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.GEODE,
                                                                                            self.geode_robot_ore,
                                                                                            0, self.geode_robot_obs,
                                                                                            cur_robots,
                                                                                            cur_collected_res, timestep,
                                                                                            timelimit, self.OBSIDIAN,
                                                                                            max_geodes_collected,
                                                                                            max_rob,
                                                                                            max_res, max_log)
                # clay, only allow building clay robots when one geode robot exists
                if cur_robots[self.GEODE] <= 1:
                    max_geodes_collected, max_rob, max_res, max_log = self.simulate_build_robot(self.GEODE,
                                                                                                self.geode_robot_ore,
                                                                                                0, self.geode_robot_obs,
                                                                                                cur_robots,
                                                                                                cur_collected_res,
                                                                                                timestep,
                                                                                                timelimit, self.CLAY,
                                                                                                max_geodes_collected,
                                                                                                max_rob,
                                                                                                max_res, max_log)
            else:
                # no robot can be built, continue with next timestep
                max_geodes_collected, max_rob, max_res, max_log = self.comp_collected_geodes(timestep + 1,
                                                                                             timelimit,
                                                                                             cur_robots,
                                                                                             cur_collected_res,
                                                                                             next_buy)
                max_log = "None, " + max_log

            # end of loop, return highest found value
            return max_geodes_collected, max_rob, max_res, max_log
