"""Clean single-pass replacement of GSD section, GSD_FREQS, and GSD functions."""

with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('/home/ubuntu/gh-repo/new_generator.html', 'r', encoding='utf-8') as f:
    new_gen = f.read()

# ── Extract new section HTML ──────────────────────────────────────────────────
section_start_ng = new_gen.find('<section id="symbol-generator"')
depth = 0
pos = section_start_ng
section_end_ng = None
while pos < len(new_gen):
    open_idx = new_gen.find('<section', pos)
    close_idx = new_gen.find('</section>', pos)
    if close_idx == -1:
        break
    if open_idx != -1 and open_idx < close_idx:
        depth += 1
        pos = open_idx + 1
    else:
        depth -= 1
        if depth == 0:
            section_end_ng = close_idx + len('</section>')
            break
        pos = close_idx + 1

new_section_html = new_gen[section_start_ng:section_end_ng]

# ── Extract new CSS ───────────────────────────────────────────────────────────
new_css = new_gen[:new_gen.find('</style>') + len('</style>')]

# ── Extract new GSD_FREQS ─────────────────────────────────────────────────────
new_freqs_start = new_gen.find('const GSD_FREQS = [')
new_freqs_end = new_gen.find('];', new_freqs_start) + 2
new_freqs = new_gen[new_freqs_start:new_freqs_end]

# ── Extract new JS functions ──────────────────────────────────────────────────
new_funcs_start = new_gen.find('// ── INTENTION COMPATIBILITY MAP')
new_funcs_end = new_gen.rfind('</script>')
new_funcs = new_gen[new_funcs_start:new_funcs_end]

print(f"New section HTML: {len(new_section_html)} chars")
print(f"New CSS: {len(new_css)} chars")
print(f"New GSD_FREQS: {len(new_freqs)} chars")
print(f"New JS functions: {len(new_funcs)} chars")

# ── Positions in original HTML ────────────────────────────────────────────────
GSD_HTML_START  = 222394
GSD_HTML_END    = 230871
FREQS_START     = 358055
FREQS_END       = 362822
FUNCS_START     = 381478
FUNCS_END       = 391672

css_inject_point = html.rfind('</style>')
print(f"CSS inject point: {css_inject_point}")

# ── Work from end to start to preserve positions ──────────────────────────────
# Step 1: Replace functions (highest position first)
html = html[:FUNCS_START] + new_funcs + '\n\n' + html[FUNCS_END:]
delta1 = len(new_funcs) + 2 - (FUNCS_END - FUNCS_START)

# Step 2: Replace GSD_FREQS
FREQS_START += delta1
FREQS_END += delta1
html = html[:FREQS_START] + new_freqs + html[FREQS_END:]
delta2 = len(new_freqs) - (FREQS_END - FREQS_START)

# Step 3: Replace GSD section HTML
GSD_HTML_START += delta1 + delta2
GSD_HTML_END += delta1 + delta2
html = html[:GSD_HTML_START] + new_section_html + html[GSD_HTML_END:]
delta3 = len(new_section_html) - (GSD_HTML_END - GSD_HTML_START)

# Step 4: Inject CSS before last </style>
css_inject_point += delta1 + delta2 + delta3
html = html[:css_inject_point] + '\n' + new_css + '\n' + html[css_inject_point:]

print(f"\nFinal HTML size: {len(html)} chars")
print(f"GSD_FREQS count: {html.count('const GSD_FREQS = [')}")
print(f"body-map-wrap present: {html.find('body-map-wrap') != -1}")
print(f"audio-stack-panel present: {html.find('audio-stack-panel') != -1}")
check = 'section id="symbol-generator"'
print(f"symbol-generator section present: {check in html}")
old_gsd_check = '<section id="gsd">'
print(f"old gsd section present: {old_gsd_check in html}")

with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")
