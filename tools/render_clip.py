#!/usr/bin/env python3
"""
Render a looping "Benny drives through town" clip with no paid services.
Pillow draws the scene, ffmpeg encodes it. Everything loops seamlessly.

Usage:  python3 tools/render_clip.py [--vertical] [--seconds N] [--out PATH]
"""
import argparse, math, os, subprocess, sys
from PIL import Image, ImageDraw

# ---- brand palette (sampled from the approved hero render) -------------------
GREEN   = (0x43, 0xC4, 0x55)
YELLOW  = (0xFF, 0xF0, 0x91)
CORAL   = (0xFF, 0x85, 0x4F)
PURPLE  = (0x5A, 0x2A, 0x8F)
SKY_TOP = (0x00, 0xC5, 0xFC)
SKY_BOT = (0xAE, 0xEC, 0xFF)
ROAD    = (0x7E, 0x86, 0x94)
ROAD_LT = (0x99, 0xA1, 0xAE)
KERB    = (0xD8, 0xDD, 0xE4)
TREE    = (0x1F, 0x8A, 0x4C)
TRUNK   = (0x8A, 0x5A, 0x33)
# buildings deliberately avoid green so the bus separates from them
BUILDINGS = [(0xFF, 0xC2, 0x4D), (0xFF, 0x8F, 0xA3), (0x7E, 0xA8, 0xFF),
             (0xFF, 0xB0, 0x6B), (0xC9, 0xA7, 0xFF)]


def rr(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def make_sky(W, H, horizon):
    sky = Image.new('RGB', (W, H), SKY_TOP)
    d = ImageDraw.Draw(sky)
    for y in range(horizon):
        t = y / max(1, horizon - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * t) for i in range(3)))
    # sun, soft halo
    sx, sy, sr = int(W * 0.12), int(H * 0.13), int(H * 0.075)
    for i in range(9, 0, -1):
        a = int(16 + 10 * (9 - i))
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([sx - sr - i * 9, sy - sr - i * 9,
                                    sx + sr + i * 9, sy + sr + i * 9],
                                   fill=(255, 246, 190, a))
        sky = Image.alpha_composite(sky.convert('RGBA'), ov).convert('RGB')
    ImageDraw.Draw(sky).ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 246, 170))
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


def paint_clouds(d, tw, H):
    def puff(cx, cy, s):
        for dx, dy, r in ((0, 0, 46), (-38, 10, 32), (40, 8, 35), (-14, -18, 30), (18, -14, 28)):
            d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s,
                       cx + (dx + r) * s, cy + (dy + r) * s], fill=(255, 255, 255, 240))
    puff(int(tw * 0.22), int(H * 0.30), 1.0)
    puff(int(tw * 0.68), int(H * 0.16), 0.72)


def paint_buildings(d, tw, H, base):
    xs = [(0.04, 0.30, 0.46), (0.38, 0.24, 0.34), (0.66, 0.28, 0.52)]
    for i, (fx, fw, fh) in enumerate(xs):
        c = BUILDINGS[i % len(BUILDINGS)]
        w = int(tw * fw); x = int(tw * fx); h = int(base * fh)
        y0 = base - h
        rr(d, [x, y0, x + w, base], 18, c)
        rr(d, [x - 6, y0 - 14, x + w + 6, y0 + 16], 12,
           tuple(max(0, v - 28) for v in c))
        cols = max(2, w // 58); rows = max(2, h // 74)
        for cx in range(cols):
            for ry in range(rows):
                wx = x + 20 + cx * ((w - 34) // max(1, cols))
                wy = y0 + 40 + ry * ((h - 46) // max(1, rows))
                if wy + 30 < base - 8:
                    rr(d, [wx, wy, wx + 26, wy + 30], 7, (255, 255, 255, 205))


def paint_trees(d, tw, H, base):
    for fx, s in ((0.16, 1.0), (0.62, 0.78)):
        cx = int(tw * fx); r = int(52 * s)
        d.rectangle([cx - int(9 * s), base - int(78 * s), cx + int(9 * s), base], fill=TRUNK)
        for dx, dy, rr_ in ((0, -78, 1.0), (-30, -58, 0.72), (30, -58, 0.72), (0, -108, 0.66)):
            R = int(r * rr_)
            d.ellipse([cx + int(dx * s) - R, base + int(dy * s) - R,
                       cx + int(dx * s) + R, base + int(dy * s) + R], fill=TREE)


def paint_dashes(d, tw, H):
    d.rounded_rectangle([int(tw * 0.10), H // 2 - 7, int(tw * 0.62), H // 2 + 7], radius=7,
                        fill=(255, 255, 255, 235))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vertical', action='store_true')
    ap.add_argument('--seconds', type=int, default=10)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--out', default='assets/video/benny-drive-16x9.mp4')
    ap.add_argument('--sprite', default='assets/sprites/bus-front.png')
    a = ap.parse_args()

    W, H = (1080, 1920) if a.vertical else (1920, 1080)
    N = a.seconds * a.fps
    horizon = int(H * 0.62)
    road_h = H - horizon

    # Every scrolling layer must travel a whole number of tiles across the clip,
    # otherwise the loop seam shows. speed = tiles * tile_w / N.
    scr = {}
    cl_w = int(W * 0.50)
    scr['clouds'] = strip(cl_w, horizon, paint_clouds, W)
    bd_w = int(W * 0.42)
    scr['buildings'] = strip(bd_w, horizon, lambda d, tw, h: paint_buildings(d, tw, h, horizon), W)
    tr_w = int(W * 0.30)
    scr['trees'] = strip(tr_w, horizon, lambda d, tw, h: paint_trees(d, tw, h, horizon), W)
    dash_w = int(W * 0.16)
    scr['dashes'] = strip(dash_w, road_h, paint_dashes, W)

    speeds = {'clouds': cl_w * 1 / N, 'buildings': bd_w * 3 / N,
              'trees': tr_w * 6 / N, 'dashes': dash_w * 14 / N}

    sky = make_sky(W, H, horizon)
    ground = Image.new('RGBA', (W, road_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ground)
    gd.rectangle([0, 0, W, road_h], fill=ROAD + (255,))
    gd.rectangle([0, 0, W, int(road_h * 0.06)], fill=KERB + (255,))
    gd.rectangle([0, int(road_h * 0.06), W, int(road_h * 0.09)], fill=ROAD_LT + (255,))

    bus = Image.open(a.sprite).convert('RGBA')
    target_w = int(W * (0.42 if not a.vertical else 0.92))
    bus = bus.resize((target_w, int(bus.height * target_w / bus.width)), Image.LANCZOS)

    outdir = os.path.dirname(a.out) or '.'
    os.makedirs(outdir, exist_ok=True)
    frames_dir = os.path.join(outdir, '_frames')
    os.makedirs(frames_dir, exist_ok=True)

    BOUNCES = 8           # whole cycles across the loop -> seamless
    baseline = horizon + int(road_h * (0.46 if not a.vertical else 0.30))

    for f in range(N):
        fr = sky.copy().convert('RGBA')
        for name, tw in (('clouds', cl_w), ('buildings', bd_w), ('trees', tr_w)):
            off = int(round(speeds[name] * f)) % tw
            fr.alpha_composite(scr[name].crop((off, 0, off + W, horizon)), (0, 0))
        fr.alpha_composite(ground, (0, horizon))
        off = int(round(speeds['dashes'] * f)) % dash_w
        fr.alpha_composite(scr['dashes'].crop((off, 0, off + W, road_h)), (0, horizon))

        ph = 2 * math.pi * BOUNCES * f / N
        lift = (1 - math.cos(ph)) * 0.5            # 0..1
        dy = -int(round(lift * H * 0.022))
        squash = 1.0 - 0.035 * lift                # stretch a little at the top
        bw = int(bus.width * (1 / squash) ** 0.35)
        bh = int(bus.height * squash)
        b = bus.resize((bw, bh), Image.LANCZOS)

        # contact shadow shrinks as the bus lifts
        sw = int(bw * (0.80 - 0.16 * lift)); sh = int(bh * 0.10)
        sh_img = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        ImageDraw.Draw(sh_img).ellipse([0, 0, sw, sh],
                                       fill=(30, 40, 55, int(105 - 42 * lift)))
        fr.alpha_composite(sh_img, ((W - sw) // 2, baseline - sh // 2))
        fr.alpha_composite(b, ((W - bw) // 2, baseline - bh + dy))

        fr.convert('RGB').save(os.path.join(frames_dir, f'f{f:05d}.png'))

    ff = subprocess.run(['python3', '-c',
                         'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],
                        capture_output=True, text=True).stdout.strip()
    subprocess.run([ff, '-y', '-loglevel', 'error', '-framerate', str(a.fps),
                    '-i', os.path.join(frames_dir, 'f%05d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
                    '-movflags', '+faststart', a.out], check=True)
    for fn in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, fn))
    os.rmdir(frames_dir)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
