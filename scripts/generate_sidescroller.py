"""Generate a retro side-scrolling SVG animation for GitHub profile."""

SKILLS = ["Python", "Scala", "Data", "Go", "TypeScript", "AWS", "AI"]

# 8x8 pixel character frames (simplified bio-warrior style)
CHAR_FRAME1 = [
    "..1111..",
    ".111111.",
    ".133331.",
    ".131131.",
    ".133331.",
    "..1111..",
    ".222222.",
    ".222222.",
    ".222222.",
    "..2..2..",
    ".33..33.",
    ".33..33.",
]

CHAR_FRAME2 = [
    "..1111..",
    ".111111.",
    ".133331.",
    ".131131.",
    ".133331.",
    "..1111..",
    ".222222.",
    ".222222.",
    ".222222.",
    ".2....2.",
    ".33..33.",
    "33....33",
]

# Crawl frames: 16 cols x 12 rows, facing right, on all fours
CRAWL_FRAME1 = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..........1111..",
    ".........111111.",
    "..22222..133331.",
    "..222222.133131.",
    "..222222.133331.",
    "..33..33..3333..",
]

CRAWL_FRAME2 = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..........1111..",
    ".........111111.",
    "..22222..133331.",
    "..222222.133131.",
    "..222222.133331.",
    ".33....33.3333..",
]

COLORS = {
    "1": "#7c5c3a",  # brown hair
    "2": "#a6e3a1",  # green (body)
    "3": "#f5e0dc",  # skin
    "4": "#f38ba8",  # red accent (unused in side view)
}

GROUND_COLOR = "#45475a"
SKY_COLOR = "#1e1e2e"
STAR_COLOR = "#585b70"
PLATFORM_COLOR = "#585b70"
ITEM_COLORS = ["#f38ba8", "#fab387", "#f9e2af", "#a6e3a1", "#89b4fa", "#cba6f7", "#f5c2e7", "#94e2d5"]


def pixel_char(frame, x_off, y_off, px=3):
    """Render a pixel character as SVG rects."""
    rects = []
    for r, row in enumerate(frame):
        for c, ch in enumerate(row):
            if ch != "." and ch in COLORS:
                rects.append(
                    f'<rect x="{x_off + c * px}" y="{y_off + r * px}" '
                    f'width="{px}" height="{px}" fill="{COLORS[ch]}"/>'
                )
    return "\n".join(rects)


def build_jump_path():
    """Build keyframe values and timing for platform jump animation.

    Character base position is (20, ground_y-36) = (20, 124).
    Translate offsets (dx, dy) move from that origin.
    Platform surfaces: (150, y=120), (350, y=100), (550, y=115).
    dy to stand on platform = surface_y - ground_y = surface_y - 160.
    """
    # Character left edge = 20 + dx. Must reach full height
    # BEFORE platform left edge (x=150, 350, 550).
    # P1: need dy=-40  by dx<130  (platform x=150)
    # P2: need dy=-60  by dx<330  (platform x=350, highest→earliest start)
    # P3: need dy=-45  by dx<530  (platform x=550)
    pts = [
        # ground run
        (0, 0),
        (80, 0),
        # jump to P1 (dy=-40) — clear by dx=125
        (100, -20),
        (125, -40),
        (175, -40),   # run across platform 1
        (195, -40),
        # drop off
        (215, -20),
        (240, 0),
        # ground run
        (265, 0),
        # jump to P2 (dy=-60) — highest, start earliest, clear by dx=322
        (285, -15),
        (305, -35),
        (322, -60),
        (380, -60),   # run across platform 2
        (395, -60),
        # drop off
        (415, -30),
        (440, 0),
        # ground run
        (485, 0),
        # jump to P3 (dy=-45) — clear by dx=525
        (502, -15),
        (518, -35),
        (525, -45),
        (578, -45),   # run across platform 3
        (595, -45),
        # drop off
        (612, -22),
        (640, 0),
        # ground run to exit
        (780, 0),
    ]
    max_dx = pts[-1][0]
    values = "; ".join(f"{dx} {dy}" for dx, dy in pts)
    key_times = "; ".join(
        f"{dx / max_dx:.4f}" if 0 < dx < max_dx else ("0" if dx == 0 else "1")
        for dx, _ in pts
    )
    return values, key_times


def generate_svg():
    w, h = 800, 200
    ground_y = 160
    px = 3

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')

    # Background
    lines.append(f'<rect width="{w}" height="{h}" fill="{SKY_COLOR}"/>')

    # Stars (static)
    import random
    random.seed(42)
    for _ in range(30):
        sx, sy = random.randint(0, w), random.randint(0, ground_y - 20)
        size = random.choice([1, 2])
        opacity = random.choice([0.3, 0.5, 0.7])
        lines.append(f'<rect x="{sx}" y="{sy}" width="{size}" height="{size}" fill="{STAR_COLOR}" opacity="{opacity}"/>')

    # Ground tiles
    for x in range(0, w, 16):
        lines.append(f'<rect x="{x}" y="{ground_y}" width="15" height="15" fill="{GROUND_COLOR}" rx="1"/>')
        lines.append(f'<rect x="{x}" y="{ground_y + 16}" width="15" height="24" fill="#313244" rx="1"/>')

    # Floating platforms
    platforms = [(150, 120), (350, 100), (550, 115)]
    for px_pos, py_pos in platforms:
        for bx in range(4):
            lines.append(
                f'<rect x="{px_pos + bx * 16}" y="{py_pos}" width="15" height="10" fill="{PLATFORM_COLOR}" rx="1"/>'
            )

    # Skill items floating above platforms + along ground
    # Each item disappears when the character reaches it, then reappears next cycle
    item_positions = [
        (70, 135),    # ground (char arrives ~dx=50 → x≈70)
        (170, 95),    # platform 1
        (270, 135),   # ground
        (370, 75),    # platform 2
        (470, 135),   # ground
        (570, 90),    # platform 3
        (720, 135),   # ground
    ]
    anim_dur = 12  # must match character travel duration
    for i, (ix, iy) in enumerate(item_positions):
        if i >= len(SKILLS):
            break
        color = ITEM_COLORS[i % len(ITEM_COLORS)]
        # Time when character center (x≈32+dx) reaches this item
        # Character starts at x=20, center≈32. Item at ix. dx = ix - 32.
        hit_dx = max(0, ix - 32)
        hit_t = hit_dx / 780  # fraction of 12s cycle
        # Item visible until character arrives, then vanish, reappear at cycle reset
        t1 = f"{max(0, hit_t - 0.01):.3f}"
        t2 = f"{min(1, hit_t):.3f}"
        t3 = f"{min(1, hit_t + 0.02):.3f}"
        bounce_delay = i * 0.3
        lines.append(f'<g>')
        # Disappear on collect, reappear at loop
        lines.append(f'  <animate attributeName="opacity" '
                     f'values="1; 1; 0; 0; 0; 1" '
                     f'keyTimes="0; {t1}; {t2}; {t3}; 0.99; 1" '
                     f'dur="{anim_dur}s" repeatCount="indefinite" calcMode="discrete"/>')
        lines.append(f'  <animateTransform attributeName="transform" type="translate" '
                     f'values="0,0; 0,-4; 0,0" dur="1.2s" begin="{bounce_delay}s" repeatCount="indefinite"/>')
        # Item diamond shape
        lines.append(f'  <rect x="{ix}" y="{iy}" width="8" height="8" fill="{color}" rx="1" '
                     f'transform="rotate(45 {ix+4} {iy+4})"/>')
        # Sparkle
        lines.append(f'  <rect x="{ix+2}" y="{iy+2}" width="4" height="4" fill="white" opacity="0.5" rx="1" '
                     f'transform="rotate(45 {ix+4} {iy+4})"/>')
        lines.append(f'</g>')
        # Label (also disappears)
        lines.append(f'<text x="{ix+4}" y="{iy+18}" text-anchor="middle" '
                     f'font-family="monospace" font-size="7" fill="{color}" opacity="0.8">'
                     f'<animate attributeName="opacity" '
                     f'values="0.8; 0.8; 0; 0; 0; 0.8" '
                     f'keyTimes="0; {t1}; {t2}; {t3}; 0.99; 1" '
                     f'dur="{anim_dur}s" repeatCount="indefinite" calcMode="discrete"/>'
                     f'{SKILLS[i]}</text>')

    # Character: crawl on ground, stand in air
    jump_values, jump_key_times = build_jump_path()
    # Stand only during jump ascent, crawl everywhere else
    # Ascent: dx 80→125, 265→322, 485→525
    # keyTimes based on dx/780
    phase_kt = (
        "0;0.1026;0.1603;"      # gnd → ascent P1 → land P1
        "0.3397;0.4128;"        # ascent P2 → land P2
        "0.6218;0.6731;1"       # ascent P3 → land P3
    )
    crawl_op = "1;0;1;0;1;0;1;1"
    stand_op = "0;1;0;1;0;1;0;0"

    def add_char(frame, x, y, walk_vals, phase_op):
        lines.append('<g>')
        lines.append(
            f'<animate attributeName="opacity"'
            f' values="{phase_op}"'
            f' keyTimes="{phase_kt}"'
            f' dur="12s" calcMode="discrete"'
            f' repeatCount="indefinite"/>'
        )
        lines.append('<g>')
        lines.append(
            f'<animate attributeName="opacity"'
            f' values="{walk_vals}" dur="0.8s"'
            f' repeatCount="indefinite"/>'
        )
        lines.append(
            f'<animateTransform attributeName="transform"'
            f' type="translate" values="{jump_values}"'
            f' keyTimes="{jump_key_times}"'
            f' dur="12s" repeatCount="indefinite"/>'
        )
        lines.append(pixel_char(frame, x, y, px))
        lines.append('</g>')
        lines.append('</g>')

    cy = ground_y - 36
    # Crawl on ground (alternating)
    add_char(CRAWL_FRAME1, 20, cy, "1;1;0;0", crawl_op)
    add_char(CRAWL_FRAME2, 20, cy, "0;0;1;1", crawl_op)
    # Stand during jump ascent only
    add_char(CHAR_FRAME1, 20, cy, "1;1;0;0", stand_op)
    add_char(CHAR_FRAME2, 20, cy, "0;0;1;1", stand_op)

    # HUD overlay
    lines.append('<rect x="10" y="8" width="120" height="22" fill="#1e1e2e" opacity="0.8" rx="4"/>')
    lines.append('<text x="18" y="23" font-family="monospace" font-size="11" fill="#cba6f7" font-weight="bold">'
                 '&#x25B6; katsut</text>')

    lines.append('<rect x="670" y="8" width="120" height="22" fill="#1e1e2e" opacity="0.8" rx="4"/>')
    lines.append('<text x="678" y="23" font-family="monospace" font-size="11" fill="#a6e3a1">'
                 'Fukuoka, JP</text>')

    # Score-like display
    lines.append('<rect x="260" y="8" width="280" height="22" fill="#1e1e2e" opacity="0.8" rx="4"/>')
    lines.append('<text x="270" y="23" font-family="monospace" font-size="11" fill="#f9e2af">'
                 'PM / Data Eng / Instructor</text>')

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    svg = generate_svg()
    with open("sidescroller.svg", "w") as f:
        f.write(svg)
    print("Generated sidescroller.svg")