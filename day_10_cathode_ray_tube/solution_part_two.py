
__author__ = "Maximilian Geitner"
__date__ = "10.12.2022"


def draw_pixel(crt, cycle_inner, val):
    # compute current x-coordinate to render
    to_draw_pixel = (cycle_inner - 1) % 40
    # decide whether val lies within one pixel distance to x-coordinate and render '#'
    to_draw = val == to_draw_pixel or (val - 1) == to_draw_pixel or (val + 1) == to_draw_pixel
    # print(to_draw_pixel, val, to_draw)
    if to_draw:
        crt += "#"
    else:
        crt += "."
    # add line break every 40 cycles
    if cycle_inner % 40 == 0:
        crt += "\n"
    return crt

# Example Output Row: ##..##..##..##..##..##..##..##..##..##..


if __name__ == '__main__':
    file = open('input.txt', 'r')

    x = 1  # starting value
    cycle = 0
    screen = ""  # screen output

    # Part Two: Don't compute signal strengths anymore,
    # but display output depending on the current value during each cycle
    for line in file:
        value = 0
        line = line.replace("\n", "")
        if line == "noop":
            cycle += 1
            # draw one pixel for noop operation
            screen = draw_pixel(screen, cycle, x)
        else:
            parts = line.split(" ")
            value = int(parts[1])
            # draw two pixels for each add-operation
            screen = draw_pixel(screen, cycle + 1, x)
            screen = draw_pixel(screen, cycle + 2, x)
            cycle += 2

        x += value

    print("Screen Output (Solution Part Two): \n", screen)
    print("--> Read letters in the screen output in order to find the solution")
