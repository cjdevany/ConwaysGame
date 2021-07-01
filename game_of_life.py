import pygame

""" 
To-Do:
    Get the game working with dragging the mouse as well as clicks.
    Introduce a welcome screen with controls and instructions.
"""

##### Globals #####
DISPLAY_RESOLUTION = [800, 600]
CELL_SIZES = [10, 15, 20, 25, 30]
SIZE = 2
SPEED = 3
STROKE = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)


##### Functions #####
# Takes a mouse position (x, y) and translates to a 2-d index (row, column).
def positionToIndex(position):
    return (position[1] // CELL_SIZES[SIZE], position[0] // CELL_SIZES[SIZE])


# Takes a boolean grid and draws it to a screen.
def drawGrid(grid, screen):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            color = WHITE if grid[row][col] is True else BLACK
            pygame.draw.rect(screen, color, (CELL_SIZES[SIZE] * col, CELL_SIZES[SIZE] * row, CELL_SIZES[SIZE] - STROKE, CELL_SIZES[SIZE] - STROKE))


# Iterate in a square around the point and count how many neighbors are alive
def countLiveNeighbors(grid, row, col):
    count = 0
    for y in range(row - 1, row + 2):
        for x in range(col - 1, col + 2):
            # If it can cause an index error it's a dead spot
            if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[y]):
                continue
            elif grid[y][x] is True:
                count += 1
    # If our param position is true then it was included in the count and needs to be removed
    if grid[row][col] is True:
        count -= 1
    return count


# Copies from one grid to another - if grids aren't the same size the excess is dropped.
# Used when re-sizing the window to keep the information that was already present.
def gridCopy(copyFrom, copyTo):
    for i in range(len(copyFrom)):
        for j in range(len(copyFrom[i])):
            if i >= len(copyTo) or j >= len(copyTo[i]):
                continue
            else:
                copyTo[i][j] = copyFrom[i][j]


# Takes a 2-d grid and returns the next generation following Conways Rules.
def mutate(grid):
    """
    Rules:
    1) Any live cell with 2 or 3 live neighbors survives
    2) Any dead cell with 3 live neighbors becomes alive
    3) All other live cells die in the next generation. Similarly, all dead cells stay dead.
    """
    newGrid = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            neighbors = countLiveNeighbors(grid, row, col)            
            if neighbors == 2:
                if grid[row][col] is True:
                    newGrid[row][col] = True
            elif neighbors == 3:
                newGrid[row][col] = True                

    return newGrid


# Takes the old pause status, reverses it, updates the title bar, and returns the new pause status.
def pause(paused):
    if paused:
        pygame.display.set_caption("Conway's Game of Life : Running")
        return False
    else:
        pygame.display.set_caption("Conway's Game of Life : Paused")
        return True


def main():
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life : Paused")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(DISPLAY_RESOLUTION)
    running = True
    paused = True
    global SIZE
    global SPEED

    # Init the gameboard
    numRows, numCols = DISPLAY_RESOLUTION[1] // CELL_SIZES[SIZE], DISPLAY_RESOLUTION[0] // CELL_SIZES[SIZE]
    grid = [[False for _ in range(numCols)] for _ in range(numRows)]

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Pause or unpause on spacebar
                if event.key == pygame.K_SPACE:
                    paused = pause(paused)

                # r resets the game if it's paused
                if paused and event.key == pygame.K_r:
                    grid = [[False for _ in range(numCols)] for _ in range(numRows)]
                    numRows, numCols = DISPLAY_RESOLUTION[1] // CELL_SIZES[SIZE], DISPLAY_RESOLUTION[0] // CELL_SIZES[SIZE]
                
                # # up and down keys will change the cell size
                if paused and event.key == pygame.K_DOWN:
                    if SIZE > 0:
                        SIZE -= 1
                        numRows, numCols = DISPLAY_RESOLUTION[1] // CELL_SIZES[SIZE], DISPLAY_RESOLUTION[0] // CELL_SIZES[SIZE]
                        oldGrid = grid
                        grid = [[False for _ in range(numCols)] for _ in range(numRows)]
                        gridCopy(oldGrid, grid)  
                    
                if paused and event.key == pygame.K_UP:
                    if SIZE < len(CELL_SIZES) - 1:
                        SIZE += 1
                        numRows, numCols = DISPLAY_RESOLUTION[1] // CELL_SIZES[SIZE], DISPLAY_RESOLUTION[0] // CELL_SIZES[SIZE]
                        oldGrid = grid
                        grid = [[False for _ in range(numCols)] for _ in range(numRows)]
                        gridCopy(oldGrid, grid)  
                
                # Left and right keys will change the game speed
                if not paused and event.key == pygame.K_LEFT:
                    if SPEED > 1:
                        SPEED -= 1
                if not paused and event.key == pygame.K_RIGHT:
                    if SPEED < 5:
                        SPEED += 1

            # Clicking a cell flips it between alive and dead.
            if paused and event.type == pygame.MOUSEBUTTONDOWN:
                pos = positionToIndex(pygame.mouse.get_pos())
                grid[pos[0]][pos[1]] = not grid[pos[0]][pos[1]]

            # Handle exit condition
            if event.type == pygame.QUIT:
                running = False
                break
        
        # Computing
        if not paused:
            grid = mutate(grid)
            dt = clock.tick(SPEED)
            
            # if grid is empty, lets automatically pause the game as nothing is running.
            if grid == [[False for _ in range(numCols)] for _ in range(numRows)]:
                paused = pause(paused)

        # Rendering
        screen.fill(GREY)
        drawGrid(grid, screen)
        pygame.display.flip()     

    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()