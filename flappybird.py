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
pipe_img = pygame.image.load("images/pipe-green.png").convert()
# Load and scale the background image to fit the screen
background_img = pygame.image.load("images/background-day.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Load and scale the floor image to fit the screen width
floor_img = pygame.image.load("images/base.png").convert()
floor_height = 100  # Set the desired height for the floor area
floor_img = pygame.transform.scale(floor_img, (WIDTH, floor_height))

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

# Game variables
bird = Bird()
pipes = []
score = 0
floor_height = 100  # Define the floor height

# Main game loop
running = True
clock = pygame.time.Clock()

title_screen()  # Display the title screen before starting the game loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button clicks
            bird.jump()  # Make the bird jump on mouse click



    # Check for collisions
    for pipe in pipes:
        if bird.x + bird_img.get_width() > pipe.x and bird.x < pipe.x + pipe.width:
            if bird.y < pipe.top or bird.y + bird_img.get_height() > HEIGHT - pipe.bottom:
                # running = False
                # break
                print("hit pipe")
                pass

        if pipe.x == bird.x - pipe.width:
            score += 1

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

pygame.quit()
