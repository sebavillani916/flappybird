import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load("images/bluebird-downflap.png").convert() 
birdYellow_img = pygame.image.load("images/yellowbird-upflap.png").convert() 
birdRed_img = pygame.image.load("images/redbird-upflap.png").convert() 

bird_img = random.choice([bird_img, birdYellow_img, birdRed_img])

pipe_img = pygame.image.load("images/pipe-green.png").convert()

# Load and scale the background image to fit the screen
background_img = pygame.image.load("images/background-day.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

backgroundN_img = pygame.image.load("images/background-night.png").convert()
backgroundN_img = pygame.transform.scale(backgroundN_img, (WIDTH, HEIGHT))

# Randomly select day or night background
background_img = random.choice([background_img, backgroundN_img])

# Load and scale the floor image to fit the screen width
floor_img = pygame.image.load("images/base.png").convert()
floor_height = 100  # Set the desired height for the floor area
floor_img = pygame.transform.scale(floor_img, (WIDTH, floor_height))

# Load the game over image
game_over_img = pygame.image.load("images/scoreboard.png").convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (300, 400))  

# Load sound files
wing_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
swoosh_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
die_sound = pygame.mixer.Sound("sound/sfx_die.wav")
point_sound = pygame.mixer.Sound("sound/sfx_point.wav")

# Set volume levels
wing_sound.set_volume(0.3)  
swoosh_sound.set_volume(0.3)  
hit_sound.set_volume(0.3)  
die_sound.set_volume(0.3)  
point_sound.set_volume(0.3)  

def read_high_score():
    try:
        with open("high_score.txt", "r") as f:
            high_score_str = f.read().strip()
            if high_score_str:
                return int(high_score_str)
            else:
                return 0
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

high_score = read_high_score()

def update_high_score(new_score):
    global high_score
    if new_score > high_score:
        high_score = new_score
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))

def title_screen():
    play_button_img = pygame.image.load("images/play_button.png").convert_alpha()  # Load play button image
    # Scale the play button image
    play_button_img = pygame.transform.scale(play_button_img, (200, 90))
    play_button_rect = play_button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Position the play button

    title_image = pygame.image.load("images/logo.png").convert_alpha()  # Load title image
    title_image = pygame.transform.scale(title_image, (350, 130))  # Scale the title image (adjust size as needed)
    title_rect = title_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))  # Position the title image above the play button


    title_running = True
    while title_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                title_running = False
                pygame.quit()
                exit()  # Exit the game if the close button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    title_running = False  # Exit the title screen loop to start the game

        screen.blit(background_img, (0, 0))  # Use the same background for the title screen
        screen.blit(title_image, title_rect)  # Draw the title image
        screen.blit(play_button_img, play_button_rect)  # Draw the play button

        pygame.display.flip()
        clock.tick(60)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10

    def show(self):
        screen.blit(bird_img, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Adjust for floor collision
        if self.y > HEIGHT - 100 - 40:  # Assuming 40 is the bird's height
            self.y = HEIGHT - 100 - 40
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

     # Check for ceiling collision
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def jump(self):
        self.velocity += self.lift
        wing_sound.play()  # Play wing sound when the bird jumps
        swoosh_sound.play()  # Play swooshing sound when the bird jumps

# Pipe class
class Pipe:
    def __init__(self):
        self.top = random.randint(50, HEIGHT - 250 - 100)  # Adjusted to ensure top pipes do not stretch out of the screen
        self.bottom = HEIGHT - self.top - 200  # Adjusted to ensure bottom pipes do not appear under the background
        self.x = WIDTH
        self.width = 40
        self.speed = 3

    def show(self):
        # Top pipe
        top_pipe_img = pygame.transform.flip(pipe_img, False, True)  # Flip the pipe image for the top pipe
        screen.blit(top_pipe_img, (self.x, self.top - top_pipe_img.get_height()))

        # Bottom pipe
        screen.blit(pipe_img, (self.x, HEIGHT - self.bottom))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.width

def game_over_screen():
    global high_score
    restart_button_img = pygame.image.load("images/play_again.png").convert_alpha()
    restart_button_img = pygame.transform.scale(restart_button_img, (200, 60))
    restart_button_rect = restart_button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    game_over_rect = game_over_img.get_rect(center=(WIDTH // 2, restart_button_rect.top - 100))  # Adjust the vertical offset as needed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return  # Exit the function to restart the game immediately

        screen.blit(background_img, (0, 0))
        screen.blit(game_over_img, game_over_rect)  # Display the game over image
        screen.blit(restart_button_img, restart_button_rect)
        
       # Display the high score inside the scoreboard image
        high_score_font = pygame.font.Font(None, 36)
        high_score_text = high_score_font.render(str(high_score), True, BLACK)
        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2 + 89, game_over_rect.top + 165))  # Adjust the x-coordinate to move the text to the right

        screen.blit(high_score_text, high_score_rect)


        pygame.display.flip()
        clock.tick(60)

# Game variables
bird = Bird()
pipes = []
score = 0
floor_height = 100  # Define the floor height
game_over = False

# Main game loop
running = True
clock = pygame.time.Clock()

title_screen()  # Display the title screen before starting the game loop

while running:
    if game_over:
        update_high_score(score)
        game_over_screen()  
        bird = Bird()
        pipes = []
        score = 0
        game_over = False
        # Removed the call to title_screen()
        continue  # Continue with the next iteration of the loop, effectively restarting the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
                wing_sound.play()  # Play wing sound when the bird jumps
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button clicks
            bird.jump()  # Make the bird jump on mouse click
            wing_sound.play()  # Play wing sound when the bird jumps

    if not game_over:
        # Check for collisions
        for pipe in pipes:
            if bird.x + bird_img.get_width() > pipe.x and bird.x < pipe.x + pipe.width:
                if bird.y < pipe.top or bird.y + bird_img.get_height() > HEIGHT - pipe.bottom:
                    game_over = True
                    hit_sound.play()  # Play hit sound when the bird collides with the pipes
                    die_sound.play()  # Play die sound when the game is over
                    break

            if pipe.x == bird.x - pipe.width:
                score += 1
                point_sound.play()  # Play point sound when the bird gets a point

        # Update bird
        bird.update()

        # Generate pipes
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 150:
            pipes.append(Pipe())

        # Update pipes 
        for pipe in pipes:
            pipe.update()
            if pipe.offscreen():
                pipes.remove(pipe)

    # Draw everything
    screen.blit(background_img, (0, 0))  # Draw the background first
    bird.show()
    for pipe in pipes:
        pipe.show()
    screen.blit(floor_img, (0, HEIGHT - floor_height))  # Draw the floor

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit
