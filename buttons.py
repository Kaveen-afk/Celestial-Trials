import pygame

class Button:
    def __init__(self, x, y, image, scale=1):
        """
        Initialize the Button.

        Args:
            x (int): X-coordinate of the top-left corner of the button.
            y (int): Y-coordinate of the top-left corner of the button.
            image (pygame.Surface): The button's image.
            scale (float): The scaling factor for the image.
        """
        # Scale the image
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
        Draw the button on the screen and check for clicks.

        Args:
            surface (pygame.Surface): The surface to draw the button on.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        action = False
        # Get the mouse position
        pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        # Reset click status when the mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


        