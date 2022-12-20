
__author__ = "Maximilian Geitner"
__date__ = "18.12.2022"


# Solution idea: for each lava cube, count amount of neighbor cubes (6 cubes to check) that are also lava cubes
# Sum of all counted lava cube neighbours is relevant for calculating the exterior surface area
def count_lava_cube_neighbors(cur, list_cubes):
    neighbors = 0
    for entry in list_cubes:
        counter = 0
        for i in range(len(cur)):
            if cur[i] == entry[i]:
                counter += 1
        if counter == 2:
            # two dimensions are the same
            # check whether last dim is off by one
            for i in range(len(cur)):
                if cur[i] + 1 == entry[i] or cur[i] - 1 == entry[i]:
                    neighbors += 1
                    break
    return neighbors


if __name__ == '__main__':
    FILENAME = 'input.txt'
    file = open(FILENAME, 'r')

    cubes = []
    # Step 1: Read file
    for line in file:
        line = line.replace("\n", "")
        parts = line.split(",")

        cube = []
        for idx in parts:
            cube.append(int(idx))
        cubes.append(cube)
        # print(len(cube))

    # Step 2: Count not connected sides
    # For each cube: Look at side and check that there is no neighbor
    result = 0
    for cube in cubes:
        # surface area for one lave cube = 6 - (amount of lava blocks)
        count = 6 - count_lava_cube_neighbors(cube, cubes)
        result += count
    print("Exterior Surface Area (Solution Part One): ", result)
