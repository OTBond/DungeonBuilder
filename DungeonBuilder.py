#Goal: Create maps with connecting rooms and visualize them
import pygame, random
pygame.init()

#Window
Title = "Dungeon Builder"
WIDTH = 650
HEIGHT = 650

FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(Title)
clock = pygame.time.Clock()

#Colors
DARK_BLUE = (16,86,103)
WHITE = (255,255,255)
GREEN = (80,255,80)
BLACK = (0,0,0)

#SETTINGS
grid = 64
running = True
def getMap(maxRooms):
    map_grid = []
    map_size = 10
    seed = [random.randint(0,9), random.randint(0,9)]
    current = seed
    numRooms = 0
    
    #First: populate grid
    for r in range(map_size):
        map_grid.append([])
        for c in range(map_size):
            map_grid[r].append("*")
            
    #Second: place seed
    map_grid[seed[0]][seed[1]] = "R"

    #Third: loop through with new offsets until 10 unique connected rooms
    #picking a random direction and populating the next available room in that
    #direction, or picking a new direction if there isnt one
    while numRooms < maxRooms-1:
        x, y = 0, 0
        undecided = True
        finding = True
        while undecided:
            xPos, yPos = current[0], current[1]
            direction = random.randint(0,3)
            if direction == 0:
                #Up
                y = -1
            elif direction == 1:
                #Down
                y = 1
            elif direction == 2:
                #Right
                x = 1
            elif direction == 3:
                #Left
                x =  -1
                
            while finding:
                xPos += x
                yPos += y

                if 9 < yPos or 0 > yPos or 9 < xPos or 0 > xPos:
                    finding = False
                    break

                if map_grid[xPos][yPos] == "*":
                    map_grid[xPos][yPos] = "R"
                    current = [xPos,yPos]
                    numRooms += 1
                    undecided = False
                    finding = False

            if 9 < yPos or 0 > yPos or 9 < xPos or 0 > xPos:
                    undecided = False
            
    return map_grid

maxRooms = 10
displayMap = getMap(maxRooms)

while running:
    #Process Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and maxRooms < 25:
                maxRooms += 1
            if event.key == pygame.K_z and maxRooms > 0:
                maxRooms -= 1
            displayMap = getMap(maxRooms)

    #Draw game stuff
    screen.fill(DARK_BLUE)
    for r in range(len(displayMap)):
        for c in range(len(displayMap[0])):
            if displayMap[r][c] == "R":
                drawRect = pygame.Rect(c*grid, r*grid, grid, grid)
                pygame.draw.rect(screen, WHITE, drawRect)

                pygame.draw.line(screen, BLACK, (c*grid, r*grid), (c*grid, r*grid+grid), 3)
                pygame.draw.line(screen, BLACK, (c*grid, r*grid), (c*grid+grid, r*grid), 3)
                pygame.draw.line(screen, BLACK, (c*grid+grid, r*grid+grid), (c*grid+grid, r*grid), 3)
                pygame.draw.line(screen, BLACK, (c*grid, r*grid+grid), (c*grid+grid, r*grid+grid), 3)
    

    pygame.display.flip()    

    clock.tick(FPS)

pygame.quit()
