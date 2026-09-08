# Encodes a curated set of source reels to lightweight web MP4 + poster frames,
# and writes data/videos.js (window.LP_VIDEOS) for the gallery's "Відео" filter.
import os, json, subprocess
from PIL import Image
import imageio_ffmpeg

ROOT = r"C:/Users/Eigenmethod/Desktop/LittlePAW"
SRC = os.path.join(ROOT, "littlepaw_by_hanna")
VID_DIR = os.path.join(ROOT, "assets", "video")
DATA = os.path.join(ROOT, "data")
FF = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs(VID_DIR, exist_ok=True)

# (source number, species, poster timestamp seconds)
CURATED = [
    ("002", "dog", 1.0),
    ("209", "dog", 1.5),
    ("246", "dog", 1.0),
    ("269", "dog", 1.0),
    ("270", "dog", 1.0),
    ("289", "dog", 1.0),
    ("803", "dog", 1.0),
    ("230", "dog", 1.0),
    ("265", "dog", 1.0),
    ("809", "cat", 1.2),
    ("030", "cat", 1.0),
]

items = []
for num, sp, t in CURATED:
    src = os.path.join(SRC, f"{num}.mp4")
    if not os.path.exists(src):
        print(f"! skip {num}: source mp4 not found")
        continue
    mp4 = os.path.join(VID_DIR, f"v-{num}.mp4")
    poster = os.path.join(VID_DIR, f"v-{num}.jpg")
    # encode: cap height 720, H.264, faststart, quiet AAC audio (skip if already done)
    if not os.path.exists(mp4):
        subprocess.run([FF, "-y", "-i", src,
                        "-vf", "scale=-2:'min(720,ih)'",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
                        "-movflags", "+faststart", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "96k", mp4], capture_output=True)
    # poster frame (fall back to first frame if timestamp is past the clip end)
    subprocess.run([FF, "-y", "-ss", str(t), "-i", src, "-frames:v", "1",
                    "-vf", "scale=-2:'min(720,ih)'", poster], capture_output=True)
    if not os.path.exists(poster):
        subprocess.run([FF, "-y", "-i", src, "-frames:v", "1",
                        "-vf", "scale=-2:'min(720,ih)'", poster], capture_output=True)
    im = Image.open(poster)
    items.append({
        "id": f"v{num}",
        "video": f"assets/video/v-{num}.mp4",
        "src": f"assets/video/v-{num}.jpg",
        "species": sp, "kind": "video", "breed": "", "service": "",
        "w": im.width, "h": im.height,
    })
    sz = os.path.getsize(mp4) / 1024
    print(f"v-{num}.mp4  {im.width}x{im.height}  {sz:.0f} KB")

payload = {"items": items}
with open(os.path.join(DATA, "videos.js"), "w", encoding="utf-8") as f:
    f.write("window.LP_VIDEOS = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n")
total = sum(os.path.getsize(os.path.join(VID_DIR, f"v-{n}.mp4")) for n, _, _ in CURATED) / 1048576
print(f"\nvideos.js: {len(items)} clips, {total:.1f} MB total")
