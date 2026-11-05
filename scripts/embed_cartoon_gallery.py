import os, json

with open("/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca/sleeping-symbolic.svg") as f:
    cartoon_sleep = f.read()

cartoon_runs = []
for i in range(4):
    with open(f"/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca/running-{i}-symbolic.svg") as f:
        cartoon_runs.append(f.read())

def get_inner(s):
    start = s.find(">", s.find("<svg")) + 1
    end = s.rfind("</svg>")
    return s[start:end].strip()

sleep_svg = get_inner(cartoon_sleep)
run_svgs = [get_inner(r) for r in cartoon_runs]

# Read docs/alpaca_gallery.html
with open("/home/mrnv/Documents/local-ai-monitor/docs/alpaca_gallery.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace Candidate 1 in JS
cand1_start = content.find('id: 1,')
cand2_start = content.find('id: 2,')

if cand1_start != -1 and cand2_start != -1:
    new_cand1 = f'''id: 1,
        title: "1. Official Cartoon Line-Art (New)",
        desc: "Authentic Ollama mascot drawing with crisp dark outlines, pure white body fill, cute eyes with sparkle, and inverted Y snout.",
        sleeping: `{sleep_svg}`,
        running: [
          `{run_svgs[0]}`,
          `{run_svgs[1]}`,
          `{run_svgs[2]}`,
          `{run_svgs[3]}`
        ]
      }},

      {{
        '''
    # slice out old cand1
    prefix = content[:cand1_start]
    suffix = content[cand2_start:]
    updated_content = prefix + new_cand1 + suffix

    with open("/home/mrnv/Documents/local-ai-monitor/docs/alpaca_gallery.html", "w", encoding="utf-8") as f:
        f.write(updated_content)

    brain_path = "/home/mrnv/.gemini/antigravity/brain/6a31e139-ea5a-4089-b458-8aa8b4fb0fa4/alpaca_gallery.html"
    with open(brain_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("Gallery updated successfully.")
else:
    print("Could not find candidate boundaries.")
