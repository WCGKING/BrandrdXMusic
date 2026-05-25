import os
import random
import aiohttp
import aiofiles
import traceback
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from py_yt import VideosSearch
from BrandrdXMusic import app
import math

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

CANVAS_W, CANVAS_H = 1320, 760

FONT_REGULAR_PATH = "BrandrdXMusic/assets/font2.ttf"
FONT_BOLD_PATH = "BrandrdXMusic/assets/font3.ttf"
DEFAULT_THUMB = "BrandrdXMusic/assets/BrandrdXMusicBots.jpg"


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines[:2]


def random_gradient():
    colors = [
        [(15, 12, 41), (48, 43, 99), (36, 36, 62)],
        [(10, 10, 10), (35, 35, 40), (20, 20, 25)],
        [(26, 26, 46), (56, 56, 86), (40, 40, 60)],
        [(20, 25, 35), (45, 50, 70), (30, 35, 50)],
        [(12, 17, 30), (38, 43, 65), (25, 30, 45)],
        [(18, 18, 28), (48, 48, 68), (32, 32, 48)],
        [(8, 15, 25), (28, 40, 55), (18, 28, 40)],
        [(22, 22, 35), (52, 52, 75), (35, 35, 55)],
        [(14, 20, 28), (44, 50, 68), (28, 35, 48)],
        [(16, 14, 38), (46, 44, 88), (30, 28, 60)],
    ]
    return random.choice(colors)


def apply_gradient(canvas, colors):
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for y in range(CANVAS_H):
        progress = y / CANVAS_H
        
        if progress < 0.4:
            t = progress / 0.4
            r = int(colors[0][0] * (1-t) + colors[1][0] * t)
            g = int(colors[0][1] * (1-t) + colors[1][1] * t)
            b = int(colors[0][2] * (1-t) + colors[1][2] * t)
        else:
            t = (progress - 0.4) / 0.6
            r = int(colors[1][0] * (1-t) + colors[2][0] * t)
            g = int(colors[1][1] * (1-t) + colors[2][1] * t)
            b = int(colors[1][2] * (1-t) + colors[2][2] * t)
        
        draw.line([(0, y), (CANVAS_W, y)], fill=(r, g, b, 255))
    
    return Image.alpha_composite(canvas, overlay)


def random_layout():
    layouts = [
        {
            'art_size': random.randint(420, 520),
            'art_x': random.randint(60, 120),
            'art_shape': random.choice(['circle', 'rounded', 'diamond']),
            'text_align': 'right',
            'accent_style': random.choice(['line', 'dot', 'wave']),
            'show_particles': random.choice([True, False])
        },
        {
            'art_size': random.randint(400, 500),
            'art_x': CANVAS_W - random.randint(520, 620),
            'art_shape': random.choice(['circle', 'rounded', 'square']),
            'text_align': 'left',
            'accent_style': random.choice(['line', 'glow', 'none']),
            'show_particles': random.choice([True, False])
        },
        {
            'art_size': random.randint(380, 480),
            'art_x': random.randint(80, 140),
            'art_shape': random.choice(['circle', 'hexagon', 'rounded']),
            'text_align': 'right',
            'accent_style': random.choice(['dot', 'wave', 'glow']),
            'show_particles': random.choice([True, False])
        }
    ]
    return random.choice(layouts)


def create_shape_mask(size, shape):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    
    if shape == 'circle':
        draw.ellipse([0, 0, size, size], fill=255)
    elif shape == 'rounded':
        radius = random.randint(40, 80)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    elif shape == 'square':
        draw.rectangle([0, 0, size, size], fill=255)
    elif shape == 'diamond':
        points = [(size//2, 0), (size, size//2), (size//2, size), (0, size//2)]
        draw.polygon(points, fill=255)
    elif shape == 'hexagon':
        center = size // 2
        radius = size // 2 - 10
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=255)
    
    return mask


def random_accent_color():
    colors = [
        (88, 166, 255),
        (138, 180, 248),
        (156, 163, 255),
        (200, 200, 220),
        (180, 190, 254),
        (120, 200, 255),
        (165, 177, 255),
        (255, 170, 128),
        (255, 138, 180),
        (148, 226, 213),
    ]
    return random.choice(colors)


def add_particles(draw, accent_color):
    for _ in range(random.randint(15, 30)):
        x = random.randint(0, CANVAS_W)
        y = random.randint(0, CANVAS_H)
        size = random.randint(1, 4)
        alpha = random.randint(40, 120)
        draw.ellipse([x, y, x+size, y+size], fill=(*accent_color, alpha))


def add_accent_elements(draw, layout, accent_color):
    style = layout['accent_style']
    
    if style == 'line':
        y_pos = random.randint(100, 200)
        x_start = random.randint(30, 100)
        length = random.randint(200, 400)
        width = random.randint(2, 4)
        draw.line([(x_start, y_pos), (x_start + length, y_pos)], 
                 fill=(*accent_color, 180), width=width)
    
    elif style == 'dot':
        for _ in range(random.randint(3, 8)):
            x = random.randint(40, CANVAS_W - 40)
            y = random.randint(40, CANVAS_H - 40)
            size = random.randint(4, 10)
            draw.ellipse([x, y, x+size, y+size], fill=(*accent_color, 100))
    
    elif style == 'wave':
        y_start = random.randint(80, 150)
        for x in range(0, CANVAS_W, 3):
            wave_y = y_start + int(math.sin(x / 50) * 20)
            draw.ellipse([x, wave_y, x+2, wave_y+2], fill=(*accent_color, 60))


def add_glow_ring(canvas, x, y, size, color, blur_amount):
    ring_size = size + 30
    ring_img = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(ring_img)
    
    for i in range(5):
        offset = i * 5
        alpha = 150 - (i * 30)
        rdraw.ellipse([offset, offset, ring_size - offset, ring_size - offset],
                     outline=(*color, alpha), width=3)
    
    ring_img = ring_img.filter(ImageFilter.GaussianBlur(blur_amount))
    canvas.paste(ring_img, (x - 15, y - 15), ring_img)


async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    thumb_path = None
    
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "Unknown")
        thumburl = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(thumburl) as resp:
                    if resp.status == 200:
                        thumb_path = CACHE_DIR / f"thumb{videoid}.png"
                        async with aiofiles.open(thumb_path, "wb") as f:
                            await f.write(await resp.read())
        except:
            pass

        if thumb_path and thumb_path.exists():
            base_img = Image.open(thumb_path).convert("RGBA")
        else:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")

    except Exception as e:
        print(f"[gen_thumb Error - Using Default] {e}")
        try:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")
            title = "BrandrdXMusic"
            duration = "Unknown"
            views = "Unknown Views"
            channel = "BrandrdXMusic"
        except:
            traceback.print_exc()
            return None

    try:
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 255))
        
        gradient_colors = random_gradient()
        canvas = apply_gradient(canvas, gradient_colors)
        
        layout = random_layout()
        accent_color = random_accent_color()
        
        if layout['show_particles']:
            draw = ImageDraw.Draw(canvas)
            add_particles(draw, accent_color)
            canvas = canvas.filter(ImageFilter.GaussianBlur(1))
        
        art_size = layout['art_size']
        art_x = layout['art_x']
        art_y = (CANVAS_H - art_size) // 2
        
        mask = create_shape_mask(art_size, layout['art_shape'])
        art = base_img.resize((art_size, art_size), Image.LANCZOS)
        art.putalpha(mask)
        
        if random.choice([True, False]):
            add_glow_ring(canvas, art_x, art_y, art_size, accent_color, random.randint(8, 15))
        
        canvas.paste(art, (art_x, art_y), art)
        
        draw = ImageDraw.Draw(canvas)
        
        add_accent_elements(draw, layout, accent_color)
        
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, random.randint(36, 48))
        brand_x = random.randint(35, 60)
        brand_y = random.randint(25, 45)
        
        shadow_offset = 2
        draw.text((brand_x + shadow_offset, brand_y + shadow_offset), 
                 app.username, fill=(0, 0, 0, 150), font=brand_font)
        draw.text((brand_x, brand_y), app.username, fill=(255, 255, 255, 255), font=brand_font)
        
        brand_bbox = draw.textbbox((brand_x, brand_y), app.username, font=brand_font)
        brand_w = brand_bbox[2] - brand_bbox[0]
        underline_y = brand_bbox[3] + 6
        draw.line([(brand_x, underline_y), (brand_x + brand_w, underline_y)], 
                 fill=(*accent_color, 200), width=3)
        
        if layout['text_align'] == 'right':
            info_x = art_x + art_size + random.randint(60, 100)
            max_text_w = CANVAS_W - info_x - 50
        else:
            info_x = random.randint(50, 100)
            max_text_w = art_x - info_x - 50
        
        np_options = ["NOW PLAYING", "PLAYING NOW", "NOW PLAYING", "PLAYING"]
        np_font = ImageFont.truetype(FONT_BOLD_PATH, random.randint(50, 70))
        np_text = random.choice(np_options)
        np_y = random.randint(120, 160)
        
        np_shadow = 3
        draw.text((info_x + np_shadow, np_y + np_shadow), np_text, 
                 fill=(0, 0, 0, 180), font=np_font)
        draw.text((info_x, np_y), np_text, fill=(*accent_color, 255), font=np_font)
        
        title_font_size = random.randint(36, 48)
        title_font = ImageFont.truetype(FONT_BOLD_PATH, title_font_size)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = np_y + random.randint(70, 100)
        
        title_shadow = 2
        draw.multiline_text((info_x + title_shadow, title_y + title_shadow), title_text, 
                          fill=(0, 0, 0, 160), font=title_font, 
                          spacing=random.randint(8, 15))
        draw.multiline_text((info_x, title_y), title_text, 
                          fill=(255, 255, 255, 255), font=title_font, 
                          spacing=random.randint(8, 15))
        
        meta_font = ImageFont.truetype(FONT_REGULAR_PATH, random.randint(28, 36))
        meta_y = title_y + random.randint(120, 160)
        line_spacing = random.randint(45, 60)
        
        duration_label = duration
        if duration and ":" in duration:
            parts = duration.split(":")
            if len(parts) == 2 and parts[0].isdigit():
                duration_label = f"{parts[0]}m {parts[1]}s"
        
        meta_labels = random.choice([
            ["Views", "Duration", "Channel"],
            ["", "", ""]
        ])
        
        meta_items = [
            f"{meta_labels[0]} {views}" if meta_labels[0] else f"{views}",
            f"{meta_labels[1]} {duration_label}" if meta_labels[1] else f"{duration_label}",
            f"{meta_labels[2]} {channel}" if meta_labels[2] else f"{channel}"
        ]
        
        for idx, meta in enumerate(meta_items):
            y = meta_y + (idx * line_spacing)
            draw.text((info_x + 1, y + 1), meta, fill=(0, 0, 0, 140), font=meta_font)
            draw.text((info_x, y), meta, fill=(220, 220, 230, 255), font=meta_font)
        
        if random.choice([True, False]):
            corner_size = random.randint(30, 50)
            corner_width = random.randint(2, 4)
            corner_color = (*accent_color, 120)
            
            draw.line([(25, 25), (25 + corner_size, 25)], fill=corner_color, width=corner_width)
            draw.line([(25, 25), (25, 25 + corner_size)], fill=corner_color, width=corner_width)
            
            draw.line([(CANVAS_W - 25, 25), (CANVAS_W - 25 - corner_size, 25)], 
                     fill=corner_color, width=corner_width)
            draw.line([(CANVAS_W - 25, 25), (CANVAS_W - 25, 25 + corner_size)], 
                     fill=corner_color, width=corner_width)
        
        out = CACHE_DIR / f"{videoid}_final.png"
        canvas.save(out, quality=95, optimize=True)

        if thumb_path and thumb_path.exists():
            try:
                os.remove(thumb_path)
            except:
                pass

        return str(out)

    except Exception as e:
        print(f"[get_thumb Processing Error] {e}")
        traceback.print_exc()
        return None
