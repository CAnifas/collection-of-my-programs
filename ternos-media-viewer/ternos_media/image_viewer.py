import os
import sys
import argparse
from PIL import Image
from ternos_media.renderer import get_scaled_dimensions, render_image_to_ansi

def main():
    # Enable ANSI escape sequences on Windows consoles
    if sys.platform == "win32":
        os.system("")
        
    # Reconfigure stdout to support UTF-8 characters like half-blocks
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description="imgTernos - Render images (PNG/JPG) directly in the terminal."
    )
    parser.add_argument("image_path", help="Path to the image file (JPG, PNG, etc.)")
    parser.add_argument("-w", "--width", type=int, help="Override target width in character cells")
    parser.add_argument("-t", "--height", type=int, help="Override target height in terminal lines")
    
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"Error: File not found at '{args.image_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        with Image.open(args.image_path) as img:
            # User height option is in terminal lines; convert to pixels (1 line = 2 vertical pixels)
            max_h_px = args.height * 2 if args.height else None
            
            target_w, target_h = get_scaled_dimensions(
                img.width, img.height, 
                max_w=args.width, 
                max_h=max_h_px
            )
            
            ansi_art = render_image_to_ansi(img, target_w, target_h)
            print(ansi_art)
    except Exception as e:
        print(f"Error rendering image: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
