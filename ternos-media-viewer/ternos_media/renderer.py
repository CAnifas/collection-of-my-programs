import os
from PIL import Image

def get_scaled_dimensions(orig_w, orig_h, max_w=None, max_h=None):
    """
    Calculates the best target dimensions to scale an image to fit inside the terminal
    while maintaining the aspect ratio.
    
    Note: Since we use Unicode half-blocks (top half and bottom half), we fit two vertical 
    pixels into one terminal character cell. In modern terminal fonts, a character cell is
    approximately twice as tall as it is wide. Therefore, drawing two vertical pixels per cell 
    results in an almost perfect 1:1 pixel aspect ratio.
    """
    try:
        term_w, term_h = os.get_terminal_size()
    except OSError:
        term_w, term_h = 80, 24

    if max_w is None:
        max_w = term_w
    if max_h is None:
        # Leave 2 terminal lines of breathing room for shell prompt and layout
        max_h = max(2, (term_h - 2) * 2)

    img_ratio = orig_w / orig_h
    term_ratio = max_w / max_h

    if img_ratio > term_ratio:
        # Width is the limiting factor
        w = max_w
        h = int(w / img_ratio)
    else:
        # Height is the limiting factor
        h = max_h
        w = int(h * img_ratio)

    # Ensure dimensions are valid and height is even for pairing top/bottom half blocks
    w = max(1, w)
    h = max(2, (h // 2) * 2)

    return w, h

def render_image_to_ansi(image: Image.Image, target_width: int, target_height: int) -> str:
    """
    Resizes a Pillow Image and converts it into an ANSI escape sequence string
    using half-blocks (▀ and ▄) for double vertical resolution and transparency support.
    """
    # Resize the image using high-quality Resampling (LANCZOS or BILINEAR)
    # Pillow 9+ has Resampling enum, but we fall back to older names if needed.
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS
        
    resized_img = image.resize((target_width, target_height), resample)
    
    if resized_img.mode != "RGBA":
        resized_img = resized_img.convert("RGBA")

    width, height = resized_img.size
    pixels = list(resized_img.getdata())

    lines = []
    for y in range(0, height, 2):
        line_chars = []
        for x in range(width):
            top_idx = y * width + x
            bottom_idx = (y + 1) * width + x

            r1, g1, b1, a1 = pixels[top_idx]
            
            if bottom_idx < len(pixels):
                r2, g2, b2, a2 = pixels[bottom_idx]
            else:
                r2, g2, b2, a2 = 0, 0, 0, 0

            # Alpha threshold (0-255)
            t_solid = a1 >= 128
            b_solid = a2 >= 128

            if not t_solid and not b_solid:
                # Both transparent -> print space with default terminal background
                line_chars.append("\x1b[0m ")
            elif t_solid and not b_solid:
                # Top is solid, bottom is transparent -> upper half block, foreground is top color
                line_chars.append(f"\x1b[0m\x1b[38;2;{r1};{g1};{b1}m▀")
            elif not t_solid and b_solid:
                # Top is transparent, bottom is solid -> lower half block, foreground is bottom color
                line_chars.append(f"\x1b[0m\x1b[38;2;{r2};{g2};{b2}m▄")
            else:
                # Both solid -> upper half block, foreground is top, background is bottom
                line_chars.append(f"\x1b[38;2;{r1};{g1};{b1}m\x1b[48;2;{r2};{g2};{b2}m▀")

        # Reset formatting at the end of each terminal line
        lines.append("".join(line_chars) + "\x1b[0m")

    return "\n".join(lines)
