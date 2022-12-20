
__author__ = "Maximilian Geitner"
__date__ = "19.12.2022"

from day_19_not_enough_minerals.blueprint import Blueprint

if __name__ == '__main__':
    file = open('input.txt', 'r')

    blueprints = []
    # Step 1: Read file
    for line in file:
        line = line.replace("\n", "").replace("Blueprint ", "").replace(": Each ore robot costs ", ",") \
            .replace(" ore. Each clay robot costs ", ",").replace(" ore. Each obsidian robot costs ", ",") \
            .replace(" ore and ", ",").replace(" clay. Each geode robot costs ", ",").replace(" ore and ", ",") \
            .replace(" obsidian.", "")
        parts = line.split(",")
        blueprints.append(Blueprint(parts))
    file.close()

    total_one = 0
    total = 1
    print("Build Plan Info: 0 = ORE ROBOT, 1 = CLAY ROBOT, 2 = OBSIDIAN ROBOT, 3 = GEODE ROBOT\n\n")
    print("Warning: Execution may take a few minutes, especially buildprint 3 requires a lot of computational resources.\n\n")
    # Step 2: Calculate opened geodes per blueprint and compute solution
    for blueprint in blueprints:
        if blueprint.blueprint_id <= 3:
            found_geodes, robs, res, log = blueprint.comp_collected_geodes_start(32, enable_clay_first=False)
            print("ID: ", blueprint.blueprint_id, "Opened geodes", found_geodes, ", Amount Robots: ", robs,
                  ", Resources: ", res, )
            print("Build Plan: ", log)
            total *= found_geodes
            print("--> Amount of opened geodes: ", found_geodes, "Current Product: ", total)

    print("Product of all three opened geode values (Solution Part Two): ", total)
