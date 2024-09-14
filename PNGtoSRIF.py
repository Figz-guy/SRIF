from PIL import Image
import lzma
import struct
import sys
import os

def encode_png_to_srif(input_png_path, output_srif_path):
    with Image.open(input_png_path) as img:
        img = img.convert('RGBA')
        width, height = img.size
        raw_data = img.tobytes()

    compressed_data = lzma.compress(raw_data)

    with open(output_srif_path, 'wb') as file:
        file.write(b'SRIF')
        file.write(struct.pack('I', width))
        file.write(struct.pack('I', height))
        file.write(compressed_data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: drag a .png file onto this script")
        sys.exit(1)

    input_png_path = sys.argv[1]
    if not input_png_path.lower().endswith('.png'):
        print("The input file must be a .png file")
        sys.exit(1)

    if not os.path.isfile(input_png_path):
        print("File does not exist")
        sys.exit(1)

    output_srif_path = os.path.splitext(input_png_path)[0] + '.srif'
    encode_png_to_srif(input_png_path, output_srif_path)
    print(f"Encoded file saved as {output_srif_path}")

