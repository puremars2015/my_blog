from PIL import Image
import os

def convert_webp_to_ico(input_path, output_path):
    """
    Convert a WebP image to ICO format.
    
    :param input_path: Path to the input WebP image
    :param output_path: Path to save the output ICO file
    """
    try:
        # Open the WebP image
        with Image.open(input_path) as img:
            # Ensure image is in RGBA mode
            img = img.convert("RGBA")
            # Save as ICO
            img.save(output_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        print(f"Converted successfully: {output_path}")
    except Exception as e:
        print(f"Error converting {input_path} to ICO: {e}")

if __name__ == "__main__":
    # Input and output file paths
    input_webp = input("Enter the path to the WebP image: ").strip()
    output_ico = input("Enter the path to save the ICO file (e.g., output/favicon.ico): ").strip()

    # Ensure output directory exists
    output_dir = os.path.dirname(output_ico)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert the image
    convert_webp_to_ico(input_webp, output_ico)
