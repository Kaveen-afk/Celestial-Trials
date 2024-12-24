import pygame

class Projectile:
    def __init__(self, x, y, width, height, image, target, speed=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)  # Load the bullet image
        self.speed = speed
        self.target = target
        self.velocity = self.calculate_velocity()

    def calculate_velocity(self):
        # Calculate the direction vector from the projectile to the target
        target_center = self.target.get_center()
        dx = target_center[0] - self.x
        dy = target_center[1] - self.y
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        # Normalize the velocity for consistent speed
        return [dx / magnitude * self.speed, dy / magnitude * self.speed]

    def update(self):
        # Update the projectile's position
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self, window):
        # Draw the projectile (bullet) to the screen
        window.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def check_collision(self, obj):
        # Check for collision with another object (like an enemy)
        x1, y1 = self.get_center()
        x2, y2 = obj.get_center()
        w1, h1 = self.width / 2, self.height / 2
        w2, h2 = obj.collider[0] / 2, obj.collider[1] / 2
        if x1 + w1 > x2 - w2 and x1 - w1 < x2 + w2:
            return y1 + h1 > y2 - h2 and y1 - h1 < y2 + h2
        return False
