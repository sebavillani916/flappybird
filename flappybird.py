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
bird_img = pygame.image.load("images/jerry.png").convert() 
pipe_img = pygame.image.load("images/pipes.png").convert()
background_img = pygame.image.load("images/background-day.png").convert()

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

        if self.y > HEIGHT - 40:
            self.y = HEIGHT - 40
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def jump(self):
        self.velocity += self.lift

# Pipe class
class Pipe:
    def __init__(self):
        self.top = random.randint(50, HEIGHT - 250)
        self.bottom = HEIGHT - self.top - 200
        self.x = WIDTH
        self.width = 40
        self.speed = 3

    def show(self):
        screen.blit(pipe_img, (self.x, 0), (0, 0, self.width, self.top))
        screen.blit(pipe_img, (self.x, HEIGHT - self.bottom), (0, pipe_img.get_height() - self.bottom, self.width, self.bottom))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.width

# Game variables
bird = Bird()
pipes = []
score = 0

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

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

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
