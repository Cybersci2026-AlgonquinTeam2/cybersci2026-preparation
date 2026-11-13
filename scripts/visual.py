"""Visual upgrades shared by the PDF and EPUB builders.

- ASCII box diagrams in code blocks -> real SVG images (never wrap or garble on a phone)
- Bold lead-ins ("Plain English.", "Analogy.", "Lesson.", ...) -> colour-coded callout boxes
- "Check yourself" / "Teach it back" headings -> highlighted study prompts
"""
import base64
import hashlib
from html import escape

from lxml import etree, html as lhtml

BOX_CHARS = set("─│┌┐└┘├┤┬┴┼▶▼◀▲═║╔╗╚╝")

CALLOUTS = {
    "plain english": ("plain", "In plain English"),
    "intuition": ("plain", "Intuition"),
    "analogy": ("analogy", "Analogy"),
    "lesson": ("lesson", "Lesson"),
    "lessons": ("lesson", "Lessons"),
    "key lesson": ("lesson", "Lesson"),
    "expert note": ("expert", "Expert note"),
    "why it works": ("why", "Why it works"),
    "why": ("why", "Why"),
    "teach it back": ("teach", "Teach it back"),
    "failure modes": ("warn", "Failure modes"),
    "pitfall": ("warn", "Pitfall"),
    "pitfalls": ("warn", "Pitfalls"),
    "pitfall in the original": ("warn", "Pitfall"),
    "alternatives": ("alt", "Alternatives"),
    "variations": ("alt", "Variations"),
    "tell-tale": ("plain", "Tell-tale"),
    "reasoning": ("why", "Reasoning"),
    "fix": ("lesson", "Fix"),
    "where else you will see it": ("alt", "Where else you will see it"),
    "mastery check": ("teach", "Mastery check"),
    "triage": ("plain", "Triage"),
    "check yourself": ("teach", "Check yourself"),
}

CSS_CALLOUTS = """
.co { margin: .9em 0; padding: .55em .8em; border-radius: 8px; border-left: 5px solid #64748b;
      background: rgba(127,127,127,.10); }
.co p { margin: .25em 0; }
.co .co-label { display: block; font-size: .72em; font-weight: bold; text-transform: uppercase;
                letter-spacing: .06em; margin-bottom: .2em; }
.co-plain  { border-left-color: #2563eb; background: rgba(37,99,235,.11); }
.co-plain .co-label  { color: #2563eb; }
.co-analogy { border-left-color: #7c3aed; background: rgba(124,58,237,.11); }
.co-analogy .co-label { color: #7c3aed; }
.co-lesson { border-left-color: #16a34a; background: rgba(22,163,74,.12); }
.co-lesson .co-label { color: #16a34a; }
.co-expert { border-left-color: #d97706; background: rgba(217,119,6,.12); }
.co-expert .co-label { color: #d97706; }
.co-why    { border-left-color: #0d9488; background: rgba(13,148,136,.12); }
.co-why .co-label    { color: #0d9488; }
.co-teach  { border-left-color: #db2777; background: rgba(219,39,119,.11); }
.co-teach .co-label  { color: #db2777; }
.co-warn   { border-left-color: #dc2626; background: rgba(220,38,38,.11); }
.co-warn .co-label   { color: #dc2626; }
.co-alt    { border-left-color: #64748b; background: rgba(100,116,139,.12); }
.co-alt .co-label    { color: #64748b; }
h2.teach-h, h3.teach-h { border-bottom-color: #db2777; color: #db2777; }
"""


def ascii_svg(text, font=13):
    lines = text.rstrip("\n").split("\n")
    cw = font * 0.6
    width = int(max(len(l) for l in lines) * cw + 32)
    lh = font * 1.35
    height = int(len(lines) * lh + 28)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
           f'<rect width="{width}" height="{height}" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>']
    for i, l in enumerate(lines):
        y = 18 + font + i * lh
        out.append(f'<text x="16" y="{y:.1f}" xml:space="preserve" font-family="Menlo, Consolas, Courier, monospace" '
                   f'font-size="{font}" fill="#0f172a">{escape(l)}</text>')
    out.append("</svg>")
    return "".join(out)


def is_diagram(text):
    return any(ch in BOX_CHARS for ch in text) and len(text.strip().split("\n")) >= 1


def convert_ascii_blocks(root, emit):
    """emit(svg_text) -> src string for an <img>."""
    for pre in list(root.iter("pre")):
        txt = pre.text_content()
        if not is_diagram(txt):
            continue
        src = emit(ascii_svg(txt))
        fig = lhtml.Element("div", {"class": "fig diagram"})
        etree.SubElement(fig, "img", {"src": src, "alt": "diagram"})
        pre.getparent().replace(pre, fig)


def callouts(root):
    for p in list(root.iter("p")):
        if p.get("class"):
            continue
        kids = list(p)
        if not kids or kids[0].tag != "strong" or (p.text or "").strip():
            continue
        key = " ".join(kids[0].text_content().split()).lower().rstrip(".:!")
        if key not in CALLOUTS:
            continue
        cls, label = CALLOUTS[key]
        box = lhtml.Element("div", {"class": f"co co-{cls}"})
        lab = etree.SubElement(box, "span", {"class": "co-label"})
        lab.text = label
        tail = kids[0].tail or ""
        kids[0].getparent().remove(kids[0])
        body = etree.SubElement(box, "p")
        body.text = tail.lstrip(" .:")
        for c in list(p):
            body.append(c)
        p.getparent().replace(p, box)
    for h in root.iter("h2", "h3"):
        t = " ".join(h.text_content().split()).lower()
        if "check yourself" in t or "teach it back" in t or "teach-back" in t:
            h.set("class", "teach-h")


def data_uri(svg_text):
    return "data:image/svg+xml;base64," + base64.b64encode(svg_text.encode("utf-8")).decode()


def digest(svg_text):
    return hashlib.md5(svg_text.encode("utf-8")).hexdigest()[:10]
