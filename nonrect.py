import pygame
import ctypes
from ctypes import wintypes

# Initialize Pygame
pygame.init()

# Create a transparent Pygame window
window = pygame.display.set_mode((800, 600), pygame.NOFRAME)
pygame.display.set_caption("Non-rectangular Window")

# Load the window shape image with an alpha channel
window_shape_image = pygame.image.load("window_shape.png")

# Convert the image to a compatible format
window_shape_image = window_shape_image.convert_alpha()

# Get the window handle
hwnd = pygame.display.get_wm_info()["window"]

# Get the window dimensions
width, height = pygame.display.get_surface().get_size()

# Define the window shape region based on the alpha channel of the image
mask = pygame.mask.from_surface(window_shape_image)

# Get the outline of the shape as a set of points
shape_outline = mask.outline()

# Create a list of points for the region
region_points = []
for outline_point in shape_outline:
    region_points.append((outline_point[0], outline_point[1]))

# Create a region from the points
region = (wintypes.POINT * len(region_points))(*region_points)
mask = ctypes.windll.gdi32.CreatePolygonRgn(region, len(region), 1)

# Set the window shape using the region
ctypes.windll.user32.SetWindowRgn(hwnd, mask, True)

# Define the BLENDFUNCTION structure
class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ("BlendOp", ctypes.c_byte),
        ("BlendFlags", ctypes.c_byte),
        ("SourceConstantAlpha", ctypes.c_byte),
        ("AlphaFormat", ctypes.c_byte)
    ]

# Make the window transparent
blend = BLENDFUNCTION()
blend.BlendOp = 0
blend.BlendFlags = 0
blend.SourceConstantAlpha = 255
blend.AlphaFormat = 1

flags = 0x0001 | 0x0002  # LWA_COLORKEY | LWA_ALPHA
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, flags)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

# Cleanup
pygame.quit()
