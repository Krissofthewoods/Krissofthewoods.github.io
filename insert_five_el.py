with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('/home/ubuntu/gh-repo/five-elements.html', 'r', encoding='utf-8') as f:
    five_el = f.read()

insert_marker = '<div class="section-divider"></div>\n\n<!-- THE FRAMEWORK -->'
insert_block = '\n<div class="section-divider"></div>\n\n<!-- FIVE ELEMENTS OF PATTERN -->\n' + five_el + '\n\n'

new_html = html.replace(insert_marker, insert_block + insert_marker, 1)

if new_html == html:
    print("ERROR: marker not found")
else:
    with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    present = 'id="five-elements"' in new_html
    print(f"Done. File size: {len(new_html)}")
    print(f"Five elements section present: {present}")
    print(f"Price $5.55 present: {'5.55' in new_html}")
