"""Generate a retro side-scrolling SVG animation for GitHub profile."""

SKILLS = ["Python", "Scala", "Java", "Go", "TypeScript", "AWS", "Data", "AI"]

# 8x8 pixel character frames (simplified bio-warrior style)
CHAR_FRAME1 = [
    "..1111..",
    ".111111.",
    ".133331.",
    ".131131.",
    ".133331.",
    "..1111..",
    ".222222.",
    ".224422.",
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
    ".224422.",
    ".222222.",
    ".2....2.",
    ".33..33.",
    "33....33",
]

COLORS = {
    "1": "#89b4fa",  # blue (helmet)
    "2": "#a6e3a1",  # green (body)
    "3": "#f5e0dc",  # skin
    "4": "#f38ba8",  # red accent
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
    item_positions = [
        (170, 95), (370, 75), (570, 90),  # above platforms
        (50, 135), (250, 135), (450, 135), (650, 135), (750, 135),  # ground level
    ]
    for i, (ix, iy) in enumerate(item_positions):
        if i >= len(SKILLS):
            break
        color = ITEM_COLORS[i % len(ITEM_COLORS)]
        # Bouncing item with staggered animation
        delay = i * 0.3
        lines.append(f'<g>')
        lines.append(f'  <animateTransform attributeName="transform" type="translate" '
                     f'values="0,0; 0,-4; 0,0" dur="1.2s" begin="{delay}s" repeatCount="indefinite"/>')
        # Item diamond shape
        lines.append(f'  <rect x="{ix}" y="{iy}" width="8" height="8" fill="{color}" rx="1" '
                     f'transform="rotate(45 {ix+4} {iy+4})"/>')
        # Sparkle
        lines.append(f'  <rect x="{ix+2}" y="{iy+2}" width="4" height="4" fill="white" opacity="0.5" rx="1" '
                     f'transform="rotate(45 {ix+4} {iy+4})"/>')
        lines.append(f'</g>')
        # Label
        lines.append(f'<text x="{ix+4}" y="{iy+18}" text-anchor="middle" '
                     f'font-family="monospace" font-size="7" fill="{color}" opacity="0.8">{SKILLS[i]}</text>')

    # Character with running animation (alternating frames)
    # Frame 1 (visible 0-0.4s)
    lines.append('<g>')
    lines.append('  <animate attributeName="opacity" values="1;1;0;0" dur="0.8s" repeatCount="indefinite"/>')
    lines.append('  <animateTransform attributeName="transform" type="translate" '
                 'values="0,0; 800,0" dur="12s" repeatCount="indefinite"/>')
    char1 = pixel_char(CHAR_FRAME1, 20, ground_y - 36, px)
    lines.append(char1)
    lines.append('</g>')

    # Frame 2 (visible 0.4-0.8s)
    lines.append('<g>')
    lines.append('  <animate attributeName="opacity" values="0;0;1;1" dur="0.8s" repeatCount="indefinite"/>')
    lines.append('  <animateTransform attributeName="transform" type="translate" '
                 'values="0,0; 800,0" dur="12s" repeatCount="indefinite"/>')
    char2 = pixel_char(CHAR_FRAME2, 20, ground_y - 36, px)
    lines.append(char2)
    lines.append('</g>')

    # HUD overlay
    lines.append('<rect x="10" y="8" width="120" height="22" fill="#1e1e2e" opacity="0.8" rx="4"/>')
    lines.append('<text x="18" y="23" font-family="monospace" font-size="11" fill="#cba6f7" font-weight="bold">'
                 '&#x25B6; katsut</text>')

    lines.append('<rect x="670" y="8" width="120" height="22" fill="#1e1e2e" opacity="0.8" rx="4"/>')
    lines.append('<text x="678" y="23" font-family="monospace" font-size="11" fill="#a6e3a1">'
                 'Fukuoka, JP</text>')

    # Score-like display
    lines.append('<rect x="300" y="8" width="200" height="22" fill="#1e1e2e" opacity="0.8" rx="4"/>')
    lines.append('<text x="310" y="23" font-family="monospace" font-size="11" fill="#f9e2af">'
                 'PM / Data Engineer</text>')

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    svg = generate_svg()
    with open("sidescroller.svg", "w") as f:
        f.write(svg)
    print("Generated sidescroller.svg")