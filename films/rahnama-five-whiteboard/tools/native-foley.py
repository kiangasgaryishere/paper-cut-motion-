"""Lemo Opuscar Whiteboard native foley functions (MIT); no demo story/music. Source: lemomo-ai/lemo-opuscar/styles/whiteboard/demo/mix.py."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from core.audio.sfx import SR,bp,lp
rng=np.random.default_rng(11)
tt=lambda d:np.arange(int(d*SR))/SR
def dec(d,tau):return np.exp(-tt(d)/tau)
_band = {}
def band(n, lo, hi):                                      # cached long filtered noise, sliced randomly
    k = (lo, hi)
    if k not in _band: _band[k] = bp(rng.standard_normal(SR * 8), lo, hi, 2).astype(np.float32)
    b = _band[k]; i = int(rng.integers(0, len(b) - n - 1)); return b[i:i + n]
def marker(dur, length, kind, pen, z=1.):
    d = max(.03, dur); n = int(d * SR); u = np.linspace(0, 1, n)
    v = 1 - .8 * np.cos(2 * np.pi * u)                    # hand speed (engine's prog derivative)
    if kind == 'dash': v = np.ones(n) * 1.2
    a = (v / 1.8) ** .8 * np.minimum(1, u * d / .006) * np.minimum(1, (1 - u) * d / .012)
    br = {'black': 1.0, 'orange': 1.12, 'blue': .92}.get(pen, 1.)
    hiss = band(n, 2200 * br, 7500 * br) * (.55 + .45 * v / 1.8)       # felt on gloss
    body = band(n, 500 * br, 1500 * br) * .45
    grain = (rng.random(n) < .004 * (1 + v)) * rng.standard_normal(n) * .8   # tiny stick-slip ticks
    x = (hiss + body + bp(grain, 1500, 6000)) * a
    if kind != 'dash' and length > 140 and rng.random() < .28:          # the dry-erase squeak
        s0 = rng.uniform(.15, .55) * d; sd = min(d - s0, rng.uniform(.06, .16))
        if sd > .03:
            m = int(sd * SR); ts = np.arange(m) / SR; f0 = rng.uniform(1500, 2600) * br
            f = f0 * (1 + .03 * np.sin(2 * np.pi * rng.uniform(7, 13) * ts) + .05 * rng.standard_normal() * ts / sd)
            sq = np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
            sq *= np.sin(np.pi * ts / sd) ** 1.5 * .35
            i0 = int(s0 * SR); x[i0:i0 + m] += sq[:len(x) - i0]
    x[:int(.004 * SR)] += bp(rng.standard_normal(int(.004 * SR)), 2500, 6500) * np.linspace(1, 0, int(.004 * SR)) * 1.4   # nib lands
    return x * .32 * min(1.3, z ** .5)
def tap(z=1.):
    n = int(.03 * SR); x = bp(rng.standard_normal(n), 1800, 6000) * dec(.03, .004) * 1.2
    return x * .3 * min(1.3, z ** .5)

# ───────── other foley
def ring(fs, taus, amps, d):
    x = np.zeros(int(d * SR)); t = tt(d)
    for f, ta, am in zip(fs, taus, amps): x += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / ta) * am
    return x
def magnet(big=0):
    d = .5; x = np.zeros(int(d * SR))
    c = bp(rng.standard_normal(int(.005 * SR)), 2000, 9000) * np.linspace(1, 0, int(.005 * SR)) * 1.5; x[:len(c)] += c
    x += ring([830, 1370, 2210, 3120], [.07, .05, .035, .02], [.35, .25, .15, .08], d)   # steel face of the board
    x += ring([140 + 30 * big], [.09 + .06 * big], [.9 + .6 * big], d) * .9          # board body thump
    return x * (.55 + .35 * big)
def magnet_off():
    d = .35; x = lp(rng.standard_normal(int(d * SR)), 1800) * np.minimum(1, tt(d) / .15) * dec(d, .1) * .25
    x[:int(.004 * SR)] += bp(rng.standard_normal(int(.004 * SR)), 2500, 8000) * .8
    return x
def cap_pop():
    d = .25; t = tt(d); x = np.zeros(len(t))
    sl = bp(rng.standard_normal(int(.07 * SR)), 1200, 5000) * np.linspace(.2, 1, int(.07 * SR)) * .35; x[:len(sl)] += sl   # cap sliding off
    i = int(.07 * SR); p = ring([1750, 3400], [.03, .012], [.8, .3], d - .07); x[i:i + len(p)] += p
    x[i:i + 60] += rng.standard_normal(60) * .9
    return x * .6
def cap_on():
    d = .2; x = np.zeros(int(d * SR))
    for k, o in enumerate([0, .045]):
        i = int(o * SR); c = bp(rng.standard_normal(int(.006 * SR)), 2500, 9000) * np.linspace(1, 0, int(.006 * SR)); x[i:i + len(c)] += c * (1 - .4 * k)
        r = ring([2600], [.015], [.4], .06); x[i:i + len(r)] += r
    return x * .7
def eraser(d, rewind=False):
    n = int(d * SR); t = tt(d)
    base = bp(rng.standard_normal(n), 250, 2600) * .6 + bp(rng.standard_normal(n), 2500, 6000) * .15
    if rewind: mod = .75 + .25 * np.sin(2 * np.pi * 9 * t)
    else: mod = .45 + .55 * np.abs(np.sin(np.pi * t / d * 7))            # zig-zag strokes
    a = np.minimum(1, t / .04) * np.minimum(1, (d - t) / .06)
    return base * mod * a * .5
def plop():
    d = .9; t = tt(d); x = np.zeros(len(t))
    f = 900 * np.exp(-t / .05) + 240; x += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .07) * .8
    x += bp(rng.standard_normal(len(t)), 900, 6000) * np.exp(-t / .12) * .35
    for k in range(5):                                   # droplets
        o = int(rng.uniform(.12, .6) * SR); dd = .05; fb = rng.uniform(1400, 3200)
        b = np.sin(2 * np.pi * np.cumsum(fb * (1 + tt(dd) * 8)) / SR) * dec(dd, .015) * .25; x[o:o + len(b)] += b[:len(x) - o]
    return x * .8
def tray_clack(v=1.):
    d = .6; x = np.zeros(int(d * SR))
    for k, (o, g) in enumerate([(0, 1), (.075, .45), (.13, .2)]):     # plastic bounces
        i = int(o * SR); c = bp(rng.standard_normal(int(.008 * SR)), 1200, 6000) * np.linspace(1, 0, int(.008 * SR)) * g
        x[i:i + len(c)] += c; r = ring([620, 1180, 2350], [.05, .04, .03], [.4, .3, .15], .2) * g; x[i:i + len(r)] += r
    return x * .7 * v
def thud(v=1.):
    d = .4; x = ring([95, 180], [.08, .05], [1, .4], d) + lp(rng.standard_normal(int(d * SR)), 600) * dec(d, .03) * .5
    return x * .7 * v
def whoosh(d, v=1.):
    n = int(d * SR); t = tt(d); sh = np.sin(np.pi * t / d) ** 2
    x = bp(rng.standard_normal(n), 300, 2400) * sh
    return x * .35 * v
def clock_tick(k):
    d = .25; x = bp(rng.standard_normal(int(.004 * SR)), 3000, 9000) * 1.2
    y = np.zeros(int(d * SR)); y[:len(x)] += x
    y += ring([1250 if k % 2 else 1480, 2900], [.018, .01], [.35, .15], d)
    return y * .22

