#!/usr/bin/env python3
"""
Render looping "Benny the Bus" clips with no paid services.
Pillow draws the scene, ffmpeg encodes it. Every clip loops seamlessly.

    python3 tools/render_clip.py --scene day   --seconds 10 --out out.mp4
    python3 tools/render_clip.py --scene night --framing closeup --seconds 8 --out out.mp4
    python3 tools/render_clip.py --scene rain  --vertical --seconds 10 --out out.mp4

Scenes: day, rain, night, sunset, park
Framing: wide (default), closeup

Seamless looping works because every scrolling layer travels a whole number of
tile widths across the clip, and the bounce runs a whole number of cycles. The
last frame therefore matches the first.
"""
import argparse
import math
import os
import random
import subprocess
from PIL import Image, ImageDraw, ImageFilter

# ---- brand palette (sampled from the approved hero render) -------------------
TRUNK = (0x8A, 0x5A, 0x33)

SCENES = {
    'day': dict(
        sky=((0x00, 0xC5, 0xFC), (0xAE, 0xEC, 0xFF)),
        orb=((255, 246, 170), (255, 246, 190), 0.12, 0.13),
        buildings=[(0xFF, 0xC2, 0x4D), (0xFF, 0x8F, 0xA3), (0x7E, 0xA8, 0xFF),
                   (0xFF, 0xB0, 0x6B), (0xC9, 0xA7, 0xFF)],
        window=(255, 255, 255, 205),
        tree=(0x1F, 0x8A, 0x4C),
        road=(0x7E, 0x86, 0x94), road_lt=(0x99, 0xA1, 0xAE), kerb=(0xD8, 0xDD, 0xE4),
        tint=None, stars=False, rain=False, headlights=False,
    ),
    'park': dict(
        sky=((0x2F, 0xD0, 0xFF), (0xC6, 0xF4, 0xFF)),
        orb=((255, 246, 170), (255, 246, 190), 0.82, 0.14),
        buildings=[(0xE8, 0xD9, 0xB0), (0xD9, 0xBF, 0xE8), (0xF0, 0xC9, 0xA8)],
        window=(255, 255, 255, 120),
        tree=(0x17, 0x7A, 0x42),
        road=(0xBE, 0xA1, 0x72),
        road_lt=(0xD2, 0xB8, 0x8C), kerb=(0x8F, 0xD0, 0x7E),
        tint=None, stars=False, rain=False, headlights=False,
    ),
    'rain': dict(
        sky=((0x6E, 0x8B, 0xA8), (0xBF, 0xD2, 0xE0)),
        orb=None,
        buildings=[(0xC9, 0x9E, 0x5E), (0xC7, 0x82, 0x90), (0x74, 0x8C, 0xC0),
                   (0xC2, 0x8E, 0x64), (0xA1, 0x91, 0xC4)],
        window=(255, 250, 220, 190),
        tree=(0x1B, 0x6B, 0x42),
        road=(0x5E, 0x67, 0x74), road_lt=(0x77, 0x81, 0x8E), kerb=(0xA8, 0xB1, 0xBC),
        tint=(40, 60, 90, 46), stars=False, rain=True, headlights=True,
    ),
    'night': dict(
        sky=((0x0B, 0x1E, 0x54), (0x3B, 0x4C, 0x94)),
        orb=((245, 245, 220), (230, 235, 255), 0.83, 0.12),
        buildings=[(0x35, 0x3F, 0x74), (0x46, 0x3C, 0x66),
                   (0x2C, 0x4A, 0x77), (0x4E, 0x3A, 0x5E), (0x32, 0x44, 0x6B)],
        window=(255, 226, 130, 245),
        tree=(0x12, 0x3E, 0x36),
        road=(0x30, 0x36, 0x48), road_lt=(0x43, 0x4A, 0x5E), kerb=(0x55, 0x5E, 0x76),
        tint=(10, 20, 60, 60), stars=True, rain=False, headlights=True,
    ),
    'sunset': dict(
        sky=((0xFF, 0x8C, 0x6B), (0xFF, 0xD9, 0x9E)),
        orb=((255, 214, 120), (255, 190, 120), 0.80, 0.42),
        buildings=[(0xC2, 0x6D, 0x7A), (0xE0, 0x92, 0x5E), (0x8E, 0x6E, 0xA8),
                   (0xD4, 0x7E, 0x6A), (0xA8, 0x74, 0x9E)],
        window=(255, 236, 170, 225),
        tree=(0x2A, 0x5E, 0x4A),
        road=(0x6E, 0x62, 0x66),
        road_lt=(0x8A, 0x7C, 0x80), kerb=(0xC4, 0xAE, 0xA6),
        tint=(255, 150, 90, 34), stars=False, rain=False, headlights=True,
    ),
}


def make_sky(W, H, horizon, sc, rng):
    top, bot = sc['sky']
    sky = Image.new('RGB', (W, H), top)
    d = ImageDraw.Draw(sky)
    for y in range(horizon):
        t = y / max(1, horizon - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    sky = sky.convert('RGBA')

    if sc['stars']:
        st = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        for _ in range(150):
            x = rng.randrange(W)
            y = rng.randrange(int(horizon * 0.8))
            r = rng.choice([1, 1, 1, 2, 2, 3])
            a = rng.randint(120, 255)
            sd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 245, a))
        sky = Image.alpha_composite(sky, st)

    if sc['orb']:
        core, halo, fx, fy = sc['orb']
        sx, sy, sr = int(W * fx), int(H * fy), int(H * 0.075)
        for i in range(9, 0, -1):
            ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ov).ellipse(
                [sx - sr - i * 9, sy - sr - i * 9, sx + sr + i * 9, sy + sr + i * 9],
                fill=halo + (int(16 + 10 * (9 - i)),))
            sky = Image.alpha_composite(sky, ov)
        ImageDraw.Draw(sky).ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=core + (255,))
    return sky


def strip(tile_w, H, painter, screen_w):
    """Build a horizontally tiling RGBA strip wide enough to crop a screen from."""
    n = math.ceil((screen_w + tile_w) / tile_w)
    s = Image.new('RGBA', (tile_w * n, H), (0, 0, 0, 0))
    one = Image.new('RGBA', (tile_w, H), (0, 0, 0, 0))
    painter(ImageDraw.Draw(one), tile_w, H)
    for i in range(n):
        s.paste(one, (i * tile_w, 0), one)
    return s


def paint_clouds(d, tw, H, sc):
    if sc['stars']:
        col = (200, 210, 240, 120)
    elif sc['rain']:
        col = (225, 232, 240, 225)
    else:
        col = (255, 255, 255, 240)

    def puff(cx, cy, s):
        for dx, dy, r in ((0, 0, 46), (-38, 10, 32), (40, 8, 35), (-14, -18, 30), (18, -14, 28)):
            d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s,
                       cx + (dx + r) * s, cy + (dy + r) * s], fill=col)
    puff(int(tw * 0.22), int(H * 0.30), 1.0)
    puff(int(tw * 0.68), int(H * 0.16), 0.72)


def paint_buildings(d, tw, H, base, sc):
    pal = sc['buildings']
    for i, (fx, fw, fh) in enumerate([(0.04, 0.30, 0.46), (0.38, 0.24, 0.34), (0.66, 0.28, 0.52)]):
        c = pal[i % len(pal)]
        w = int(tw * fw)
        x = int(tw * fx)
        h = int(base * fh)
        y0 = base - h
        d.rounded_rectangle([x, y0, x + w, base], radius=18, fill=c)
        d.rounded_rectangle([x - 6, y0 - 14, x + w + 6, y0 + 16], radius=12,
                            fill=tuple(max(0, v - 28) for v in c))
        cols = max(2, w // 58)
        rows = max(2, h // 74)
        for cx in range(cols):
            for ry in range(rows):
                wx = x + 20 + cx * ((w - 34) // max(1, cols))
                wy = y0 + 40 + ry * ((h - 46) // max(1, rows))
                if wy + 30 < base - 8:
                    d.rounded_rectangle([wx, wy, wx + 26, wy + 30], radius=7, fill=sc['window'])


def paint_trees(d, tw, H, base, sc):
    for fx, s in ((0.16, 1.0), (0.62, 0.78)):
        cx = int(tw * fx)
        r = int(52 * s)
        d.rectangle([cx - int(9 * s), base - int(78 * s), cx + int(9 * s), base], fill=TRUNK)
        for dx, dy, rr in ((0, -78, 1.0), (-30, -58, 0.72), (30, -58, 0.72), (0, -108, 0.66)):
            R = int(r * rr)
            d.ellipse([cx + int(dx * s) - R, base + int(dy * s) - R,
                       cx + int(dx * s) + R, base + int(dy * s) + R], fill=sc['tree'])


def make_rain_tile(tw, th, rng):
    t = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    for _ in range(90):
        x = rng.randrange(tw)
        y = rng.randrange(th)
        ln = rng.randint(18, 34)
        d.line([(x, y), (x - ln // 3, y + ln)], fill=(210, 228, 245, rng.randint(70, 150)), width=2)
    return t


def tile_across(dst, tile, ox, oy, W, H):
    tw, th = tile.size
    x0 = -(ox % tw)
    y0 = -(oy % th)
    for x in range(x0, W, tw):
        for y in range(y0, H, th):
            dst.alpha_composite(tile, (x, y))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scene', default='day', choices=sorted(SCENES))
    ap.add_argument('--framing', default='wide', choices=['wide', 'closeup'])
    ap.add_argument('--vertical', action='store_true')
    ap.add_argument('--seconds', type=int, default=10)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--out', default='assets/video/benny-drive-16x9.mp4')
    ap.add_argument('--sprite', default='assets/sprites/bus-front.png')
    a = ap.parse_args()

    sc = SCENES[a.scene]
    rng = random.Random(7)
    W, H = (1080, 1920) if a.vertical else (1920, 1080)
    N = a.seconds * a.fps
    horizon = int(H * 0.62)
    road_h = H - horizon

    cl_w, bd_w, tr_w = int(W * 0.50), int(W * 0.42), int(W * 0.30)
    dash_w = int(W * 0.16)
    scr = {
        'clouds': strip(cl_w, horizon, lambda d, tw, h: paint_clouds(d, tw, h, sc), W),
        'buildings': strip(bd_w, horizon, lambda d, tw, h: paint_buildings(d, tw, h, horizon, sc), W),
        'trees': strip(tr_w, horizon, lambda d, tw, h: paint_trees(d, tw, h, horizon, sc), W),
        'dashes': strip(dash_w, road_h,
                        lambda d, tw, h: d.rounded_rectangle(
                            [int(tw * 0.10), h // 2 - 7, int(tw * 0.62), h // 2 + 7],
                            radius=7, fill=(255, 255, 255, 235)), W),
    }
    # tiles per loop -> whole number, so the seam never shows
    speeds = {'clouds': cl_w * 1 / N, 'buildings': bd_w * 3 / N,
              'trees': tr_w * 6 / N, 'dashes': dash_w * 14 / N}

    sky = make_sky(W, H, horizon, sc, rng)
    ground = Image.new('RGBA', (W, road_h), sc['road'] + (255,))
    gd = ImageDraw.Draw(ground)
    gd.rectangle([0, 0, W, int(road_h * 0.06)], fill=sc['kerb'] + (255,))
    gd.rectangle([0, int(road_h * 0.06), W, int(road_h * 0.09)], fill=sc['road_lt'] + (255,))

    glow = None
    if sc['headlights']:
        g = Image.new('RGBA', (260, 190), (0, 0, 0, 0))
        gd3 = ImageDraw.Draw(g)
        for r in range(90, 0, -8):
            gd3.ellipse([130 - r, 95 - r * 0.7, 130 + r, 95 + r * 0.7],
                        fill=(255, 236, 170, 10))
        glow = g.filter(ImageFilter.GaussianBlur(14))

    rain_tile = make_rain_tile(240, 240, rng) if sc['rain'] else None
    rain_sx, rain_sy = 240 * 4 / N, 240 * 9 / N

    bus = Image.open(a.sprite).convert('RGBA')
    if a.framing == 'closeup':
        # frame on the face: the sprite is a 3/4 view, so the eyes sit left of centre
        fw = 1.05 if not a.vertical else 1.55
        focal = (0.30, 0.34)
        baseline_f = 0.46
    else:
        fw = 0.42 if not a.vertical else 0.92
        focal = None
        baseline_f = 0.46 if not a.vertical else 0.30
    target_w = int(W * fw)
    bus = bus.resize((target_w, int(bus.height * target_w / bus.width)), Image.LANCZOS)
    baseline = horizon + int(road_h * baseline_f)

    outdir = os.path.dirname(a.out) or '.'
    os.makedirs(outdir, exist_ok=True)
    ff = subprocess.run(['python3', '-c',
                         'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],
                        capture_output=True, text=True).stdout.strip()
    # stream frames straight into ffmpeg - avoids encoding a PNG per frame
    enc = subprocess.Popen(
        [ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', f'{W}x{H}', '-framerate', str(a.fps), '-i', '-',
         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
         '-movflags', '+faststart', a.out], stdin=subprocess.PIPE)

    BOUNCES = 8
    _bus_cache = {}
    for f in range(N):
        fr = sky.copy()
        for name, tw in (('clouds', cl_w), ('buildings', bd_w), ('trees', tr_w)):
            off = int(round(speeds[name] * f)) % tw
            fr.alpha_composite(scr[name].crop((off, 0, off + W, horizon)), (0, 0))
        fr.alpha_composite(ground, (0, horizon))
        off = int(round(speeds['dashes'] * f)) % dash_w
        fr.alpha_composite(scr['dashes'].crop((off, 0, off + W, road_h)), (0, horizon))

        ph = 2 * math.pi * BOUNCES * f / N
        lift = (1 - math.cos(ph)) * 0.5
        dy = -int(round(lift * H * 0.022))
        squash = 1.0 - 0.035 * lift
        bw = int(bus.width * (1 / squash) ** 0.35)
        bh = int(bus.height * squash)
        b = _bus_cache.get((bw, bh))
        if b is None:
            b = bus.resize((bw, bh), Image.LANCZOS)
            _bus_cache[(bw, bh)] = b
        if focal:
            bx = int(W * 0.5 - bw * focal[0])
            by = int(H * 0.46 - bh * focal[1]) + dy
        else:
            bx, by = (W - bw) // 2, baseline - bh + dy

        if not focal:
            sw = int(bw * (0.80 - 0.16 * lift))
            sh = int(bh * 0.10)
            sh_img = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
            ImageDraw.Draw(sh_img).ellipse([0, 0, sw, sh],
                                           fill=(30, 40, 55, int(105 - 42 * lift)))
            fr.alpha_composite(sh_img, ((W - sw) // 2, baseline - sh // 2))

        if glow is not None and not focal:
            for gx, gy in ((bx + int(bw * 0.16), by + int(bh * 0.74)),
                           (bx + int(bw * 0.55), by + int(bh * 0.74))):
                fr.alpha_composite(glow, (gx - glow.width // 2, gy - glow.height // 2))

        fr.alpha_composite(b, (bx, by))

        if rain_tile is not None:
            rl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            tile_across(rl, rain_tile, int(rain_sx * f), int(rain_sy * f), W, H)
            fr.alpha_composite(rl)

        if sc['tint']:
            fr.alpha_composite(Image.new('RGBA', (W, H), sc['tint']))

        enc.stdin.write(fr.convert('RGB').tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit(f'ffmpeg failed for {a.out}')
    print('wrote', a.out)


if __name__ == '__main__':
    main()
