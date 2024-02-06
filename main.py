import pygame
import sys
import random

# simple falling sand simulation using pygame based on noita's sand physics
# https://noitagame.com/

# constants
WIDTH = 800
HEIGHT = 600
FPS = 60
PARTICLE_SIZE = 7
SAND = "1"
WATER = "2"
GAS = "3"
LAVA = "4"
ROCK = "5"
ICE = "6"
WOOD = "7"
FIRE = "8"
MUD = "9"
GRASS = "A"
IRON = "B"
EMPTY = "0"

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)
WATER_COLOR = (0, 0, 255)
GAS_COLOR = (128, 128, 200)
LAVA_COLOR = (255, 0, 0)
ROCK_COLOR = (128, 128, 128)
ICE_COLOR = (0, 255, 255)
WOOD_COLOR = (139, 69, 19)
FIRE_COLOR = (255, 69, 0)
MUD_COLOR = (139, 69, 79)
GRASS_COLOR = (50, 190, 50)
IRON_COLOR = (140, 100, 100)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Falling Sand")
clock = pygame.time.Clock()

# create grid
grid = [[EMPTY for _ in range(WIDTH // PARTICLE_SIZE)] for _ in range(HEIGHT // PARTICLE_SIZE)]
next_grid = [[EMPTY for _ in range(WIDTH // PARTICLE_SIZE)] for _ in range(HEIGHT // PARTICLE_SIZE)]
direction_history_grid = [[0 for _ in range(WIDTH // PARTICLE_SIZE)] for _ in range(HEIGHT // PARTICLE_SIZE)]

# define a placing cooldown variable for sand
placing_cooldown = 10

# define a change element cooldown variable
change_element_cooldown = 0

# define a save cooldown variable
save_cooldown = 0

# define a load cooldown variable
load_cooldown = 0

# track current element
current_element = 1
possible_elements = [SAND, WATER, GAS, LAVA, ROCK, ICE, WOOD, MUD, GRASS, IRON, EMPTY]
# name element for display
element_names = ["SAND", "WATER", "GAS", "LAVA", "ROCK", "ICE", "WOOD", "MUD", "GRASS", "IRON", "EMPTY"]

# weight the chance to spawn a certain element
element_weights = [
    0.002, # sand
    0.002, # water
    0.0, # gas
    0.0001, # lava
    0.0001, # rock
    0.001, # ice
    0.001, # wood
    0.001, # mud
    0.002, # grass
    0.0001,  # iron,
    0.999   # empty
]

# main loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # deplete sand placing cooldown by one
    placing_cooldown -= 1


    if pygame.mouse.get_pressed()[0]:
        # create a sand shape using a string array
        # consider this data structure

        sand_shape = []
        shape_width = random.randint(3, 11)
        shape_height = random.randint(3, 15)

        for y in range(shape_height):
            sand_shape.append(["*"] * shape_width)
            for x in range(shape_width):
                if random.random() > 0.5:
                    sand_shape[y][x] = " "      

        # # from previous shape, create a new one with a random rotation
        # for _ in range(random.randint(0, 3)):
        #     sand_shape = list(zip(*sand_shape[::-1]))

        # reset placing cooldown
        placing_cooldown = 10

        # draw the sand shape looping through the string array around the mouse position
        for y in range(len(sand_shape)):
            for x in range(len(sand_shape[y])):
                if pygame.mouse.get_pos()[1] // PARTICLE_SIZE - len(sand_shape) // 2 + y < 0 or pygame.mouse.get_pos()[1] // PARTICLE_SIZE - len(sand_shape) // 2 + y >= len(grid):
                    continue
                # check boundaries for x
                if pygame.mouse.get_pos()[0] // PARTICLE_SIZE - len(sand_shape[y]) // 2 + x < 0 or pygame.mouse.get_pos()[0] // PARTICLE_SIZE - len(sand_shape[y]) // 2 + x >= len(grid[0]):
                    continue                
                elif sand_shape[y][x] == "*":
                    grid[pygame.mouse.get_pos()[1] // PARTICLE_SIZE - len(sand_shape) // 2 + y][pygame.mouse.get_pos()[0] // PARTICLE_SIZE - len(sand_shape[y]) // 2 + x] = possible_elements[current_element]


    if pygame.mouse.get_pressed()[2]:
        # place water around the mouse position using a string array
        water_shape = [
            " *** ",
            "*****",
            "*****",
            "*****",
            " *** "
        ]

        for y in range(len(water_shape)):
            for x in range(len(water_shape[y])):
                # check boundaries for y
                if pygame.mouse.get_pos()[1] // PARTICLE_SIZE - len(water_shape) // 2 + y < 0 or pygame.mouse.get_pos()[1] // PARTICLE_SIZE - len(water_shape) // 2 + y >= len(grid):
                    continue
                # check boundaries for x
                if pygame.mouse.get_pos()[0] // PARTICLE_SIZE - len(water_shape[y]) // 2 + x < 0 or pygame.mouse.get_pos()[0] // PARTICLE_SIZE - len(water_shape[y]) // 2 + x >= len(grid[0]):
                    continue
                elif water_shape[y][x] == "*":
                    grid[pygame.mouse.get_pos()[1] // PARTICLE_SIZE - len(water_shape) // 2 + y][pygame.mouse.get_pos()[0] // PARTICLE_SIZE - len(water_shape[y]) // 2 + x] = possible_elements[current_element]
        
    # place gas with middle mouse button
    if pygame.mouse.get_pressed()[1]:
        x, y = pygame.mouse.get_pos()
        x //= PARTICLE_SIZE
        y //= PARTICLE_SIZE
        grid[y][x] = GAS

    # listen for Z key to slow down the simulation
    if pygame.key.get_pressed()[pygame.K_z]:
        FPS = 20
    else:
        FPS = 60

    # listen for X key to speed up the simulation
    if pygame.key.get_pressed()[pygame.K_x]:
        FPS = 120

    # listen for C key to clear the all grids
    if pygame.key.get_pressed()[pygame.K_c]:
        grid = [[EMPTY for _ in range(WIDTH // PARTICLE_SIZE)] for _ in range(HEIGHT // PARTICLE_SIZE)]
        next_grid = [[EMPTY for _ in range(WIDTH // PARTICLE_SIZE)] for _ in range(HEIGHT // PARTICLE_SIZE)]
        direction_history_grid = [[0 for _ in range(WIDTH // PARTICLE_SIZE)] for _ in range(HEIGHT // PARTICLE_SIZE)]
    
    # listen for R key to randomize the grid and reset next grid
    if pygame.key.get_pressed()[pygame.K_r]:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                element = random.choices(possible_elements, weights=element_weights)[0]
                grid[y][x] = element
                next_grid[y][x] = element
                direction_history_grid[y][x] = 0
                # fill neighboring cells with same element
                if y - 1 >= 0 and grid[y - 1][x] == EMPTY:
                    grid[y - 1][x] = element
                    next_grid[y - 1][x] = element
                if y + 1 < len(grid) and grid[y + 1][x] == EMPTY:
                    grid[y + 1][x] = element
                    next_grid[y + 1][x] = element
                if x - 1 >= 0 and grid[y][x - 1] == EMPTY:
                    grid[y][x - 1] = element
                    next_grid[y][x - 1] = element
                if x + 1 < len(grid[y]) and grid[y][x + 1] == EMPTY:
                    grid[y][x + 1] = element
                    next_grid[y][x + 1] = element
                


    # listen for E key to change the current element only once
    change_element_cooldown -= 1
    
    if pygame.key.get_pressed()[pygame.K_e] and change_element_cooldown <= 0:
        change_element_cooldown = 10
        current_element += 1
        if current_element >= len(possible_elements):
            current_element = 0 

    # liste for Q key to go back to the previous element
    if pygame.key.get_pressed()[pygame.K_q] and change_element_cooldown <= 0:
        change_element_cooldown = 10
        current_element -= 1
        if current_element < 0:
            current_element = len(possible_elements) - 1
    
    # listen for S key to save the current grid to a file
    save_cooldown -= 1
    if pygame.key.get_pressed()[pygame.K_s] and save_cooldown <= 0:
        save_cooldown = 10
        with open("grid.txt", "w") as file:
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    file.write(str(grid[y][x]))
                file.write("\n")

            file.close()
            print("Saved grid to file")

    # listen for L key to load the grid from a file
    load_cooldown -= 1
    if pygame.key.get_pressed()[pygame.K_l] and load_cooldown <= 0:
        load_cooldown = 10
        with open("grid.txt", "r") as file:
            lines = file.readlines()
            for y in range(len(lines)):
                for x in range(len(lines[y]) - 1):
                    grid[y][x] = lines[y][x]
                    next_grid[y][x] = lines[y][x]
            file.close()
            print("Loaded grid from file")
    
    # listen for P key to pause the simulation
    if pygame.key.get_pressed()[pygame.K_p]:
        FPS = 0

    # listen for O key to resume the simulation
    if pygame.key.get_pressed()[pygame.K_o]:
        FPS = 60
    
    # listen for T to replace only the top row with sand
    if pygame.key.get_pressed()[pygame.K_t]:
        for x in range(len(grid[0])):
            grid[0][x] = possible_elements[current_element]
            next_grid[0][x] = possible_elements[current_element]
    
    # listen for Y to replace only the bottom row with current element
    if pygame.key.get_pressed()[pygame.K_y]:
        for x in range(len(grid[-1])):
            grid[-1][x] = possible_elements[current_element]
            next_grid[-1][x] = possible_elements[current_element]
    
    # listen for U to replace only the left column with current element
    if pygame.key.get_pressed()[pygame.K_u]:
        for y in range(len(grid)):
            grid[y][0] = possible_elements[current_element]
            next_grid[y][0] = possible_elements[current_element]
    
    # listen for I to replace only the right column with current element
    if pygame.key.get_pressed()[pygame.K_i]:
        for y in range(len(grid)):
            grid[y][-1] = possible_elements[current_element]
            next_grid[y][-1] = possible_elements[current_element]   

    # listen for G to replace only the middle column with current element
    if pygame.key.get_pressed()[pygame.K_g]:
        for y in range(len(grid)):
            grid[y][len(grid[y]) // 2] = possible_elements[current_element]
            next_grid[y][len(grid[y]) // 2] = possible_elements[current_element]

    # listen for H to replace only the middle row with current element
    if pygame.key.get_pressed()[pygame.K_h]:
        for x in range(len(grid[0])):
            grid[len(grid) // 2][x] = possible_elements[current_element]
            next_grid[len(grid) // 2][x] = possible_elements[current_element]
    
    # listen for J to replace diagonal from top left to bottom right with current element
    if pygame.key.get_pressed()[pygame.K_j]:
        for i in range(len(grid)):
            grid[i][i] = possible_elements[current_element]
            next_grid[i][i] = possible_elements[current_element]
    
    # listen for K to replace diagonal from top right to bottom left with current element
    if pygame.key.get_pressed()[pygame.K_k]:
        for i in range(len(grid)):
            grid[i][len(grid[i]) - i - 1] = possible_elements[current_element]
            next_grid[i][len(grid[i]) - i - 1] = possible_elements[current_element]
    
    # listen for F to fill the entire grid with current element
    if pygame.key.get_pressed()[pygame.K_f]:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                grid[y][x] = possible_elements[current_element]
                next_grid[y][x] = possible_elements[current_element]
    
    # listen for D to draw circles of current element around the mouse position
    if pygame.key.get_pressed()[pygame.K_d]:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if (x - pygame.mouse.get_pos()[0] // PARTICLE_SIZE) ** 2 + (y - pygame.mouse.get_pos()[1] // PARTICLE_SIZE) ** 2 < 100:
                    grid[y][x] = possible_elements[current_element]
                    next_grid[y][x] = possible_elements[current_element]

    # listen for A to quit the simulation
    if pygame.key.get_pressed()[pygame.K_a]:
        running = False


    # listen for W to shift the grid right by one
    if pygame.key.get_pressed()[pygame.K_w]:
        for y in range(len(grid)):
            for x in range(len(grid[y]) - 1, 0, -1):
                grid[y][x] = grid[y][x - 1]
                next_grid[y][x] = grid[y][x - 1]

    # listen for N to print the number of current element in the grid
    count = 0
    if pygame.key.get_pressed()[pygame.K_n]:
        count = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == possible_elements[current_element]:
                    count += 1

    
    # push all elements at mouse Y position to the left when pressing M
    if pygame.key.get_pressed()[pygame.K_m]:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if y == pygame.mouse.get_pos()[1] // PARTICLE_SIZE:
                    grid[y][x] = grid[y][x - 1]
                    next_grid[y][x] = grid[y][x - 1]
        
    # particle simulation logic, sand falls down and fall to the left or right if there is no space below
    for y in range(len(grid) - 1, -1, -1):
        for x in range(len(grid[y])):
            # sand logic, it should fall through empty space or water
            if grid[y][x] == SAND:
                # define a random direction to fall to the left or right
                random_direction = random.choice([-1, 1])


                if y + 1 < len(grid) and grid[y + 1][x] == EMPTY:
                    next_grid[y + 1][x] = SAND
                    next_grid[y][x] = EMPTY
                # elif y + 1 < len(grid) and x - 1 >= 0 and grid[y + 1][x - random_direction] == EMPTY:
                #     next_grid[y + 1][x - random_direction] = SAND
                #     next_grid[y][x] = EMPTY
                elif y + 1 < len(grid) and x + 1 < len(grid[y]) and grid[y + 1][x + random_direction] == EMPTY:
                    next_grid[y + 1][x + random_direction] = SAND
                    next_grid[y][x] = EMPTY

                
                # include water
                elif y + 1 < len(grid) and grid[y + 1][x] == WATER:
                    next_grid[y + 1][x] = SAND
                    next_grid[y][x] = WATER
                elif y + 1 < len(grid) and x - 1 >= 0 and grid[y + 1][x - 1] == WATER:
                    next_grid[y + 1][x - 1] = SAND
                    next_grid[y][x] = WATER
                elif y + 1 < len(grid) and x + 1 < len(grid[y]) and grid[y + 1][x + 1] == WATER:
                    next_grid[y + 1][x + 1] = SAND
                    next_grid[y][x] = WATER
                # include gas
                elif y + 1 < len(grid) and grid[y + 1][x] == GAS:
                    next_grid[y + 1][x] = SAND
                    next_grid[y][x] = GAS
                elif y + 1 < len(grid) and x - 1 >= 0 and grid[y + 1][x - 1] == GAS:
                    next_grid[y + 1][x - 1] = SAND
                    next_grid[y][x] = GAS
                elif y + 1 < len(grid) and x + 1 < len(grid[y]) and grid[y + 1][x + 1] == GAS:
                    next_grid[y + 1][x + 1] = SAND
                    next_grid[y][x] = GAS
            elif grid[y][x] == WATER:
                random_direction = random.choice([-1, -1, 1, 1, 1, -1, 1])
                random_direction *= random.choice([1, 2, 3, 4, 5, 6, 7, 8])

                # if there is space below, move down
                if y + 1 < len(grid) and grid[y + 1][x] == EMPTY:
                    next_grid[y + 1][x] = WATER
                    next_grid[y][x] = EMPTY
                elif y + 1 < len(grid) and grid[y + 1][x] == LAVA:
                    next_grid[y + 1][x] = LAVA
                    next_grid[y][x] = GAS
                # if there isn't space below, try to move to the left or right but not down yet, it will fall down next frame
                elif y + 1 < len(grid) and x + random_direction < len(grid[y]) and x + random_direction >= 0 and grid[y][x + random_direction] == EMPTY:
                    next_grid[y][x + random_direction] = WATER
                    next_grid[y][x] = EMPTY

            elif grid[y][x] == LAVA and random.random() > 0.9:
                # lava flows like water but replace water
                random_direction = random.choice([-1, -1, 1, 1, 1, -1, 1])

                # if there is space below, move down
                if y + 1 < len(grid) and grid[y + 1][x] == EMPTY:
                    next_grid[y + 1][x] = LAVA
                    next_grid[y][x] = EMPTY
                # if there isn't space below, try to move to the left or right but not down yet, it will fall down next frame
                elif y + 1 < len(grid) and x + random_direction < len(grid[y]) and x + random_direction >= 0 and grid[y][x + random_direction] == EMPTY:
                    next_grid[y][x + random_direction] = LAVA
                    next_grid[y][x] = EMPTY
                # if there is water below, replace it with lava
                elif y + 1 < len(grid) and grid[y + 1][x] == WATER:
                    next_grid[y + 1][x] = LAVA
                    if random.random() > 0.9:
                        next_grid[y][x] = ROCK
                    # replace all neighboring empty space with gas
                    if y - 1 >= 0 and grid[y - 1][x] == EMPTY:
                        next_grid[y - 1][x] = GAS
                    if x - 1 >= 0 and grid[y][x - 1] == EMPTY:
                        next_grid[y][x - 1] = GAS
                    if x + 1 < len(grid[y]) and grid[y][x + 1] == EMPTY:
                        next_grid[y][x + 1] = GAS
                    
                # if there is sand below replace it with gas
                elif y + 1 < len(grid) and grid[y + 1][x] == SAND:
                    next_grid[y + 1][x] = GAS
                    next_grid[y][x] = EMPTY
                elif y + 1 < len(grid) and grid[y + 1][x] == GAS:
                    next_grid[y + 1][x] = LAVA
                    next_grid[y][x] = GAS                    

            elif grid[y][x] == ROCK:
                # rock doesn't move
                next_grid[y][x] = ROCK
            elif grid[y][x] == ICE:
                # ice melts into water when one of its neighbors is lava
                if y + 1 < len(grid) and grid[y + 1][x] == LAVA:
                    next_grid[y][x] = WATER
                elif y - 1 >= 0 and grid[y - 1][x] == LAVA:
                    next_grid[y][x] = WATER
                elif x - 1 >= 0 and grid[y][x - 1] == LAVA:
                    next_grid[y][x] = WATER
                elif x + 1 < len(grid[y]) and grid[y][x + 1] == LAVA:
                    next_grid[y][x] = WATER
            elif grid[y][x] == WOOD and random.random() > 0.99:
                # wood burns into lava when one of its neighbors is lava
                if y + 1 < len(grid) and grid[y + 1][x] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                elif y - 1 >= 0 and grid[y - 1][x] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                elif x - 1 >= 0 and grid[y][x - 1] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                elif x + 1 < len(grid[y]) and grid[y][x + 1] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
            elif grid[y][x] == GRASS and random.random() > 0.3:
                # wood burns into lava when one of its neighbors is lava
                if y + 1 < len(grid) and grid[y + 1][x] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                elif y - 1 >= 0 and grid[y - 1][x] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                elif x - 1 >= 0 and grid[y][x - 1] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                elif x + 1 < len(grid[y]) and grid[y][x + 1] == LAVA:
                    next_grid[y][x] = LAVA
                    next_grid[y - 1][x] = GAS
                
                    

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # gas logic (it goes up)
            if grid[y][x] == GAS and random.random() > 0.5:
                random_direction = random.choice([-1, -1, 1, 1, 1, -1, 1])

                # if there is space above, move up
                if y - 1 >= 0 and grid[y - 1][x] == EMPTY:
                    next_grid[y - 1][x] = GAS
                    next_grid[y][x] = EMPTY
                elif y - 1 >= 0 and grid[y - 1][x] == WATER:
                    next_grid[y - 1][x] = GAS
                    next_grid[y][x] = WATER                    
                elif y - 1 >= 0 and grid[y - 1][x] == LAVA:
                    next_grid[y - 1][x] = GAS
                    next_grid[y][x] = LAVA     
                # if there isn't space above, try to move to the left or right but not up yet, it will go up next frame
                elif y - 1 >= 0 and x + random_direction < len(grid[y]) and x + random_direction >= 0 and grid[y][x + random_direction] == EMPTY:
                    next_grid[y][x + random_direction] = GAS
                    next_grid[y][x] = EMPTY

                # if it reaches the top, it disappears
                if y - 1 < 0:
                    next_grid[y][x] = EMPTY
                
                # elif y - 1 >= 0 and x - 1 >= 0 and grid[y - 1][x - 1] == EMPTY:
                #     next_grid[y - 1][x - 1] = GAS
                #     next_grid[y][x] = EMPTY
                # elif y - 1 >= 0 and x + 1 < len(grid[y]) and grid[y - 1][x + 1] == EMPTY:
                #     next_grid[y - 1][x + 1] = GAS
                #     next_grid[y][x] = EMPTY

    # 



    # draw
    screen.fill(BLACK)

    for y in range(len(next_grid)):
        for x in range(len(next_grid[y])):
            if next_grid[y][x] == SAND:
                pygame.draw.rect(screen, SAND_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == WATER:
                pygame.draw.rect(screen, WATER_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == GAS:
                pygame.draw.rect(screen, GAS_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == LAVA:
                pygame.draw.rect(screen, LAVA_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == ROCK:
                pygame.draw.rect(screen, ROCK_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == ICE:
                pygame.draw.rect(screen, ICE_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == WOOD:
                pygame.draw.rect(screen, WOOD_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == FIRE:
                pygame.draw.rect(screen, FIRE_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == MUD:
                pygame.draw.rect(screen, MUD_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == GRASS:
                pygame.draw.rect(screen, GRASS_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))
            elif next_grid[y][x] == IRON:
                pygame.draw.rect(screen, IRON_COLOR, (x * PARTICLE_SIZE, y * PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE))

    # apply a shader to the screen
    newshader = pygame.Surface((WIDTH, HEIGHT))
    newshader.set_alpha(0)
    newshader.fill((0, 0, 0))
    screen.blit(newshader, (0, 0))

    # draw the FPS on the screen
    font = pygame.font.Font(None, 36)
    text = font.render("FPS: " + str(FPS), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # draw the current element on the screen
    text = font.render("Element (E): " + str(element_names[current_element]), True, (255, 255, 255))
    screen.blit(text, (10, 40))

    # # draw the number of current element on the screen
    # text = font.render("Number of " + str(element_names[current_element]) + ": " + str(count), True, (255, 255, 255))
    # screen.blit(text, (10, 70))

    # swap grids
    grid = next_grid

    # after drawing everything, flip the display
    pygame.display.flip()
    clock.tick(FPS)



pygame.quit()


