from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter  = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def draw_rect_alpha(surface, color, rect, alpha = 128):
    shape_surf = None
    if isinstance(color, tuple) and len(color) > 3:
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    else:
        shape_surf = pygame.Surface(pygame.Rect(rect).size)
        shape_surf.set_alpha(alpha)
        shape_surf.fill(color)
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius, alpha = 128):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = None
    if isinstance(color, tuple) and len(color) > 3:
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    else:
        shape_surf = pygame.Surface(target_rect.size)
        shape_surf.set_alpha(alpha)
        shape_surf.fill(color)
    surface.blit(shape_surf, target_rect)

def draw_polygon_alpha(surface, color, points, alpha = 128):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = None
    if isinstance(color, tuple) and len(color) > 3:
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    else:
        shape_surf = pygame.Surface(target_rect.size)
        shape_surf.set_alpha(alpha)
        shape_surf.fill(color)
    surface.blit(shape_surf, target_rect)