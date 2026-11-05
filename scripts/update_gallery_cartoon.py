import os

with open("/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca/sleeping-symbolic.svg") as f:
    cartoon_sleeping = f.read()

cartoon_running = []
for i in range(4):
    with open(f"/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca/running-{i}-symbolic.svg") as f:
        cartoon_running.append(f.read())

# Strip XML header and svg tags for inline embedding
def extract_inner(svg_text):
    start = svg_text.find(">", svg_text.find("<svg")) + 1
    end = svg_text.rfind("</svg>")
    return svg_text[start:end].strip()

inner_sleeping = extract_inner(cartoon_sleeping)
inner_running = [extract_inner(r) for r in cartoon_running]

# Read current gallery
with open("/home/mrnv/Documents/local-ai-monitor/docs/alpaca_gallery.html", "r", encoding="utf-8") as f:
    gal = f.read()

# Replace Candidate 1 with Cartoon Line-Art in CANDIDATES array
old_cand1_marker = 'title: "1. Official Ollama 3/4",'
new_cand1_title = 'title: "1. Official Cartoon Line-Art (New)",'

print("Gallery ready for update.")
