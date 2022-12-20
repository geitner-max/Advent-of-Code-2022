
__author__ = "Maximilian Geitner"
__date__ = "19.12.2022"

from day_19_not_enough_minerals.blueprint import Blueprint

if __name__ == '__main__':
    file = open('input.txt', 'r')

    blueprints = []
    # Step 1: Read file and create blueprint objects
    for line in file:
        line = line.replace("\n", "").replace("Blueprint ", "").replace(": Each ore robot costs ", ",") \
            .replace(" ore. Each clay robot costs ", ",").replace(" ore. Each obsidian robot costs ", ",") \
            .replace(" ore and ", ",").replace(" clay. Each geode robot costs ", ",").replace(" ore and ", ",") \
            .replace(" obsidian.", "")
        parts = line.split(",")
        blueprints.append(Blueprint(parts))
    file.close()

    total = 0
    print("Build Plan Info: 0 = ORE ROBOT, 1 = CLAY ROBOT, 2 = OBSIDIAN ROBOT, 3 = GEODE ROBOT\n\n")
    # Step 2: Process blueprints and opened geode information
    for blueprint in blueprints:
        found_geodes, robs, res, log = blueprint.comp_collected_geodes_start(24, enable_clay_first=True)
        print("ID: ", blueprint.blueprint_id, "Opened geodes", found_geodes, ", Amount Robots: ", robs,
              ", Resources: ", res, )
        print("Build Plan: ", log)
        total_blue = blueprint.blueprint_id * found_geodes
        total += total_blue
        print("--> Quality level added: ", total_blue, ", Current Total: ", total)

    print("Quality Level Sum of all of the Blueprints (Solution Part One): ", total)
