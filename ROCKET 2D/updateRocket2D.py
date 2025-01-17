import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket vs UFOs")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Load images
rocket_img = pygame.image.load("rocket.png")  # Rocket image
rocket_img = pygame.transform.scale(rocket_img, (50, 60))
ufo_img = pygame.image.load("ufo.png")  # UFO image
ufo_img = pygame.transform.scale(ufo_img, (50, 40))
alien_img = pygame.image.load("alien.png")  # Alien Warrior image
alien_img = pygame.transform.scale(alien_img, (50, 50))

# High score file
HIGH_SCORE_FILE = "high_score.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))


# Classes
class Rocket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 5
        self.width = 50
        self.height = 60
        self.bullets = []
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def shoot(self):
        bullet = pygame.Rect(self.x + self.width // 2 - 5, self.y, 10, 20)
        self.bullets.append(bullet)

    def draw(self):
        screen.blit(rocket_img, (self.x, self.y))
        for bullet in self.bullets:
            pygame.draw.rect(screen, RED, bullet)

    def update_bullets(self, ufos):
        for bullet in self.bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                self.bullets.remove(bullet)
            else:
                for ufo in ufos[:]:
                    if bullet.colliderect(ufo.rect):
                        self.bullets.remove(bullet)
                        ufos.remove(ufo)
                        return True
        return False


class UFO:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-100, -40)
        self.speed = speed
        self.width = 50
        self.height = 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        screen.blit(ufo_img, (self.x, self.y))


class Alien:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-200, -100)
        self.speed = speed
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        screen.blit(alien_img, (self.x, self.y))


# Game function
def main():
    rocket = Rocket()
    ufos = []
    aliens = []
    score = 0
    level = 1
    high_score = load_high_score()
    running = True
    game_over = False

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    rocket.shoot()
                if event.key == pygame.K_RETURN and game_over:
                    return True  # Restart game

        if not game_over:
            # Spawn UFOs
            if random.randint(1, max(50 - level * 2, 10)) == 1:
                ufos.append(UFO(speed=random.randint(2, 4) + level // 2))

            # Spawn Aliens
            if random.randint(1, max(100 - level * 3, 20)) == 1:
                aliens.append(Alien(speed=random.randint(2, 4) + level // 2))

            # Update and draw UFOs
            for ufo in ufos[:]:
                ufo.move()
                if ufo.y > HEIGHT:
                    ufos.remove(ufo)
                else:
                    ufo.draw()

            # Update and draw Aliens
            for alien in aliens[:]:
                alien.move()
                if alien.y > HEIGHT:
                    aliens.remove(alien)
                elif alien.rect.colliderect(rocket.rect):
                    game_over = True
                else:
                    alien.draw()

            # Update rocket and bullets
            keys = pygame.key.get_pressed()
            rocket.move(keys)
            if rocket.update_bullets(ufos):
                score += 1
                if score > high_score:
                    high_score = score
                if score % 10 == 0:  # Increase level every 10 points
                    level += 1

            rocket.draw()

            # Display score and level
            score_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 50))
            screen.blit(level_text, (10, 90))

        else:
            # Game Over Screen
            game_over_text = large_font.render("GAME OVER", True, RED)
            restart_text = font.render("Press ENTER to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - 170, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

    save_high_score(high_score)
    pygame.quit()


# Run the game
while main():
    pass
