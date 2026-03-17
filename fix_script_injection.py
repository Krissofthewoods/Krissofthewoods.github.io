#!/usr/bin/env python3
"""
Fix the broken HTML injection inside the main script block.
The new generator section HTML was accidentally inserted at offset 462 inside
the script, breaking the JS at the starfield canvas line.
"""

with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the main script block
script_start = html.rfind('<script>')
script_end = html.rfind('</script>')
script_content = html[script_start+8:script_end]

# Find where the HTML injection starts and ends
inject_start = script_content.find('<section id="symbol-generator"')

# Find the closing </section> by counting nesting depth
depth = 0
pos = inject_start
inject_end = -1
while pos < len(script_content):
    open_pos = script_content.find('<section', pos)
    close_pos = script_content.find('</section>', pos)
    if open_pos == -1 and close_pos == -1:
        break
    if open_pos != -1 and (close_pos == -1 or open_pos < close_pos):
        depth += 1
        pos = open_pos + 1
    else:
        depth -= 1
        pos = close_pos + 10
        if depth == 0:
            inject_end = pos
            break

print(f"Injection: offset {inject_start} to {inject_end}, length {inject_end - inject_start}")

# Extract the injected HTML section (we'll put it back in the body)
injected_html = script_content[inject_start:inject_end]

# The broken JS line before the injection was:
# const canvas = document.getElementByI
# It should be:
# const canvas = document.getElementById('starfield');
before_injection = script_content[:inject_start]
after_injection = script_content[inject_end:]

# Fix the truncated line
broken_line = "const canvas = document.getElementByI"
fixed_line = "const canvas = document.getElementById('starfield')"
before_injection_fixed = before_injection.replace(broken_line, fixed_line)
print(f"Fixed broken line: {broken_line[:40]} -> {fixed_line[:40]}")

# Reassemble the script
fixed_script = before_injection_fixed + after_injection

# Now rebuild the full HTML:
# 1. Put the fixed script back
# 2. Find where the symbol-generator section SHOULD be in the body and ensure it's there

# Check if the symbol-generator section also exists in the body (outside script)
body_section_pos = html.find('<section id="symbol-generator"')
print(f"Symbol generator section in body at: {body_section_pos}")
print(f"Script block starts at: {script_start}")

# The section is only inside the script - we need to put it in the body too
# Find the right place: after the five-elements section, before the framework section
# or at the end of the main content

# Rebuild the HTML with fixed script
new_html = html[:script_start+8] + fixed_script + html[script_end:]

# Now check if symbol-generator section exists in the body
body_check = new_html[:new_html.rfind('<script>')]
sg_in_body = '<section id="symbol-generator"' in body_check
print(f"Symbol generator in body after fix: {sg_in_body}")

if not sg_in_body:
    # Find insertion point: before the footer/sources section
    # Look for the five-elements section end or framework section start
    insert_marker = '<section id="framework"'
    insert_pos = new_html.find(insert_marker)
    if insert_pos == -1:
        insert_marker = '<div class="section-divider"'
        # Find the last divider before the script
        script_pos = new_html.rfind('<script>')
        insert_pos = new_html.rfind(insert_marker, 0, script_pos - 50000)
    
    print(f"Inserting symbol-generator section at body position: {insert_pos}")
    new_html = new_html[:insert_pos] + injected_html + '\n' + new_html[insert_pos:]

# Verify the fix
test_script_start = new_html.rfind('<script>')
test_script_end = new_html.rfind('</script>')
test_script = new_html[test_script_start+8:test_script_end]
has_injection = '<section id="symbol-generator"' in test_script
has_fixed_line = "getElementById('starfield')" in test_script
body_has_section = '<section id="symbol-generator"' in new_html[:new_html.rfind('<script>')]

print(f"\nVerification:")
print(f"  Script still has HTML injection: {has_injection}")
print(f"  Script has fixed starfield line: {has_fixed_line}")
print(f"  Body has symbol-generator section: {body_has_section}")

if not has_injection and has_fixed_line:
    with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("\nFile written successfully.")
else:
    print("\nERROR: Fix did not work as expected. File NOT written.")
