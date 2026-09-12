import os
from PIL import Image
import math

def create_walk_frames(filename):
    img = Image.open(filename).convert("RGBA")
    w, h = img.size
    
    frame1 = Image.new("RGBA", (w, h), (0,0,0,0))
    frame2 = Image.new("RGBA", (w, h), (0,0,0,0))
    
    pixels = img.load()
    p1 = frame1.load()
    p2 = frame2.load()
    
    for y in range(h):
        for x in range(w):
            if pixels[x, y][3] > 0: # If not transparent
                if y > h * 0.4:
                    factor = (y - h * 0.4) / (h * 0.6)
                    # Increased amplitude massively from 20 to 180 so it's highly visible at 80x80 scale
                    shift = math.sin(x / w * math.pi * 4) * (180 * factor)
                    
                    new_x1 = int(x + shift)
                    new_x2 = int(x - shift)
                    
                    if 0 <= new_x1 < w:
                        p1[new_x1, y] = pixels[x, y]
                    if 0 <= new_x2 < w:
                        p2[new_x2, y] = pixels[x, y]
                else:
                    p1[x, y] = pixels[x, y]
                    p2[x, y] = pixels[x, y]
                    
    name, ext = os.path.splitext(filename)
    frame1.save(f"{name}_walk1{ext}")
    frame2.save(f"{name}_walk2{ext}")
    print(f"Created highly visible walk frames for {filename}")

create_walk_frames("assets/giraffe.png")
create_walk_frames("assets/cheetah.png")
