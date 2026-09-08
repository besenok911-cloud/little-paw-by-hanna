# Builds the transparent brand logo from source card 320 (emblem + "Little Paw by Hanna").
# Flood-fills the flat cream background to transparent so the logo sits on any colour.
import os
from PIL import Image
from collections import deque

ROOT = r"C:/Users/Eigenmethod/Desktop/LittlePAW"
SRC = os.path.join(ROOT, "littlepaw_by_hanna", "320.jpg")
OUT_DIR = os.path.join(ROOT, "assets", "brand")
os.makedirs(OUT_DIR, exist_ok=True)

im = Image.open(SRC).convert("RGB")
w, h = im.size
# emblem + wordmark sit top-centre of the card
crop = im.crop((int(w*0.30), int(h*0.01), int(w*0.72), int(h*0.16))).convert("RGBA")
w, h = crop.size
px = crop.load()

corners = [px[0, 0], px[w-1, 0], px[0, h-1], px[w-1, h-1]]
br = sum(c[0] for c in corners)//4
bg = sum(c[1] for c in corners)//4
bb = sum(c[2] for c in corners)//4
TOL = 42

def near(c):
    return (abs(c[0]-br)+abs(c[1]-bg)+abs(c[2]-bb))/3 < TOL

visited = [[False]*w for _ in range(h)]
dq = deque()
for x in range(w):
    dq.append((x, 0)); dq.append((x, h-1))
for y in range(h):
    dq.append((0, y)); dq.append((w-1, y))
while dq:
    x, y = dq.popleft()
    if x < 0 or y < 0 or x >= w or y >= h or visited[y][x]:
        continue
    visited[y][x] = True
    c = px[x, y]
    if near(c):
        px[x, y] = (c[0], c[1], c[2], 0)
        dq.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

crop = crop.crop(crop.getbbox())
crop.save(os.path.join(OUT_DIR, "logo.png"))
crop.save(os.path.join(OUT_DIR, "logo.webp"), "WEBP", quality=92, method=6)
print("logo built:", crop.size)
