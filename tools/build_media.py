# Copies curated source images into the project as optimized WebP,
# and writes data/gallery.json for the gallery section.
import os, json
from PIL import Image, ImageOps

ROOT = r"C:/Users/Eigenmethod/Desktop/LittlePAW"
SRC  = os.path.join(ROOT, "littlepaw_by_hanna")
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ROOT, "data")
MAXW = 1600
Q = 82

def save_webp(src_num, out_rel, maxw=MAXW, q=Q):
    src = os.path.join(SRC, f"{src_num}.jpg")
    out = os.path.join(ASSETS, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(out, "WEBP", quality=q, method=6)
    return out, im.size

# --- brand + people + interior ---
singles = {
    "people/anna-1.webp": "382",
    "people/anna-2.webp": "486",
    "people/anna-3.webp": "735",
    "interior/hotel-1.webp": "248",
    "interior/hotel-2.webp": "249",
    "interior/hotel-3.webp": "251",
    "interior/hotel-4.webp": "793",
    "interior/hotel-5.webp": "794",
    "interior/hotel-6.webp": "797",
}
for rel, num in singles.items():
    _, sz = save_webp(num, rel)
    print("saved", rel, sz)

# --- gallery ---
# (num, species, kind, breed_label, service)
portraits = [
    ("158","dog","portrait","Шпіц","hygiene"),
    ("159","dog","portrait","Шпіц","hygiene"),
    ("642","dog","portrait","Шпіц","hygiene"),
    ("696","dog","portrait","Шпіц","hygiene"),
    ("698","dog","portrait","Шпіц","hygiene"),
    ("719","dog","portrait","Шпіц","haircut"),
    ("176","dog","portrait","Шпіц","haircut"),
    ("713","dog","portrait","Шпіц","haircut"),
    ("716","dog","portrait","Шпіц","haircut"),
    ("224","dog","portrait","Пудель","haircut"),
    ("226","dog","portrait","Пудель","haircut"),
    ("668","dog","portrait","Пудель","haircut"),
    ("763","dog","portrait","Пудель","haircut"),
    ("130","dog","portrait","Пудель","haircut"),
    ("133","dog","portrait","Мальтезе","haircut"),
    ("456","dog","portrait","Бішон","haircut"),
    ("458","dog","portrait","Бішон","haircut"),
    ("673","dog","portrait","Мальтезе","haircut"),
    ("675","dog","portrait","Мальтезе","haircut"),
    ("272","dog","portrait","Ши-тцу","haircut"),
    ("810","dog","portrait","Ши-тцу","haircut"),
    ("723","dog","portrait","Ши-тцу","haircut"),
    ("038","dog","portrait","Йорк","haircut"),
    ("331","dog","portrait","Йорк","haircut"),
    ("424","dog","portrait","Йорк","haircut"),
    ("574","dog","portrait","Йорк","haircut"),
    ("139","dog","portrait","Кокер","haircut"),
    ("677","dog","portrait","Кокер","haircut"),
    ("080","dog","portrait","Кавалер","hygiene"),
    ("618","dog","portrait","Кавалер","haircut"),
    ("065","dog","portrait","Чихуахуа","hygiene"),
    ("603","dog","portrait","Чихуахуа","hygiene"),
    ("221","dog","portrait","Аусі","hygiene"),
]
beforeafter = [
    ("292","dog"),("293","dog"),("294","dog"),("295","dog"),("296","dog"),
    ("297","dog"),("298","dog"),("299","dog"),("300","dog"),
    ("364","dog"),("365","dog"),("366","dog"),("367","dog"),("368","dog"),("369","dog"),
    ("447","dog"),("448","dog"),("449","dog"),("450","dog"),("451","dog"),
    ("452","dog"),("453","dog"),("454","dog"),("455","dog"),
]
hotel_g = [("249","dog"),("250","dog"),("251","dog"),("252","dog"),
           ("254","dog"),("791","dog"),("793","dog"),("794","dog"),
           ("795","dog"),("796","dog")]

items = []
def add(num, species, kind, breed, service):
    rel = f"gallery/g-{num}.webp"
    _, sz = save_webp(num, rel)
    items.append({
        "id": f"g{num}", "src": f"assets/{rel}",
        "species": species, "kind": kind, "breed": breed, "service": service,
        "w": sz[0], "h": sz[1],
    })

for num, sp, kind, breed, svc in portraits:
    add(num, sp, kind, breed, svc)
for num, sp in beforeafter:
    add(num, sp, "beforeafter", "", "haircut")
for num, sp in hotel_g:
    add(num, sp, "hotel", "", "hotel")

# --- cats: grab frames from grooming videos + one cropped photo ---
import subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

def add_cat_video(vid_num, t):
    src = os.path.join(SRC, f"{vid_num}.mp4")
    rel = f"gallery/cat-{vid_num}.webp"
    out = os.path.join(ASSETS, rel)
    tmp = out + ".png"
    subprocess.run([FF, "-y", "-ss", str(t), "-i", src, "-frames:v", "1", tmp],
                   capture_output=True)
    im = Image.open(tmp).convert("RGB")
    im.thumbnail((1300, 1300), Image.LANCZOS)  # cap longer side
    im.save(out, "WEBP", quality=Q, method=6)
    os.remove(tmp)
    items.append({"id": f"cat{vid_num}", "src": f"assets/{rel}",
                  "species": "cat", "kind": "portrait", "breed": "Котик", "service": "cats",
                  "w": im.width, "h": im.height})

def add_cat_photo(num, top, bottom):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f"{num}.jpg"))).convert("RGB")
    w, h = im.size
    im = im.crop((0, int(h*top), w, int(h*bottom)))
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height*MAXW/im.width)), Image.LANCZOS)
    rel = f"gallery/cat-{num}.webp"
    im.save(os.path.join(ASSETS, rel), "WEBP", quality=Q, method=6)
    items.append({"id": f"cat{num}", "src": f"assets/{rel}",
                  "species": "cat", "kind": "portrait", "breed": "Котик", "service": "cats",
                  "w": im.width, "h": im.height})

for vid, t in [("030", 1.0), ("809", 1.2), ("071", 0.6)]:
    add_cat_video(vid, t)
add_cat_photo("492", 0.0, 0.60)  # tabby in carrier, drop bottom text card

os.makedirs(DATA, exist_ok=True)
payload = {"items": items}
with open(os.path.join(DATA, "gallery.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)
# Also emit a JS global so the page works without fetch() (file:// friendly)
with open(os.path.join(DATA, "gallery.js"), "w", encoding="utf-8") as f:
    f.write("window.LP_GALLERY = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n")
print(f"\ngallery.json + gallery.js: {len(items)} items")
