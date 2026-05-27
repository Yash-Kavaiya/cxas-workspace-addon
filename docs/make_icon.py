
import struct, zlib, math

def make_png(width, height, pixels):
    def pack_png_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    raw_rows = b''
    for y in range(height):
        row = b'\x00'  # filter type None
        for x in range(width):
            r, g, b, a = pixels[y][x]
            row += bytes([r, g, b, a])
        raw_rows += row

    compressed = zlib.compress(raw_rows, 9)
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)

    return (b'\x89PNG\r\n\x1a\n'
            + pack_png_chunk(b'IHDR', ihdr)
            + pack_png_chunk(b'IDAT', compressed)
            + pack_png_chunk(b'IEND', b''))

W, H = 128, 128
pixels = [[(0,0,0,0)]*W for _ in range(H)]

def lerp(a, b, t): return int(a + (b-a)*t)

def set_pixel(x, y, r, g, b, a=255):
    if 0 <= x < W and 0 <= y < H:
        pixels[y][x] = (r, g, b, a)

def fill_circle(cx, cy, radius, r, g, b, a=255):
    for y in range(max(0,cy-radius-1), min(H,cy+radius+2)):
        for x in range(max(0,cx-radius-1), min(W,cx+radius+2)):
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            if dist <= radius:
                pixels[y][x] = (r, g, b, a)
            elif dist <= radius + 1.2:
                aa = 1.0 - (dist - radius) / 1.2
                pr, pg, pb, pa = pixels[y][x]
                pixels[y][x] = (lerp(pr,r,aa), lerp(pg,g,aa), lerp(pb,b,aa), min(255, pa + int(a*aa)))

def fill_rect(x1, y1, x2, y2, r, g, b, a=255):
    for y in range(max(0,y1), min(H,y2)):
        for x in range(max(0,x1), min(W,x2)):
            pixels[y][x] = (r, g, b, a)

def rounded_rect(x1, y1, x2, y2, rad, r, g, b, a=255):
    fill_rect(x1+rad, y1, x2-rad, y2, r, g, b, a)
    fill_rect(x1, y1+rad, x2, y2-rad, r, g, b, a)
    for cx, cy in [(x1+rad, y1+rad), (x2-rad, y1+rad), (x1+rad, y2-rad), (x2-rad, y2-rad)]:
        fill_circle(cx, cy, rad, r, g, b, a)

# Background: dark navy rounded square
BG = (26, 31, 46)
rounded_rect(0, 0, W, H, 20, *BG)

# White rounded rect (speech bubble body)
rounded_rect(18, 22, 110, 82, 12, 240, 240, 245)

# Speech bubble tail (triangle pointing down-left)
tail = [(32,82),(22,98),(50,82)]
for y in range(82, 98):
    t = (y-82)/16
    x_left = int(32 - 10*t)
    x_right = int(50 - 18*t)
    fill_rect(x_left, y, x_right, y+1, 240, 240, 245)

# Robot face circle
fill_circle(64, 52, 22, 30, 40, 60)

# Eyes — Google colors
fill_circle(55, 46, 5, 66, 133, 244)   # Blue left eye
fill_circle(73, 46, 5, 52, 168, 83)    # Green right eye

# Smile arc (approximate with rects)
smile_pts = [(52,60),(56,63),(60,65),(64,66),(68,65),(72,63),(76,60)]
for i, (x, y) in enumerate(smile_pts[:-1]):
    nx, ny = smile_pts[i+1]
    for s in range(3):
        t = s/3
        px = int(x + (nx-x)*t)
        py = int(y + (ny-y)*t)
        fill_circle(px, py, 2, 251, 188, 4)  # Yellow smile

# Four color dots (Google brand) bottom-right
dot_colors = [(66,133,244),(52,168,83),(251,188,4),(234,67,53)]
dot_positions = [(88,68),(96,68),(88,76),(96,76)]
for (dx,dy),(dr,dg,db) in zip(dot_positions, dot_colors):
    fill_circle(dx, dy, 4, dr, dg, db)

png_data = make_png(W, H, pixels)
with open('/home/yashk/cxas-workspace-addon/docs/icon128.png', 'wb') as f:
    f.write(png_data)
print(f"icon128.png written, {len(png_data)} bytes")
