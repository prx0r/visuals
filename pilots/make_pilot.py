"""10s intro pilots: our gloss typography, animated, synced to the bowls strike (t=2.5s)."""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

FONTS = "/root/.fonts/"
INK, WHITE, VERM = (23, 20, 15), (255, 255, 255), (160, 43, 30)
INK50 = (118, 115, 110)
W, H, FPS, DUR = 1920, 1080, 30, 10.0
OUT = "/home/box/visuals/pilots"
ROOT = "/home/box/Downloads/yt/baumer"

def f(path, size, wght=None):
    ft = ImageFont.truetype(FONTS + path, size)
    if wght is not None:
        try:
            axes = ft.get_variation_axes()
            vals = [min(max(wght, a.get("minimum", 0)), a.get("maximum", 700))
                    if (b"eight" in a.get("name", b"") or a.get("name") in ("Weight", "wght"))
                    else a.get("default", a.get("minimum", 0)) for a in axes]
            ft.set_variation_by_axes(vals)
        except Exception:
            pass
    return ft

def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def ease_back(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def balance_wrap(text, ft, maxw):
    words = text.split()
    widths = [ft.getlength(w + " ") for w in words]
    total = sum(widths)
    if total <= maxw:
        return [text]
    # try every split point, minimize line-length imbalance (prefer >=2 lines)
    best, bi = None, 1
    for i in range(1, len(words)):
        l1, l2 = sum(widths[:i]) - widths[i - 1], sum(widths[i:])
        if l1 <= maxw and l2 <= maxw:
            score = abs(l1 - l2)
            if best is None or score < best:
                best, bi = score, i
    if best is None:
        bi = len(words) // 2
    return [" ".join(words[:bi]), " ".join(words[bi:])]


def blend(color, a):
    return tuple(round(WHITE[i] - (WHITE[i] - color[i]) * a) for i in range(3))

CARDS = {
 "verse_3": dict(dev=["उभयपट्टोद्धट्टनान्", "महाशून्यताप्रवेशः"], devsize=82,
   ia="ubhayapaṭṭoddhaṭṭanān mahāśūnyatāpraveśaḥ || 3 ||", pos=None,
   definition="Entry into the great vacuity results from the bursting open of the two boards.",
   deep=None, source="Vātūlanātha Sūtra 3 · KSTS 1923 · Muktabodha M00099"),
 "term_svatantrya": dict(dev=["स्वातन्त्र्य"], devsize=132, ia="Svātantrya", pos="(n.)",
   definition="pure freedom",
   deep=" Realisation arrives “without any cause, by their mode of action of supreme freedom” — neither forced nor earned; it is its own cause.",
   source=None),
 "verse_10": dict(dev=["द्वादशवाहोदयेन", "महामरीचिविकासः"], devsize=82,
   ia="dvādaśavāhodayena mahāmarīcivikāsaḥ || 10 ||", pos=None,
   definition="The play of the big rays follows the emanation of the twelve currents.",
   deep=None, source="Vātūlanātha Sūtra 10 · KSTS 1923 · Muktabodha M00099"),
}

X, Y0 = 140, 124
RULE_Y = Y0 + int(132 * 1.36) + int(132 * 0.18) + 72 + 56 + 12 + 8  # set below per-card instead

def layout(c):
    y = Y0
    dev_h = len(c["dev"]) * int(c["devsize"] * 1.36)
    y_after_dev = Y0 + dev_h + int(c["devsize"] * 0.18)
    y_ia = y_after_dev
    y_pos = y_ia + 72 if c["pos"] else None
    y_rule = (y_pos + 44 + 12) if c["pos"] else (y_ia + 72 + 12)
    y_def = y_rule + 46
    return dict(dev=Y0, ia=y_ia, pos=y_pos, rule=y_rule, dev_h=dev_h)

def render_frame(c, L, t):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    # rule draws 0.6-1.6
    rp = ease((t - 0.6) / 1.0)
    if rp > 0:
        y = L["rule"]
        d.rectangle([X, y, X + int(185 * rp), y + 2], fill=INK50)
    # dot pops 1.7-2.05, breathes after 2.0
    dp = ease_back((t - 2.55) / 0.35)
    if dp > 0.02:
        breath = 1.0 if t < 3.0 else 0.85 + 0.15 * math.sin((t - 3.0) * 2 * math.pi / 3.0)
        r = 4.5 * min(dp, 1.0)
        cx, cy = X + 201, L["rule"] + 1
        a = min(dp, 1.0) * breath
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=blend(VERM, a))
    # headword ink-wipe top->bottom 2.5-3.4
    hp = ease((t - 2.5) / 0.9)
    if hp > 0:
        fd = f("RozhaOne-Regular.ttf", c["devsize"])
        tmp = Image.new("L", (W, H), 0)
        td = ImageDraw.Draw(tmp)
        for i, line in enumerate(c["dev"]):
            td.text((X, L["dev"] + i * int(c["devsize"] * 1.36)), line, font=fd, fill=255)
        reveal = int((L["dev"] + c["devsize"] * 1.36 * len(c["dev"])) * hp) + 40
        td.rectangle([0, reveal, W, H], fill=0)
        ink_layer = Image.new("RGB", (W, H), INK)
        img.paste(ink_layer, (0, 0), tmp)
    # translit fade+rise 3.6-4.4
    ip = ease((t - 3.6) / 0.8)
    if ip > 0:
        fi = f("CormorantGaramond-Italic[wght].ttf", 50, 500)
        dy = int((1 - ip) * 14)
        d.text((X, L["ia"] + dy), c["ia"], font=fi, fill=blend(INK, ip))
    # pos 4.5-4.9
    if c["pos"]:
        pp = ease((t - 4.5) / 0.4)
        if pp > 0:
            d.text((X, L["pos"] + int((1 - pp) * 10)), c["pos"],
                   font=f("CormorantGaramond-Italic[wght].ttf", 36, 500), fill=blend(INK, pp))
    # definition fade+rise 5.3-6.0
    fs = f("CormorantGaramond[wght].ttf", 63, 600)
    lines = balance_wrap(c["definition"], fs, 1420)
    fp = ease((t - 5.3) / 0.7)
    if fp > 0:
        for i, ln in enumerate(lines):
            d.text((X, L["rule"] + 46 + i * 80 + int((1 - fp) * 12)), ln,
                   font=fs, fill=blend(INK, fp))
    # deep / source 6.4-7.6
    gp = ease((t - 6.4) / 1.2)
    base_y = L["rule"] + 46 + 80 * len(lines) + 34
    if c["deep"] and gp > 0:
        fdi = f("CormorantGaramond-Italic[wght].ttf", 34, 500)
        fdb = f("CormorantGaramond[wght].ttf", 34, 500)
        lead, body = "A deeper meaning:", c["deep"]
        dl = balance_wrap(body, fdb, 1380 - fdi.getlength(lead))
        y = base_y + int((1 - gp) * 8)
        d.text((X, y), lead, font=fdi, fill=blend(INK, gp))
        d.text((X + fdi.getlength(lead) + fdb.getlength(" "), y), dl[0], font=fdb, fill=blend(INK, gp))
        for i, ln in enumerate(dl[1:]):
            d.text((X, y + 52 * (i + 1)), ln, font=fdb, fill=blend(INK, gp))
    if c["source"] and gp > 0:
        d.text((X, base_y + (52 * len(balance_wrap(c["deep"], f("CormorantGaramond[wght].ttf", 34, 500), 1380)) + 70 if c["deep"] else 0)),
               c["source"], font=f("CormorantGaramond[wght].ttf", 27, 400),
               fill=blend((150, 147, 141), gp))
    return img

def make(name, card, audio_path):
    c = CARDS[card]
    L = layout(c)
    frames = os.path.join(OUT, "_f_" + name)
    os.makedirs(frames, exist_ok=True)
    n = int(DUR * FPS)
    for i in range(n):
        render_frame(c, L, i / FPS).save(f"{frames}/{i:04d}.png")
    out = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", f"{frames}/{i:04d}.png".replace("%04d", "%04d"),
                    "-i", audio_path,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=False)
    # correct glob input
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-pattern_type", "glob", "-i", f"{frames}/*.png",
                    "-i", audio_path,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    shutil.rmtree(frames)
    print("OK", out, os.path.getsize(out) // 1024, "KB")

if __name__ == "__main__":
    # audio: bowls file 12.76s, strike at 5.51 -> cut [3.0,13.0] => strike at clip 2.51
    aud = os.path.join(OUT, "_pilot_bowl.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "3.0", "-t", "10.0",
                    "-i", f"{ROOT}/sfx/bowls_intro.wav",
                    "-af", "afade=t=out:st=9.5:d=0.5", "-ar", "44100", "-ac", "2",
                    "-c:a", "pcm_s16le", aud], check=True)
    make("pilot_verse3", "verse_3", aud)
    make("pilot_svatantrya", "term_svatantrya", aud)
    make("pilot_verse10", "verse_10", aud)
