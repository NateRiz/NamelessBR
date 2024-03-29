import pygame


class Button:
    """
    Clickable button that can attach to a callback
    """
    def __init__(self, rect, callback, text):
        self.rect: pygame.rect.Rect = rect
        self.callback = callback
        self.is_enabled = True
        self.is_hidden = False
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.text_img = self.font.render(text, True, (255, 255, 255))
        self.color = (0, 245, 255)

    def draw(self, screen: pygame.surface.Surface):
        """
        Draw the button to the screen
        :param screen: Pygame screen
        """
        if self.is_hidden:
            return

        pygame.draw.rect(screen, self.color, self.rect, 2, 8)
        text_size = self.text_img.get_size()
        screen.blit(self.text_img, (self.rect.centerx - text_size[0]//2, self.rect.centery - text_size[1]//2))

    def poll_input(self, event):
        """
        Check to see if the user clicked the button
        :param event: user polled event
        """
        if not self.is_enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._is_hovering():
                self.callback()

    def _is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def set_disabled(self):
        """
        Clicking the button will not call the callback when enabled
        """
        self.is_enabled = False

    def set_enabled(self):
        """
        Clicking the button will call the callback when enabled
        """
        self.is_enabled = True

    def set_hidden(self, is_hidden):
        """
        Button does not get drawn if enabled
        :param is_hidden: if button is hidden
        """
        self.is_hidden = is_hidden
