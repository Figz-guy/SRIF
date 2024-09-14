from PIL import Image
import lzma
import struct
import sys
import os

def decode_srif_to_png(input_srif_path, output_png_path):
    with open(input_srif_path, 'rb') as file:
        magic_number = file.read(4)
        if magic_number != b'SRIF':
            raise ValueError("Not a valid .srif file")
        
        width = struct.unpack('I', file.read(4))[0]
        height = struct.unpack('I', file.read(4))[0]
        
        compressed_data = file.read()
        raw_data = lzma.decompress(compressed_data)
        
        img = Image.frombytes('RGBA', (width, height), raw_data)
        img.save(output_png_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: drag a .srif file onto this script")
        sys.exit(1)

    input_srif_path = sys.argv[1]
    if not input_srif_path.lower().endswith('.srif'):
        print("The input file must be a .srif file")
        sys.exit(1)

    if not os.path.isfile(input_srif_path):
        print("File does not exist")
        sys.exit(1)

    output_png_path = os.path.splitext(input_srif_path)[0] + '_restored.png'
    decode_srif_to_png(input_srif_path, output_png_path)
    print(f"Decoded file saved as {output_png_path}")
