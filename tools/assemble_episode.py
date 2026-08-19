#!/usr/bin/env python3
"""
Assemble the episode 1 picture track from the shot bank, with no paid services.

Each section loops its shot for exactly as long as the timing map says, then all
sections are concatenated. Because every shot loops seamlessly, a section can be
any length without a visible seam.

    python3 tools/assemble_episode.py --out assets/video/ep01-picture-lock.mp4

The result is SILENT and cut to length - record the vocal over it.
"""
import argparse
import os
import subprocess
import sys
import tempfile
from PIL import Image

FPS = 30
W, H = 1920, 1080
BPM = 112.0
BAR = 4 * 60 / BPM                # 2.143s
SECTION = 8 * BAR                 # 17.143s - one chorus or one verse
HALF = 4 * BAR                    # 8.571s - intro and outro

# (shot name, duration). "still:<path>" renders a slow push-in instead.
TIMELINE = [
    ('closeup-day',              HALF,    'Intro hook - face on screen at frame 1'),
    ('day',                      SECTION, 'Chorus 1'),
    ('rain',                     SECTION, 'Verse 1 - Wipers'),
    ('day',                      SECTION, 'Chorus 2'),
    ('closeup-day',              SECTION, 'Verse 2 - Horn'),
    ('day',                      SECTION, 'Chorus 3'),
    ('park',                     SECTION, 'Verse 3 - Doors'),
    ('day',                      SECTION, 'Chorus 4'),
    ('night',                    SECTION, 'Verse 4 - Lights'),
    ('day',                      SECTION, 'Chorus 5'),
    ('still:assets/generated/bus-family-01.png', SECTION, 'Verse 5 - Friends'),
    ('day',                      SECTION, 'Chorus 6'),
    ('sunset',                   SECTION, 'Verse 6 - Slow down'),
    ('closeup-sunset',           HALF,    'Outro - wave goodbye'),
]

ENC = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
       '-pix_fmt', 'yuv420p', '-r', str(FPS), '-video_track_timescale', '15360']


def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def make_loop(ff, src, nframes, dst):
    """Loop a shot to fill exactly `nframes` frames."""
    subprocess.run([ff, '-y', '-loglevel', 'error', '-stream_loop', '-1', '-i', src,
                    '-frames:v', str(nframes), '-an', *ENC, dst], check=True)


def make_pushin(ff, still, nframes, dst, zoom_to=1.18):
    """Slow Ken Burns push-in on a still, rendered frame by frame into ffmpeg."""
    n = nframes
    im = Image.open(still).convert('RGB')
    # oversample so the widest crop is still >= output size
    base = im.resize((int(W * zoom_to), int(H * zoom_to)), Image.LANCZOS)
    enc = subprocess.Popen(
        [ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', f'{W}x{H}', '-framerate', str(FPS), '-i', '-', '-an', *ENC, dst],
        stdin=subprocess.PIPE)
    for i in range(n):
        t = i / max(1, n - 1)
        z = 1.0 + (zoom_to - 1.0) * t          # linear, slow, no easing wobble
        cw, ch = int(base.width / z), int(base.height / z)
        x, y = (base.width - cw) // 2, (base.height - ch) // 2
        fr = base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit(f'ffmpeg failed writing {dst}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shots', default='assets/video/shots')
    ap.add_argument('--out', default='assets/video/ep01-picture-lock.mp4')
    a = ap.parse_args()

    ff = ffmpeg_exe()
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)

    missing = [n for n, _, _ in TIMELINE
               if not n.startswith('still:')
               and not os.path.exists(os.path.join(a.shots, n + '.mp4'))]
    if missing:
        sys.exit('missing shots: ' + ', '.join(sorted(set(missing))))

    # Frame boundaries come from the CUMULATIVE time, so per-section rounding
    # cannot accumulate into audible drift against the music.
    cum, acc = [], 0.0
    for _, dur, _ in TIMELINE:
        acc += dur
        cum.append(int(round(acc * FPS)))
    starts = [0] + cum[:-1]
    counts = [cum[i] - starts[i] for i in range(len(TIMELINE))]

    tmp = tempfile.mkdtemp(prefix='ep01_')
    parts = []
    for i, (name, _dur, label) in enumerate(TIMELINE):
        dst = os.path.join(tmp, f'{i:02d}.mp4')
        if name.startswith('still:'):
            make_pushin(ff, name.split(':', 1)[1], counts[i], dst)
        else:
            make_loop(ff, os.path.join(a.shots, name + '.mp4'), counts[i], dst)
        secs = starts[i] / FPS
        m, s = divmod(secs, 60)
        print(f'  {int(m)}:{s:05.2f}  {label:34s} <- {name}')
        parts.append(dst)
    t = cum[-1] / FPS

    listfile = os.path.join(tmp, 'list.txt')
    with open(listfile, 'w') as fh:
        for p in parts:
            fh.write(f"file '{p}'\n")
    subprocess.run([ff, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                    '-i', listfile, '-c', 'copy', '-movflags', '+faststart', a.out],
                   check=True)

    for p in parts:
        os.remove(p)
    os.remove(listfile)
    os.rmdir(tmp)
    m, s = divmod(t, 60)
    print(f'wrote {a.out}  ({int(m)}:{s:05.2f}, {cum[-1]} frames, silent)')


if __name__ == '__main__':
    main()
