import base64
import os

base_dir = "/Users/norton/Desktop/Cannibisters Agent/wheel_of_fortune"

def read_file(filename):
    with open(os.path.join(base_dir, filename), 'r') as f:
        return f.read()

def read_binary(filename):
    with open(os.path.join(base_dir, filename), 'rb') as f:
        return f.read()

html = read_file("index.html")
css = read_file("style.css")
js = read_file("script.js")

# Manual fix for JS radius if needed (ensure it matches latest)
# js = js.replace("wheelRadius * 0.55", "wheelRadius * 0.42") # Already fixed in file

logo_data = read_binary("logo.png")
logo_b64 = base64.b64encode(logo_data).decode('utf-8')
logo_src = f"data:image/png;base64,{logo_b64}"

# Inline CSS
html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>\n{css}\n</style>')

# Inline Logo
html = html.replace('src="logo.png"', f'src="{logo_src}"')

# Inline JS
html = html.replace('<script src="script.js"></script>', f'<script>\n{js}\n</script>')

output_path = os.path.join(base_dir, "cannibisters_wheel.html")
with open(output_path, 'w') as f:
    f.write(html)

print(f"Bundled app updated at: {output_path}")
