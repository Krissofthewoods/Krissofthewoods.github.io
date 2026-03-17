#!/usr/bin/env python3
"""
The GSD section in the current script has orphaned drawing code after the comment
"// Frequency database for the GSD tool" because the GSD_FREQS array was removed
during the generator rebuild but the drawing functions that follow it were left behind.

Fix: restore the full GSD JS block from git history (commit 020d82c), but keep the
new generator-related functions (selectBodyRegion, renderFreqGrid, playAudioStack etc.)
that were added in the rebuild commit.
"""
import subprocess

# Get the good version
result = subprocess.run(
    ['git', 'show', '020d82c:index.html'],
    capture_output=True, text=True, cwd='/home/ubuntu/gh-repo'
)
old_html = result.stdout

# Extract the full GSD JS block from old version
# From "// ___...GEOMETRIC SEMANTIC DRIVER GENERATOR" to end of its section
gsd_marker = '// _______________________________________________________\n//  GEOMETRIC SEMANTIC DRIVER GENERATOR\n// _______________________________________________________\n'
old_gsd_start = old_html.find(gsd_marker)
# Find where the GSD section ends - look for the next major section comment
old_gsd_end = old_html.find('\n// ___', old_gsd_start + 100)
if old_gsd_end == -1:
    old_gsd_end = old_html.find('\nfunction toggleNav', old_gsd_start)
old_gsd_block = old_html[old_gsd_start:old_gsd_end]
print(f"Old GSD block: {old_gsd_start} to {old_gsd_end}, length {len(old_gsd_block)}")
print(f"Old GSD start: {repr(old_gsd_block[:100])}")
print(f"Old GSD end: {repr(old_gsd_block[-100:])}")

# Now read current file
with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

s = html.rfind('<script>')
e = html.rfind('</script>')
sc = html[s+8:e]

# Find the broken GSD section in current script
cur_gsd_start = sc.find(gsd_marker)
# Find where the current GSD section ends
# It should end where the new generator functions start OR where toggleNav starts
cur_gsd_end = sc.find('\nfunction selectBodyRegion', cur_gsd_start)
if cur_gsd_end == -1:
    cur_gsd_end = sc.find('\nfunction toggleNav', cur_gsd_start)
if cur_gsd_end == -1:
    cur_gsd_end = sc.find('\n// ___', cur_gsd_start + 100)

print(f"\nCurrent GSD block: {cur_gsd_start} to {cur_gsd_end}, length {cur_gsd_end - cur_gsd_start}")
print(f"Current GSD start: {repr(sc[cur_gsd_start:cur_gsd_start+100])}")
print(f"Current GSD end: {repr(sc[cur_gsd_end-100:cur_gsd_end])}")

# Extract the new generator functions that were added in the rebuild
# These come AFTER the old GSD block ends
new_gen_funcs_start = sc.find('\nfunction selectBodyRegion')
if new_gen_funcs_start == -1:
    new_gen_funcs_start = cur_gsd_end
new_gen_funcs_end = sc.find('\nfunction toggleNav', new_gen_funcs_start)
if new_gen_funcs_end == -1:
    new_gen_funcs_end = len(sc)

new_gen_funcs = sc[new_gen_funcs_start:new_gen_funcs_end]
print(f"\nNew generator functions: {new_gen_funcs_start} to {new_gen_funcs_end}, length {len(new_gen_funcs)}")
print(f"New gen start: {repr(new_gen_funcs[:100])}")

# Build the fixed script:
# Before GSD + old GSD block + new generator functions + after new gen funcs
sc_fixed = sc[:cur_gsd_start] + old_gsd_block + new_gen_funcs + sc[new_gen_funcs_end:]

print(f"\nFixed script length: {len(sc_fixed)}")

# Write back
new_html = html[:s+8] + sc_fixed + html[e:]
with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# Verify
sc2 = new_html[new_html.rfind('<script>')+8:new_html.rfind('</script>')]
with open('/tmp/cs_v2.js', 'w') as f:
    f.write(sc2)
print(f"Verification:")
print(f"  Has HTML injection: {'<section id=' in sc2}")
print(f"  Has GSD_FREQS: {'const GSD_FREQS' in sc2}")
print(f"  Has starfield ctx: {'const ctx = canvas.getContext' in sc2}")
print(f"  Has selectBodyRegion: {'function selectBodyRegion' in sc2}")
print(f"  Has toggleNav: {'function toggleNav' in sc2}")
