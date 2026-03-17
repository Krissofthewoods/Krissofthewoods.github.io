with open('/home/ubuntu/gh-repo/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add the rpms-dot CSS animation
old_rotate = '  @keyframes rotateSlow {\n    from { transform: rotate(0deg); }\n    to { transform: rotate(360deg); }\n  }'
new_rotate = '''  @keyframes rotateSlow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @keyframes rpms-dot {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
    40% { opacity: 1; transform: scale(1.2); }
  }'''

if old_rotate in html:
    html = html.replace(old_rotate, new_rotate, 1)
    print("CSS dot animation added.")
else:
    print("WARNING: rotateSlow CSS not found exactly")

# 2. Find where rpms-loading is shown and add progress bar start
# Search for the JS pattern
idx = html.find("rpms-loading").  # find first occurrence in JS
# Better: search for classList.add('visible') near rpms-loading
import re
pattern = r"document\.getElementById\('rpms-loading'\)\.classList\.add\('visible'\);"
match = re.search(pattern, html)
if match:
    old_show = match.group(0)
    new_show = old_show + """
      let rpmsProgress = 0;
      const rpmsProgressBar = document.getElementById('rpms-progress-bar');
      const rpmsProgressInterval = setInterval(function() {
        rpmsProgress = Math.min(rpmsProgress + (Math.random() * 3 + 0.5), 90);
        rpmsProgressBar.style.width = rpmsProgress + '%';
      }, 600);
      window._rpmsProgressInterval = rpmsProgressInterval;"""
    html = html.replace(old_show, new_show, 1)
    print("RPMS progress start added.")
else:
    print("WARNING: RPMS show not found")

# 3. Find where rpms-loading is hidden and complete the bar
pattern2 = r"document\.getElementById\('rpms-loading'\)\.classList\.remove\('visible'\);"
match2 = re.search(pattern2, html)
if match2:
    old_hide = match2.group(0)
    new_hide = """clearInterval(window._rpmsProgressInterval);
      document.getElementById('rpms-progress-bar').style.width = '100%';
      setTimeout(function() {
        """ + old_hide + """
      }, 400);"""
    html = html.replace(old_hide, new_hide, 1)
    print("RPMS progress complete added.")
else:
    print("WARNING: RPMS hide not found")

# 4. Update GSD JS to show loading state and drive progress bar
old_gsd = "  btn.disabled = true;\n  btn.textContent = 'Generating reading...';\n  box.style.display = 'block';\n  text.textContent = 'Generating reading...';"
new_gsd = """  btn.disabled = true;
  btn.textContent = 'Generating reading...';
  box.style.display = 'block';
  document.getElementById('gsd-loading-state').style.display = 'block';
  document.getElementById('gsd-result-state').style.display = 'none';
  text.textContent = '';
  let gsdProgress = 0;
  const gsdProgressBar = document.getElementById('gsd-progress-bar');
  const gsdProgressInterval = setInterval(function() {
    gsdProgress = Math.min(gsdProgress + (Math.random() * 3 + 0.5), 90);
    gsdProgressBar.style.width = gsdProgress + '%';
  }, 600);"""

if old_gsd in html:
    html = html.replace(old_gsd, new_gsd, 1)
    print("GSD loading start added.")
else:
    print("WARNING: GSD gen not found exactly")

# 5. Find where GSD result is shown (text.textContent = result) and show result state
# After the API call succeeds, the text is set. Find that point.
old_gsd_result = "text.textContent = data.result;"
if old_gsd_result in html:
    new_gsd_result = """clearInterval(gsdProgressInterval);
    document.getElementById('gsd-progress-bar').style.width = '100%';
    setTimeout(function() {
      document.getElementById('gsd-loading-state').style.display = 'none';
      document.getElementById('gsd-result-state').style.display = 'block';
      text.textContent = data.result;
    }, 400);"""
    html = html.replace(old_gsd_result, new_gsd_result, 1)
    print("GSD result reveal added.")
else:
    # Try alternate - find what the GSD does with the result
    idx = html.find('gsd-reading-text')
    while idx != -1:
        ctx = html[idx:idx+200]
        if 'textContent' in ctx or 'innerHTML' in ctx:
            print(f"GSD result at {idx}: {repr(ctx[:150])}")
        idx = html.find('gsd-reading-text', idx+1)

with open('/home/ubuntu/gh-repo/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("File written.")
