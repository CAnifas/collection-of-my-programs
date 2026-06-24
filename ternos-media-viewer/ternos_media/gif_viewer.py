import os
import sys
import time
import argparse
from PIL import Image, ImageSequence
from ternos_media.renderer import get_scaled_dimensions, render_image_to_ansi

def load_gif_frames(img: Image.Image):
    """
    Loads all frames of a GIF, handling transparency and disposal methods.
    Returns lists of (frame_image, duration_in_seconds).
    """
    frames = []
    durations = []
    
    canvas = Image.new("RGBA", img.size)
    prev_canvas = None
    
    for frame in ImageSequence.Iterator(img):
        # Extract duration (default to 100ms)
        d = frame.info.get("duration", 100)
        if d == 0:
            d = 100
        durations.append(d / 1000.0)
        
        disposal = frame.info.get("disposal", 2)
        
        if disposal == 3 and prev_canvas is not None:
            canvas = prev_canvas.copy()
            
        current = frame.convert("RGBA")
        
        if disposal != 3:
            prev_canvas = canvas.copy()
            
        canvas.alpha_composite(current)
        frames.append(canvas.copy())
        
        if disposal == 2:
            canvas = Image.new("RGBA", img.size)
            
    return frames, durations

def main():
    # Enable ANSI escape sequences on Windows
    if sys.platform == "win32":
        os.system("")

    # Reconfigure stdout to support UTF-8 characters like half-blocks
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description="TernosSyS - Render animated GIFs directly in the terminal."
    )
    parser.add_argument("gif_path", help="Path to the GIF file")
    parser.add_argument("-w", "--width", type=int, help="Override target width in character cells")
    parser.add_argument("-t", "--height", type=int, help="Override target height in terminal lines")
    parser.add_argument("-l", "--loops", type=int, default=0, help="Number of loops to run (0 for infinite)")
    
    args = parser.parse_args()

    if not os.path.exists(args.gif_path):
        print(f"Error: File not found at '{args.gif_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        gif = Image.open(args.gif_path)
    except Exception as e:
        print(f"Error opening GIF: {e}", file=sys.stderr)
        sys.exit(1)

    # Hide cursor and ensure we restore it on exit
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()

    try:
        frames, durations = load_gif_frames(gif)
    except Exception as e:
        sys.stdout.write("\x1b[?25h\x1b[0m\n")
        sys.stdout.flush()
        print(f"Error processing GIF frames: {e}", file=sys.stderr)
        sys.exit(1)

    num_frames = len(frames)
    loop_count = 0
    prev_lines_count = 0

    try:
        while True:
            for idx in range(num_frames):
                frame_start_time = time.time()
                
                # Dynamically calculate size for each frame (supports responsive terminal resizing)
                max_h_px = args.height * 2 if args.height else None
                target_w, target_h = get_scaled_dimensions(
                    gif.width, gif.height,
                    max_w=args.width,
                    max_h=max_h_px
                )
                
                ansi_frame = render_image_to_ansi(frames[idx], target_w, target_h)
                current_lines_count = target_h // 2
                
                # Move cursor back up to overwrite previous frame
                if prev_lines_count > 0:
                    sys.stdout.write(f"\x1b[{prev_lines_count}A")
                
                # Print the new frame
                sys.stdout.write(ansi_frame + "\n")
                
                # If the new frame is shorter, clear leftover lines at the bottom
                if current_lines_count < prev_lines_count:
                    diff = prev_lines_count - current_lines_count
                    # Clear each extra line below
                    sys.stdout.write("\n".join(["\x1b[K"] * diff))
                    # Move back up to the end of the new frame
                    sys.stdout.write(f"\x1b[{diff}A")
                
                sys.stdout.flush()
                prev_lines_count = current_lines_count
                
                # Calculate sleep time, subtracting the time spent rendering
                elapsed = time.time() - frame_start_time
                sleep_time = max(0.0, durations[idx] - elapsed)
                time.sleep(sleep_time)
                
            loop_count += 1
            if args.loops > 0 and loop_count >= args.loops:
                break
                
    except KeyboardInterrupt:
        # User cancelled playback
        pass
    finally:
        # Restore terminal settings: show cursor, reset color, and add final newline
        sys.stdout.write("\x1b[?25h\x1b[0m\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
