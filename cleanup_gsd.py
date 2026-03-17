"""Remove the old GSD section and old GSD_FREQS that were left behind."""

with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"File size: {len(html)}")

# Find old GSD section
old_gsd_start = html.find('<section id="gsd">')
new_sym_start = html.find('<section id="symbol-generator"')
print(f"Old GSD start: {old_gsd_start}")
print(f"New symbol-generator: {new_sym_start}")

if old_gsd_start == -1:
    print("Old GSD section not found - already removed")
else:
    # Find the divider between old GSD and new symbol-generator
    divider_between = html.find('<div class="section-divider">', old_gsd_start)
    print(f"Divider after old GSD: {divider_between}")

    # The old GSD section ends with </section> before the divider
    old_gsd_close = html.rfind('</section>', old_gsd_start, divider_between)
    old_gsd_end = old_gsd_close + len('</section>')
    print(f"Old GSD end: {old_gsd_end} (size: {old_gsd_end - old_gsd_start})")

    # Remove old GSD section + the divider after it
    divider_end = divider_between + len('<div class="section-divider"></div>')
    html = html[:old_gsd_start] + html[divider_end:]
    print(f"After removing old GSD section: {len(html)}")

# Remove old GSD_FREQS (the first/shorter one)
freqs_count = html.count('const GSD_FREQS = [')
print(f"\nGSD_FREQS count: {freqs_count}")

if freqs_count == 2:
    freqs1_start = html.find('const GSD_FREQS = [')
    freqs1_end = html.find('];', freqs1_start) + 2
    freqs2_start = html.find('const GSD_FREQS = [', freqs1_start + 1)
    print(f"GSD_FREQS #1: {freqs1_start} to {freqs1_end} ({freqs1_end - freqs1_start} chars)")
    print(f"GSD_FREQS #2: {freqs2_start}")
    # Remove the first (old, shorter) one
    html = html[:freqs1_start] + html[freqs1_end + 1:]
    print(f"After removing old GSD_FREQS: {len(html)}")

# Final verification
print(f"\n=== FINAL CHECK ===")
print(f"File size: {len(html)}")
print(f"GSD_FREQS count: {html.count('const GSD_FREQS = [')}")
old_check = '<section id="gsd">'
new_check = 'section id="symbol-generator"'
print(f"Old GSD section present: {old_check in html}")
print(f"New symbol-generator present: {new_check in html}")
print(f"body-map-wrap present: {'body-map-wrap' in html}")
print(f"audio-stack-panel present: {'audio-stack-panel' in html}")
print(f"BODY_REGIONS present: {'BODY_REGIONS' in html}")
print(f"playAudioStack present: {'playAudioStack' in html}")

with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
