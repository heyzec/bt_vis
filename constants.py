import pygame

BOARD_UPDATED = pygame.event.custom_type()
BOARD_REFRESH = pygame.event.custom_type()

BLACK = pygame.Color('#000000')
WHITE = pygame.Color('#FFFFFF')
BEIGE = pygame.Color('#f0bc7a')

PIPE_FILE_SEND_USER_ACTION = '/tmp/send_user_action'
PIPE_FILE_BOARD_UPDATES = '/tmp/board_updates'
