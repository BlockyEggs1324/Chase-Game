import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

print("0 - Custom, 1 - 1920 x 1080, 2 - 1680 x 1050, 3 - 1600 x 900, 4 - 2560, 1440, 5 - 2048 x 1440")

win = int(input("Enter window size option: "))

if win == 0:
   width = int(input("Enter game width: "))
   height = int(input("Enter game height: "))
if win == 1:
   width, height = 1920, 1080
elif win == 2:
    width, height = 1680, 1050
elif win == 3:
    width, height = 1600, 900
elif win == 4:
    width, height = 2560, 1440
elif win == 5:
    width, height = 2048, 1440
else:
    width, height = 1920, 1080



# Set up the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chasing Squares")

# Set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK_SQUARE = (0, 0, 0)
WHITE = (255, 255, 255)

score_text = "1"
font = pygame.font.Font('freesansbold.ttf', 32)
score = font.render(score_text, True, WHITE, None)

scoreRect = score.get_rect()
scoreRect.center = (width // 2, 20)

#define variables

# Set up the squares
square1_pos = [50, 50]
square1_original_pos = square1_pos.copy()
square1_it = bool(random.getrandbits(1))  # Randomly determine if square 1 starts as "it" or not
square1_cooldown = False
square1_cooldown_duration = 1  # Cooldown duration in seconds
square1_cooldown_start_time = 0
square1_move = True

square2_pos = [width - 50, height - 50]
square2_original_pos = square2_pos.copy()
square2_it = not square1_it  # Square 2 is "it" if square 1 is not "it"
square2_cooldown = False
square2_cooldown_duration = 1  # Cooldown duration in seconds
square2_cooldown_start_time = 0
square2_move = True

square_speed = 1.5

# Set up the obstacles
obstacles = []
num_obstacles = 150
obstacle_size = 50
failed_obstacles = 0
for _ in range(num_obstacles + failed_obstacles):
    x = random.randint(obstacle_size, width - obstacle_size)
    y = random.randint(obstacle_size, height - obstacle_size)
    if x < 100 or y < 100 or x > width - 150 or y > height - 150:
        failed_obstacles += 1
    else:
        obstacles.append(pygame.Rect(x, y, obstacle_size, obstacle_size))

def reset_game():
    print("Game Reset")
    # Set up the squares
    square1_pos = square1_original_pos.copy()
    square1_it = bool(random.getrandbits(1))  # Randomly determine if square 1 starts as "it" or not
    square1_cooldown = False
    square1_move = True
      
    square2_pos = square2_original_pos.copy()
    square2_it = not square1_it  # Square 2 is "it" if square 1 is not "it"
    square2_cooldown = False
    square2_move = True
    # Set up the obstacles
    for obstacle in obstacles:
        obstacles.remove(obstacle)
    failed_obstacles = 0
    for _ in range(num_obstacles + failed_obstacles):
        x = random.randint(obstacle_size, width - obstacle_size)
        y = random.randint(obstacle_size, height - obstacle_size)
        if x < 100 or y < 100 or x > width - 150 or y > height - 150:
            failed_obstacles += 1
        else:
            obstacles.append(pygame.Rect(x, y, obstacle_size, obstacle_size))
            
reset_game()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Move square 1
    if keys[pygame.K_a] and square1_pos[0] > square_speed and square1_move:
        square1_pos[0] -= square_speed
    if keys[pygame.K_d] and square1_pos[0] < width - 50 - square_speed and square1_move:
        square1_pos[0] += square_speed
    if keys[pygame.K_w] and square1_pos[1] > square_speed and square1_move:
        square1_pos[1] -= square_speed
    if keys[pygame.K_s] and square1_pos[1] < height - 50 - square_speed and square1_move:
        square1_pos[1] += square_speed

    # Move square 2
    if keys[pygame.K_LEFT] and square2_pos[0] > square_speed and square2_move:
        square2_pos[0] -= square_speed
    if keys[pygame.K_RIGHT] and square2_pos[0] < width - 50 - square_speed and square2_move:
        square2_pos[0] += square_speed
    if keys[pygame.K_UP] and square2_pos[1] > square_speed and square2_move:
        square2_pos[1] -= square_speed
    if keys[pygame.K_DOWN] and square2_pos[1] < height - 50 - square_speed and square2_move:
        square2_pos[1] += square_speed

    #if keys[pygame.K_k]:
        #square1_move = False
        #time.sleep(2)
        #square1_move = True
    #if keys[pygame.K_l]:
        #square2_move = False
        #time.sleep(2)
        #square2_move = True

    if keys[pygame.K_r]:
        reset_game()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    # Check for collision with obstacles
    for obstacle in obstacles:
        if pygame.Rect(square1_pos[0], square1_pos[1], 50, 50).colliderect(obstacle):
            square1_it = True
            square2_it = False
            square1_pos = square1_original_pos.copy()
            print("Player 1 Game Over!")

        if pygame.Rect(square2_pos[0], square2_pos[1], 50, 50).colliderect(obstacle):
            square1_it = False
            square2_it = True
            square2_pos = square2_original_pos.copy()
            print("Player 2 Game Over!")

    # Check for collision between squares
    if pygame.Rect(square1_pos[0], square1_pos[1], 50, 50).colliderect(pygame.Rect(square2_pos[0], square2_pos[1], 50, 50)):
        if square1_it and not square1_cooldown and not square2_cooldown:
            square1_it = False
            square2_it = not square1_it
            square1_cooldown = True
            square1_cooldown_start_time = time.time()
            print("Player 1 caught player 2")

        elif square2_it and not square2_cooldown and not square1_cooldown:
            square1_it = True
            square2_it = not square1_it
            square2_cooldown = True
            square2_cooldown_start_time = time.time()
            print("Player 2 caught player 1")
            
    screen.blit(score, scoreRect)
    
    # Check cooldown status for square 1
    if square1_cooldown:
        current_time = time.time()
        if current_time - square1_cooldown_start_time >= square1_cooldown_duration:
            square1_cooldown = False

    # Check cooldown status for square 2
    if square2_cooldown:
        current_time = time.time()
        if current_time - square2_cooldown_start_time >= square2_cooldown_duration:
            square2_cooldown = False

    # Draw the squares and obstacles
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, (square1_pos[0], square1_pos[1], 50, 50))
    pygame.draw.rect(screen, BLUE, (square2_pos[0], square2_pos[1], 50, 50))
        
    if square1_it == True:
        pygame.draw.rect(screen, BLACK_SQUARE, (square1_pos[0] + 20, square1_pos[1] + 20, 10, 10))
        
    if square1_it == False:
        pygame.draw.rect(screen, BLACK_SQUARE, (square2_pos[0] + 20, square2_pos[1] + 20, 10, 10))
        
    if square2_it == True:
        pygame.draw.rect(screen, BLACK_SQUARE, (square2_pos[0] + 20, square2_pos[1] + 20, 10, 10))
    
    if square2_it == False:
        pygame.draw.rect(screen, BLACK_SQUARE, (square1_pos[0] + 20, square1_pos[1] + 20, 10, 10))

    if obstacles == []:
        for obstacle in obstacles:
            pygame.draw.rect(screen, (BLACK), obstacle)

    else:
        for obstacle in obstacles:
            pygame.draw.rect(screen, (WHITE), obstacle)
    # Update the display
    pygame.display.flip()
