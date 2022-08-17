import pygame
from support import draw_rect_alpha

pygame.init()
font = pygame.font.Font(None,30)

def debug(info,y = 100, x = 20):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	draw_rect_alpha(display_surface,'Black',debug_rect.inflate(20, 20))
	display_surface.blit(debug_surf,debug_rect)
