import pygame


class InputBox:
    MAX_STRING_LENGTH = len("255.255.255.255")

    def __init__(self, rect):
        self.value = ""
        self.rect = rect
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.callback = lambda: None

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, 8)
        text_img = self.font.render(self.value, True, (255, 255, 255))
        text_size = text_img.get_size()
        screen.blit(text_img, (self.rect.centerx - text_size[0]//2, self.rect.centery - text_size[1]//2))

    def poll_input(self, event):
        whitelist = "1234567890."
        if event.type == pygame.KEYDOWN:
            if event.unicode in whitelist:
                self.value = self.value[:InputBox.MAX_STRING_LENGTH - 1] + event.unicode
            elif event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key == pygame.K_RETURN:
                self.callback()

    def connect(self, callback):
        self.callback = callback
        return self
