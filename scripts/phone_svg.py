"""Phone-first SVG helper: 420 px wide portrait diagrams with large text.

Designed so a diagram stays readable when scaled to an iPhone 15 portrait width.
Usage:
    p = P("Title")
    p.box("text", "blue"); p.arrow("label"); p.row([("a","green"),("b","amber")])
    p.save(OUT, "name.svg")
"""
import textwrap
from html import escape
from pathlib import Path

W = 420
PAD = 16
INK, MUTE, BG, BORDER = "#0F172A", "#475569", "#F8FAFC", "#CBD5E1"
COL = {
    "blue": ("#DBEAFE", "#2563EB"), "green": ("#DCFCE7", "#16A34A"),
    "amber": ("#FEF3C7", "#D97706"), "red": ("#FEE2E2", "#DC2626"),
    "purple": ("#EDE9FE", "#7C3AED"), "gray": ("#E2E8F0", "#64748B"),
    "white": ("#FFFFFF", "#94A3B8"), "teal": ("#CCFBF1", "#0D9488"),
}
SANS = "Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, 'Courier New', monospace"


class P:
    def __init__(self, title, subtitle=""):
        self.parts, self.y = [], 0
        self.title = title
        self.t(title, 17, "bold", y_adv=26, start=True)
        if subtitle:
            self.t(subtitle, 12.5, fill=MUTE, y_adv=20)
        self.y += 6

    # ----- primitives -----
    def _text(self, x, y, s, size, weight="normal", fill=INK, anchor="start", mono=False):
        fam = MONO if mono else SANS
        out = (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
               f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">')
        for i, ln in enumerate(s.split("\n")):
            dy = 0 if i == 0 else round(size * 1.35, 1)
            out += f'<tspan x="{x}" dy="{dy}">{escape(ln)}</tspan>'
        return out + "</text>"

    def _wrap(self, s, width_px, size, mono=False):
        cw = size * (0.6 if mono else 0.56)
        n = max(8, int(width_px / cw))
        lines = []
        for seg in s.split("\n"):
            lines += textwrap.wrap(seg, n, break_long_words=True) or [""]
        return lines

    def t(self, s, size=13, weight="normal", fill=INK, y_adv=None, start=False, mono=False, x=PAD):
        lines = self._wrap(s, W - 2 * PAD, size, mono)
        if start:
            self.y = PAD + size
        else:
            self.y += size
        txt = "\n".join(lines)
        self.parts.append(self._text(x, self.y, txt, size, weight, fill, mono=mono))
        self.y += (len(lines) - 1) * size * 1.35 + (y_adv if y_adv is not None else 8)

    # ----- blocks -----
    def box(self, s, color="white", size=13.5, mono=False, weight="normal", sub="", x=PAD, w=None, gap=8):
        w = w or (W - 2 * PAD)
        lines = self._wrap(s, w - 22, size, mono)
        sublines = self._wrap(sub, w - 22, size - 2) if sub else []
        lh = size * 1.35
        h = 18 + len(lines) * lh + (len(sublines) * (size - 2) * 1.35 + 4 if sub else 0)
        f, st = COL[color]
        self.parts.append(f'<rect x="{x}" y="{self.y}" width="{w}" height="{h:.1f}" rx="10" fill="{f}" stroke="{st}" stroke-width="1.8"/>')
        ty = self.y + 9 + size
        self.parts.append(self._text(x + w / 2, ty, "\n".join(lines), size, weight, anchor="middle", mono=mono))
        if sub:
            sy = ty + (len(lines) - 1) * lh + (size - 2) * 1.35 + 2
            self.parts.append(self._text(x + w / 2, sy, "\n".join(sublines), size - 2, fill=MUTE, anchor="middle"))
        self.y += h + gap
        return h

    def row(self, items, size=12.5, mono=False, gap=8):
        n = len(items)
        w = (W - 2 * PAD - (n - 1) * 8) / n
        hs = []
        for lines_src, _ in items:
            hs.append(18 + len(self._wrap(lines_src, w - 14, size, mono)) * size * 1.35)
        h = max(hs)
        for i, (s, color) in enumerate(items):
            x = PAD + i * (w + 8)
            f, st = COL[color]
            lines = self._wrap(s, w - 14, size, mono)
            self.parts.append(f'<rect x="{x:.1f}" y="{self.y}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="{f}" stroke="{st}" stroke-width="1.8"/>')
            self.parts.append(self._text(x + w / 2, self.y + 9 + size, "\n".join(lines), size, anchor="middle", mono=mono))
        self.y += h + gap

    def arrow(self, label="", color="gray", length=22):
        st = COL[color][1]
        x = W / 2
        self.parts.append(f'<line x1="{x}" y1="{self.y - 2}" x2="{x}" y2="{self.y + length - 6}" stroke="{st}" stroke-width="2.2"/>')
        self.parts.append(f'<path d="M{x-6},{self.y + length - 10} L{x},{self.y + length} L{x+6},{self.y + length - 10} z" fill="{st}"/>')
        if label:
            self.parts.append(self._text(x + 12, self.y + length / 2 + 4, label, 12, fill=MUTE, mono=True))
        self.y += length + 4

    def note(self, s, size=12.5, fill=MUTE, mono=False):
        self.t(s, size, fill=fill, mono=mono, y_adv=10)

    def gap(self, n=8):
        self.y += n

    def save(self, out_dir, name):
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        h = self.y + PAD
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h:.0f}" width="{W}" height="{h:.0f}" '
               f'role="img" aria-label="{escape(self.title)}"><title>{escape(self.title)}</title>'
               f'<rect width="{W}" height="{h:.0f}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
               + "".join(self.parts) + "</svg>")
        (out_dir / name).write_text(svg, encoding="utf-8")
        return h
