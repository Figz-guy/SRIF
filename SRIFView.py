import pygame
import lzma
import struct
import sys
import os
import time
from io import BytesIO

def decode_srif(input_srif_path):
    with open(input_srif_path, 'rb') as file:
        magic_number = file.read(4)
        if magic_number != b'SRIF':
            raise ValueError("Not a valid .srif file")
        
        width = struct.unpack('I', file.read(4))[0]
        height = struct.unpack('I', file.read(4))[0]
        
        compressed_data = file.read()
        raw_data = lzma.decompress(compressed_data)
        
        return width, height, raw_data

def main():
    if len(sys.argv) != 2:
        print("Usage: drag a .srif file onto this script")
        sys.exit(1)

    srif_path = sys.argv[1]

    if not srif_path.lower().endswith('.srif'):
        print("The input file must be a .srif file")
        sys.exit(1)

    if not os.path.isfile(srif_path):
        print("File does not exist")
        sys.exit(1)

    pygame.init()
    width, height, raw_data = decode_srif(srif_path)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Live SRIF Viewer')

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if the file has been updated
        if os.path.getmtime(srif_path) > time.time() - 1:  # Check if updated in the last second
            width, height, raw_data = decode_srif(srif_path)

        # Convert raw data to Pygame surface
        image = pygame.image.fromstring(raw_data, (width, height), 'RGBA')

        # Draw the image
        screen.blit(image, (0, 0))
        pygame.display.flip()

        clock.tick(30)  # Cap the frame rate to 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
