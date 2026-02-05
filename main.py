"""
PixelOS v1.4 - Main Entry Point
Sistema operativo retro en pixels
"""

import pygame
from core.engine import PixelOS

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create the operating system
    pixel_os = PixelOS()
    
    # Run the main loop
    pixel_os.run()

if __name__ == "__main__":
    main()
