import os

def create_svg(path_data, title, extra_elements=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 32 32" class="symbolic">
  <title>{title}</title>
  {extra_elements}
  <path d="{path_data}" style="fill: currentColor; fill-rule: evenodd; stroke: none;" />
</svg>
'''

# 1. Idle (Standing alert)
idle_body = (
    # Ears
    "M 19,3 C 18,3 17.5,4 17.5,5.5 L 17.5,8 "
    "M 21.5,2.5 C 20.5,2.5 20,3.5 20,5 L 20,8 "
    # Head & Snout
    "M 16,8 C 16,6.5 17.5,5 19.5,5 L 22.5,5 C 24.5,5 26.5,6.2 26.5,8 C 26.5,9.5 25.2,10.5 23.5,10.5 L 21.5,10.5 "
    # Neck down to chest
    "L 21.5,16.5 C 21.5,18 22.5,19 22.5,19.5 "
    # Front Leg 1 (right)
    "L 22.5,27.5 C 22.5,28.3 21.5,28.5 20.5,28.5 C 19.8,28.5 19.5,28 19.5,27.5 L 19.5,21.5 "
    # Belly
    "L 13.5,21.5 "
    # Back Leg 1 (right)
    "L 13.5,27.5 C 13.5,28.3 12.5,28.5 11.5,28.5 C 10.8,28.5 10.5,28 10.5,27.5 L 10.5,21.5 "
    # Rump and Tail
    "L 8.5,21 C 7.5,21 7,20 7,19 C 6,19 5.5,18 5.5,17 C 5.5,15.8 6.5,15.5 7.5,16 L 8.5,16.2 "
    # Back to neck
    "C 9.5,16 15.5,16 16.5,15 L 16.5,8 Z "
    # Back Leg 2 (left / shadow)
    "M 8.5,21.5 L 8.5,27 C 8.5,27.6 7.8,28 7.2,28 C 6.6,28 6.2,27.5 6.2,27 L 6.2,19.5 Z "
    # Front Leg 2 (left / shadow)
    "M 17.5,21.5 L 17.5,27 C 17.5,27.6 16.8,28 16.2,28 C 15.6,28 15.2,27.5 15.2,27 L 15.2,20 Z"
)

# 2. Running Frame 0 (Stride stretch - Front leg forward, Rear leg back)
run0_body = (
    # Ears swept slightly back
    "M 17,4 C 16,3.5 15,4.5 15.5,6 L 16.5,8.5 "
    "M 19.5,3 C 18.5,2.5 17.5,3.5 18,5 L 19,8 "
    # Head & Snout leaning forward
    "M 15.5,8.5 C 15.5,7 17,5.5 19,5.5 L 23,5.5 C 25.5,5.5 27.5,6.8 27.5,8.5 C 27.5,10 26,11 24,11 L 21.5,11 "
    # Neck to chest
    "L 21.5,16 "
    # Front Leg reaching forward
    "L 25.5,21 L 28,24.5 C 28.5,25.2 27.8,26 27,26 C 26.2,26 25.5,25.3 25,24.5 L 22.5,21 "
    # Belly
    "L 14,21 "
    # Rear leg pushing down/forward
    "L 13,25.5 C 13,26.3 12,26.5 11,26.5 C 10.3,26.5 10,26 10,25.5 L 10.8,21 "
    # Tail up in excitement
    "L 8.5,20.5 C 7.5,20.5 7,19.5 7,18.5 C 5.8,18.5 5,17 5.5,15.5 C 6,14.5 7.2,14.5 8,15.5 L 9,16 "
    # Back
    "L 16,15 L 15.5,8.5 Z "
    # Opposing front leg bent trailing
    "M 19.5,20 L 21,23.5 C 21.3,24.2 20.6,25 19.8,25 C 19.2,25 18.8,24.4 18.5,23.8 L 17.5,20.5 Z "
    # Opposing back leg kicking far backward
    "M 9.5,20.5 L 6,23.5 L 3.5,25.5 C 2.8,26.1 2,25.5 2,24.7 C 2,24 2.6,23.5 3.2,23 L 6.5,20 Z"
)

# 3. Running Frame 1 (Gather phase - Legs gathered under body)
run1_body = (
    # Ears
    "M 18,3.5 C 17,3 16.2,4 16.5,5.5 L 17,8 "
    "M 20.5,2.8 C 19.5,2.2 18.5,3.2 19,4.8 L 19.5,7.8 "
    # Head & Snout
    "M 16,8 C 16,6.5 17.5,5.2 19.5,5.2 L 23,5.2 C 25.2,5.2 27,6.5 27,8.2 C 27,9.8 25.5,10.8 23.5,10.8 L 21.5,10.8 "
    # Neck and chest slightly lowered
    "L 21.5,17 "
    # Front leg tucked backward
    "L 21,22.5 L 19,25.5 C 18.5,26.2 17.5,26.2 17,25.5 C 16.5,24.8 17,24 17.5,23.3 L 19,21 "
    # Belly
    "L 14,21.5 "
    # Rear leg gathered forward under body
    "L 14,25.5 C 14,26.3 13.2,26.8 12.5,26.8 C 11.8,26.8 11.2,26.2 11.2,25.5 L 11.8,21.5 "
    # Tail
    "L 8.5,21 C 7.5,21 7,20 7,19 C 5.8,19 5.2,17.5 5.8,16.2 C 6.5,15.2 7.5,15.5 8.2,16.2 L 9,16.5 "
    # Back
    "L 16,16 L 16,8 Z "
    # Secondary front leg gathered
    "M 19.5,21 L 18.2,24.2 C 17.8,25 17,25 16.5,24.2 C 16.2,23.6 16.6,22.8 17.2,22.2 L 18.2,20.8 Z "
    # Secondary rear leg swinging forward
    "M 11,21.5 L 12.5,25 C 12.8,25.7 12.2,26.4 11.5,26.4 C 10.8,26.4 10.3,25.8 10,25.2 L 9.2,21.5 Z"
)

# 4. Running Frame 2 (Stride stretch B - Opposing front forward, opposing rear back)
run2_body = (
    # Ears
    "M 17.5,4 C 16.5,3.5 15.5,4.5 16,6 L 17,8.5 "
    "M 20,3 C 19,2.5 18,3.5 18.5,5 L 19.2,8 "
    # Head
    "M 16,8.5 C 16,7 17.2,5.5 19.2,5.5 L 23.2,5.5 C 25.5,5.5 27.5,6.8 27.5,8.5 C 27.5,10 26,11 24,11 L 21.5,11 "
    # Neck
    "L 21.5,16 "
    # Front leg 1 tucked trailing
    "L 20.5,21 L 19,24 C 18.5,24.8 17.5,24.8 17,24 C 16.5,23.3 17,22.5 17.8,21.8 L 19.5,20.5 "
    # Belly
    "L 13.5,21 "
    # Rear leg 1 driving back
    "L 10,21 L 6.5,24.5 C 5.8,25.2 4.8,24.8 4.8,24 C 4.8,23.3 5.5,22.8 6.2,22.2 L 8.5,20.5 "
    # Tail
    "L 8.5,20.5 C 7.5,20.5 7,19.5 7,18.5 C 5.8,18.5 5,17 5.5,15.5 C 6,14.5 7.2,14.5 8,15.5 L 9,16 "
    # Back
    "L 16,15 L 16,8.5 Z "
    # Front leg 2 reaching forward
    "M 21.5,19 L 24.5,22.5 L 27,25.5 C 27.6,26.2 26.8,27 26,27 C 25.2,27 24.6,26.3 24,25.5 L 21.5,22 Z "
    # Rear leg 2 driving downward
    "M 12.5,21 L 12,25.5 C 12,26.3 11,26.5 10.2,26.5 C 9.5,26.5 9,26 9,25.5 L 9.8,21 Z"
)

# 5. Running Frame 3 (Flight / Leap phase - All 4 legs airborne)
run3_body = (
    # Ears swept back
    "M 16.5,4.5 C 15.5,4 14.5,5 15,6.5 L 16,8.8 "
    "M 19,3.5 C 18,3 17,4 17.5,5.5 L 18.2,8.2 "
    # Head high
    "M 15.2,8.2 C 15.2,6.8 16.8,5.2 18.8,5.2 L 23,5.2 C 25.5,5.2 27.5,6.5 27.5,8.2 C 27.5,9.8 26,10.8 24,10.8 L 21.5,10.8 "
    # Neck and chest raised (y-1)
    "L 21.5,15 "
    # Front legs extended high in flight
    "L 25.5,18 L 29,21 C 29.8,21.7 29.2,22.8 28.2,22.8 C 27.5,22.8 26.8,22.2 26.2,21.5 L 23,19 "
    # Belly raised
    "L 13.5,19.5 "
    # Rear legs extended far back in flight
    "L 8.5,19 L 4.5,21.5 L 2,23.5 C 1.2,24.1 0.5,23.2 0.8,22.4 C 1,21.8 1.8,21.2 2.5,20.8 L 6.5,18.5 "
    # Tail high
    "L 8,19 C 7,19 6.5,18 6.5,17 C 5.5,17 4.8,15.5 5.5,14 C 6.2,13 7.5,13.2 8.2,14.2 L 9,15 "
    # Back
    "L 16,14 L 15.2,8.2 Z "
    # Secondary front leg leaping
    "M 21.5,17.5 L 24.5,20 L 27.5,22.5 C 28.2,23.1 27.5,24 26.7,24 C 26,24 25.4,23.5 24.8,22.8 L 22,20 Z "
    # Secondary rear leg extended back
    "M 9.5,19 L 5.5,22 C 4.8,22.6 4.2,22 4.2,21.2 C 4.2,20.6 4.8,20.2 5.5,19.8 L 8.5,18 Z"
)

# 6. Offline / Sleeping Frame (Curled up, eyes closed, sleep bubbles)
offline_body = (
    # Curled resting body
    "M 19,16 C 18,15 17,16 16.5,17 L 16.5,19 "
    "M 18,19 C 18,17.5 19.5,16.5 21,16.5 L 24,16.5 C 25.8,16.5 27,17.5 27,19 C 27,20.2 26,21 24.5,21 L 22,21 "
    "L 22,23 L 23.5,25.5 C 23.5,26.5 22,27 20.5,27 L 10,27 C 8,27 6.5,25.5 6.5,24 C 6.5,22.5 7.5,21.5 9,21.5 "
    "L 8,21 C 7,21 6.5,20 6.5,19.2 C 5.5,19.2 5,18 5.5,17 C 6.2,16 7.2,16.2 8,17 L 9,17.5 "
    "C 10.5,17.5 15,18 16.5,18.5 L 18,19 Z"
)

# Sleeping 'z' and 'Z' text / path for offline
sleep_z = """
  <!-- Sleep symbols (z Z) -->
  <path d="M 23,8 H 26 L 23.5,11 H 26.5 V 12 H 22.5 L 25,9 H 23 Z" style="fill: currentColor;" />
  <path d="M 26.5,3 H 29 L 27,5.5 H 29.5 V 6.2 H 26 L 28,4 H 26.5 Z" style="fill: currentColor;" />
"""

frames = [
    ("idle-symbolic.svg", "Ollama Alpaca: Idle", idle_body, ""),
    ("running-0-symbolic.svg", "Ollama Alpaca: Running 0", run0_body, ""),
    ("running-1-symbolic.svg", "Ollama Alpaca: Running 1", run1_body, ""),
    ("running-2-symbolic.svg", "Ollama Alpaca: Running 2", run2_body, ""),
    ("running-3-symbolic.svg", "Ollama Alpaca: Running 3", run3_body, ""),
    ("offline-symbolic.svg", "Ollama Alpaca: Sleeping / Offline", offline_body, sleep_z),
]

out_dir = "/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca"
os.makedirs(out_dir, exist_ok=True)

for fname, title, path_d, extra in frames:
    full_path = os.path.join(out_dir, fname)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(create_svg(path_d, title, extra))
    print(f"Generated: {full_path}")
