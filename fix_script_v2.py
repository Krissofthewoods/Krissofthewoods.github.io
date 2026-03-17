#!/usr/bin/env python3
"""
Comprehensive fix for the broken script block.
The injection left the script with:
1. Missing starfield ctx/stars code after the canvas line
2. Orphaned Capricorn/Aquarius lines (tail of energyText object) with no opening
3. The full starfield + energyText block needs to be restored

Strategy: restore the starfield block from git history and replace the broken section.
"""
import subprocess

# Get the good version from git
result = subprocess.run(
    ['git', 'show', '020d82c:index.html'],
    capture_output=True, text=True, cwd='/home/ubuntu/gh-repo'
)
old_html = result.stdout

# Extract the full starfield + energyText block from old version
# From "// STARFIELD" to just before "function getCurrentSign"
sf_start = old_html.find('\n// STARFIELD\n')
fg_start = old_html.find('\nfunction getCurrentSign()')
good_block = old_html[sf_start:fg_start]
print(f"Good block length: {len(good_block)}")
print(f"Good block start: {repr(good_block[:80])}")
print(f"Good block end: {repr(good_block[-80:])}")

# Now fix the current file
with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.rfind('<script>')
e = html.rfind('</script>')
sc = html[s+8:e]

# Find the broken section in current script:
# From "// STARFIELD" to just before "function getCurrentSign"
broken_sf_start = sc.find('\n// STARFIELD\n')
broken_fg_start = sc.find('\nfunction getCurrentSign()')
broken_block = sc[broken_sf_start:broken_fg_start]
print(f"\nBroken block length: {len(broken_block)}")
print(f"Broken block start: {repr(broken_block[:80])}")
print(f"Broken block end: {repr(broken_block[-80:])}")

# Replace broken block with good block
sc_fixed = sc[:broken_sf_start] + good_block + sc[broken_fg_start:]
print(f"\nFixed script length: {len(sc_fixed)}")

# Write back
new_html = html[:s+8] + sc_fixed + html[e:]
with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# Verify
sc2 = new_html[new_html.rfind('<script>')+8:new_html.rfind('</script>')]
with open('/tmp/cs_final.js', 'w') as f:
    f.write(sc2)
print(f"Final script length: {len(sc2)}")
print("Has HTML injection:", '<section id=' in sc2)
print("Has starfield ctx:", "const ctx = canvas.getContext" in sc2)
print("Has energyText:", "const energyText" in sc2)
print("Has Capricorn orphan:", ";\n  Capricorn:" in sc2)
