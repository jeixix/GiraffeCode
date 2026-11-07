"""
High-resolution Otter & Fish sprite and icon generator for SavannaCode.
Loads from assets/ if present, or procedurally generates and caches the
1024x1024 sprites, swim animation frames, and 72x72 emoji icons.
"""
import os
import math
import pygame
from PIL import Image, ImageDraw


def _draw_polygon_smooth(img, points, fill, outline=None, width=10):
    draw = ImageDraw.Draw(img)
    if fill:
        draw.polygon(points, fill=fill)
    if outline and width > 0:
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            draw.line([p1, p2], fill=outline, width=width)
            r = width // 2
            draw.ellipse((p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r), fill=outline)


def _create_walk_frames_pil(img):
    w, h = img.size
    frame1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    frame2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = img.load()
    p1 = frame1.load()
    p2 = frame2.load()
    for y in range(h):
        for x in range(w):
            if pixels[x, y][3] > 0:
                if y > h * 0.4:
                    factor = (y - h * 0.4) / (h * 0.6)
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
    return frame1, frame2


def _build_otter_pil():
    S = 2048
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outline = (52, 28, 14, 255)       # Deep warm espresso brown outline
    fur_main = (154, 96, 54, 255)     # Warm rich river otter brown
    fur_dark = (116, 68, 36, 255)     # Darker back/far-leg shading
    fur_light = (238, 206, 168, 255)  # Creamy beige belly, throat, and cheeks
    nose_col = (45, 24, 18, 255)
    cheek_blush = (242, 132, 112, 220)
    lw = 24

    # 1. Back legs (darker brown, behind body)
    draw.ellipse((430, 1120, 700, 1380), fill=fur_dark, outline=outline, width=lw)
    draw.ellipse((350, 1250, 560, 1400), fill=fur_dark, outline=outline, width=lw)
    draw.ellipse((1200, 1110, 1490, 1320), fill=fur_dark, outline=outline, width=lw)

    # 2. Long tapered otter tail with rounded tip (sweeping left)
    tail_pts = []
    for t_step in range(36):
        t = t_step / 35.0
        cx = 560 - t * 400
        cy = 1040 - math.sin(t * math.pi * 0.8) * 165 - t * 70
        thickness = math.cos(t * math.pi * 0.48) * 98 + 8
        tail_pts.append((cx, cy - thickness))
    for t_step in range(35, -1, -1):
        t = t_step / 35.0
        cx = 560 - t * 400
        cy = 1040 - math.sin(t * math.pi * 0.8) * 165 - t * 70
        thickness = math.cos(t * math.pi * 0.48) * 98 + 8
        tail_pts.append((cx, cy + thickness))
    _draw_polygon_smooth(img, tail_pts, fill=fur_main, outline=outline, width=lw)

    # 3. Sleek hydrodynamic otter body
    draw.ellipse((460, 810, 1480, 1300), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((450, 910, 650, 1160), fill=fur_main)

    # 4. Creamy belly patch along the underside of the torso
    belly_pts = [
        (650, 1140), (830, 1050), (1090, 1040), (1330, 1075),
        (1420, 975), (1400, 1195), (1160, 1275), (850, 1275), (630, 1220)
    ]
    draw.polygon(belly_pts, fill=fur_light)
    draw.arc((460, 810, 1480, 1300), start=340, end=195, fill=outline, width=lw)

    # 5. Foreground hind leg & webbed paw
    draw.ellipse((550, 1100, 840, 1410), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((480, 1290, 750, 1465), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((575, 1060, 815, 1245), fill=fur_main)
    draw.line([(545, 1415), (600, 1365)], fill=outline, width=14)
    draw.line([(610, 1438), (655, 1385)], fill=outline, width=14)

    # 6. Foreground front leg & webbed paw
    draw.ellipse((1110, 1090, 1400, 1415), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((1230, 1295, 1505, 1455), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((1130, 1040, 1365, 1225), fill=fur_main)
    draw.line([(1440, 1355), (1380, 1370)], fill=outline, width=14)
    draw.line([(1455, 1400), (1390, 1405)], fill=outline, width=14)

    # 7. Neck & Round Otter Head (facing right)
    draw.ellipse((1480, 520, 1650, 690), fill=fur_dark, outline=outline, width=lw)
    draw.ellipse((1520, 560, 1610, 650), fill=fur_light)
    draw.ellipse((1160, 520, 1835, 1110), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((1130, 820, 1460, 1080), fill=fur_main)

    # Creamy muzzle / cheek mask
    draw.ellipse((1345, 775, 1815, 1085), fill=fur_light)
    draw.arc((1160, 520, 1835, 1110), start=220, end=145, fill=outline, width=lw)

    # Near ear
    draw.ellipse((1185, 560, 1370, 745), fill=fur_main, outline=outline, width=lw)
    draw.ellipse((1230, 605, 1330, 705), fill=fur_light, outline=outline, width=12)

    # Rosy cheeks
    draw.ellipse((1390, 860, 1510, 940), fill=cheek_blush)
    draw.ellipse((1715, 850, 1800, 920), fill=cheek_blush)

    # Expressive eyes
    draw.ellipse((1425, 685, 1565, 835), fill=(255, 255, 255, 255), outline=outline, width=16)
    draw.ellipse((1460, 705, 1555, 820), fill=(42, 22, 12, 255))
    draw.ellipse((1475, 720, 1515, 760), fill=(255, 255, 255, 255))
    draw.ellipse((1520, 775, 1542, 797), fill=(255, 255, 255, 255))

    draw.ellipse((1655, 680, 1765, 815), fill=(255, 255, 255, 255), outline=outline, width=16)
    draw.ellipse((1680, 700, 1758, 803), fill=(42, 22, 12, 255))
    draw.ellipse((1692, 713, 1726, 747), fill=(255, 255, 255, 255))

    # Eyebrows
    draw.arc((1420, 630, 1555, 710), start=200, end=330, fill=outline, width=18)
    draw.arc((1650, 630, 1760, 705), start=210, end=335, fill=outline, width=18)

    # Nose
    nose_pts = [(1635, 810), (1755, 805), (1715, 880), (1670, 880)]
    _draw_polygon_smooth(img, nose_pts, fill=nose_col, outline=outline, width=14)
    draw.ellipse((1672, 818, 1718, 840), fill=(115, 85, 75, 255))

    # Smile
    draw.arc((1570, 860, 1695, 950), start=10, end=170, fill=outline, width=16)
    draw.arc((1690, 860, 1790, 945), start=15, end=170, fill=outline, width=16)

    # Whiskers
    whisker_lines = [
        [(1535, 890), (1325, 860)],
        [(1540, 920), (1315, 925)],
        [(1550, 950), (1350, 990)],
        [(1785, 875), (1940, 840)],
        [(1790, 905), (1955, 900)],
        [(1780, 935), (1930, 960)],
    ]
    for p1, p2 in whisker_lines:
        draw.line([p1, p2], fill=outline, width=12)

    return img.resize((1024, 1024), Image.Resampling.LANCZOS)


def _build_fish_pil():
    S = 2048
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outline = (68, 24, 12, 255)
    body_top = (255, 105, 45, 255)
    body_mid = (255, 168, 42, 255)
    body_belly = (255, 232, 140, 255)
    fin_col = (255, 82, 50, 255)
    fin_inner = (255, 210, 70, 255)
    lw = 26

    # Dorsal fin
    dorsal_pts = [(780, 690), (960, 430), (1230, 485), (1280, 690)]
    _draw_polygon_smooth(img, dorsal_pts, fill=fin_col, outline=outline, width=lw)
    draw.line([(950, 640), (1010, 485)], fill=fin_inner, width=18)
    draw.line([(1090, 650), (1145, 510)], fill=fin_inner, width=18)

    # Ventral fin
    pelvic_pts = [(850, 1280), (980, 1510), (1180, 1460), (1160, 1270)]
    _draw_polygon_smooth(img, pelvic_pts, fill=fin_col, outline=outline, width=lw)

    # Tail fin
    tail_pts = [
        (1360, 990), (1820, 580), (1880, 740),
        (1690, 990), (1880, 1240), (1820, 1400),
    ]
    _draw_polygon_smooth(img, tail_pts, fill=fin_col, outline=outline, width=lw)
    draw.polygon([(1450, 990), (1770, 700), (1630, 990), (1770, 1280)], fill=fin_inner)
    _draw_polygon_smooth(img, tail_pts, fill=None, outline=outline, width=lw)

    # Body
    draw.ellipse((320, 620, 1520, 1360), fill=body_mid, outline=outline, width=lw)
    draw.chord((320, 620, 1520, 1360), start=195, end=345, fill=body_top)
    draw.chord((340, 660, 1490, 1350), start=25, end=155, fill=body_belly)
    draw.ellipse((320, 620, 1520, 1360), fill=None, outline=outline, width=lw)

    # Scales & gill
    for sx, sy in [(880, 860), (1040, 860), (1200, 860), (960, 990), (1120, 990), (1040, 1120)]:
        draw.arc((sx, sy, sx + 120, sy + 130), start=270, end=90, fill=outline, width=16)
    draw.arc((590, 760, 790, 1210), start=295, end=65, fill=outline, width=20)

    # Side fin
    pec_pts = [(750, 1020), (1020, 930), (1060, 1140), (820, 1170)]
    _draw_polygon_smooth(img, pec_pts, fill=fin_col, outline=outline, width=22)

    # Eye & smile
    draw.ellipse((460, 770, 640, 950), fill=(255, 255, 255, 255), outline=outline, width=18)
    draw.ellipse((480, 800, 595, 925), fill=(35, 20, 15, 255))
    draw.ellipse((495, 815, 540, 860), fill=(255, 255, 255, 255))
    draw.ellipse((550, 880, 575, 905), fill=(255, 255, 255, 255))
    draw.ellipse((555, 975, 655, 1045), fill=(255, 115, 125, 225))
    draw.arc((345, 950, 535, 1075), start=15, end=145, fill=outline, width=18)

    # Bubbles
    bubble_outline = (25, 95, 145, 255)
    for bx, by, br in [(310, 680, 48), (230, 530, 68), (350, 390, 88)]:
        draw.ellipse((bx - br, by - br, bx + br, by + br), fill=(225, 250, 255, 235), outline=bubble_outline, width=14)
        draw.ellipse((bx - br // 2, by - br // 2, bx - br // 6, by - br // 6), fill=(255, 255, 255, 255))

    return img.resize((1024, 1024), Image.Resampling.LANCZOS)


def _pil_to_surface(pil_img):
    raw = pil_img.tobytes()
    surf = pygame.image.fromstring(raw, pil_img.size, "RGBA")
    try:
        return surf.convert_alpha()
    except Exception:
        return surf


def load_or_generate_otter_assets(assets_dir, load_image_fn):
    """
    Returns dict with keys:
      'otter', 'otter_walk', 'fish', 'emoji_otter', 'emoji_fish'
    Loads from assets_dir if files exist; otherwise generates via PIL,
    attempts to persist to assets_dir, and converts to pygame.Surface.
    """
    result = {}
    otter_s = load_image_fn("otter.png")
    otter_w1 = load_image_fn("otter_walk1.png")
    otter_w2 = load_image_fn("otter_walk2.png")
    fish_s = load_image_fn("fish.png")
    e_otter = load_image_fn("emoji_otter.png")
    e_fish = load_image_fn("emoji_fish.png")

    if otter_s and otter_w1 and otter_w2 and fish_s and e_otter and e_fish:
        result["otter"] = otter_s
        result["otter_walk"] = [otter_w1, otter_w2]
        result["fish"] = fish_s
        result["emoji_otter"] = e_otter
        result["emoji_fish"] = e_fish
        return result

    otter_pil = _build_otter_pil()
    fish_pil = _build_fish_pil()
    w1_pil, w2_pil = _create_walk_frames_pil(otter_pil)
    e_otter_pil = otter_pil.resize((72, 72), Image.Resampling.LANCZOS)
    e_fish_pil = fish_pil.resize((72, 72), Image.Resampling.LANCZOS)

    # Attempt to save to assets_dir if writable
    if assets_dir and os.path.isdir(assets_dir):
        for fname, p_img in [
            ("otter.png", otter_pil),
            ("otter_walk1.png", w1_pil),
            ("otter_walk2.png", w2_pil),
            ("fish.png", fish_pil),
            ("emoji_otter.png", e_otter_pil),
            ("emoji_fish.png", e_fish_pil),
        ]:
            fpath = os.path.join(assets_dir, fname)
            if not os.path.exists(fpath):
                try:
                    p_img.save(fpath)
                except Exception:
                    pass

    result["otter"] = otter_s or _pil_to_surface(otter_pil)
    result["otter_walk"] = [
        otter_w1 or _pil_to_surface(w1_pil),
        otter_w2 or _pil_to_surface(w2_pil),
    ]
    result["fish"] = fish_s or _pil_to_surface(fish_pil)
    result["emoji_otter"] = e_otter or _pil_to_surface(e_otter_pil)
    result["emoji_fish"] = e_fish or _pil_to_surface(e_fish_pil)
    return result
