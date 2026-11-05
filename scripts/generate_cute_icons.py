import os

def create_svg(title, inner_content):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 32 32" class="symbolic">
  <title>{title}</title>
  {inner_content}
</svg>
'''

# We use fill-rule="evenodd" so cutouts (eyes, snout outlines, mouth) appear cleanly in symbolic theme!
# Grid: 32 x 32

# =========================================================================
# 1. SLEEPING POSE (Official Ollama mascot sleeping, head tilted, z Z bubbles)
# =========================================================================
sleeping_svg = '''
  <!-- Cute Sleeping Alpaca Body & Tilted Head -->
  <g style="fill: currentColor; stroke: none;">
    <!-- Fluffy chubby body resting on desk/ground -->
    <path d="M 6,24 C 6,20 10,18 16,18 C 22,18 26,20 26,24 C 26,27 22,28 16,28 C 10,28 6,27 6,24 Z" />
    <!-- Little folded cute front paws -->
    <ellipse cx="13" cy="27" rx="2.5" ry="1.5" />
    <ellipse cx="19" cy="27" rx="2.5" ry="1.5" />
    <!-- Fluffy little tail -->
    <circle cx="5.5" cy="23" r="2" />
    <!-- Tilted cute chubby head -->
    <circle cx="16" cy="14" r="6" />
    <!-- Cute upright ears tilted slightly to the right -->
    <path d="M 12.5,9 C 11.5,9 11,6.5 12,5 C 13,3.5 14.5,4 14.5,6 L 14,9 Z" />
    <path d="M 17.5,9 C 16.5,9 16,6.5 17,5 C 18,3.5 19.5,4 19.5,6 L 19,9 Z" />
  </g>
  <!-- Cutout facial features (closed sleeping eyes ⌒ ⌒ and cute nose) using negative background or lines -->
  <g style="stroke: #2e3436; stroke-width: 1.2; stroke-linecap: round; fill: none;">
    <!-- Left closed sleeping eye ⌒ -->
    <path d="M 13,13.5 Q 14.5,12 16,13.5" />
    <!-- Right closed sleeping eye ⌒ -->
    <path d="M 17.5,14 Q 19,12.5 20.5,14" />
    <!-- Little cute smile/mouth -->
    <path d="M 16.5,17 Q 17.5,18 18.5,17" />
  </g>
  <!-- Floating sleep bubbles 'z' and 'Z' -->
  <g style="fill: currentColor;">
    <!-- Small z -->
    <path d="M 22,9 H 24.5 L 22.8,11.5 H 25 V 12.2 H 22 L 23.8,9.7 H 22 Z" />
    <!-- Big Z -->
    <path d="M 24.5,3.5 H 28 L 25.5,6.8 H 28.5 V 7.8 H 24.5 L 27,4.5 H 24.5 Z" />
  </g>
'''

# =========================================================================
# 2. RUNNING FRAMES 0 - 3 (Cute chubby trotting / galloping Ollama mascot)
# =========================================================================

# Frame 0: Stride A (Chubby body, front right leg forward, back left leg back, ears bouncy)
run0_svg = '''
  <g style="fill: currentColor; stroke: none;">
    <!-- Chubby body -->
    <ellipse cx="14" cy="20" rx="7.5" ry="5.5" />
    <!-- Tail -->
    <circle cx="6" cy="18.5" r="2" />
    <!-- Cute round head -->
    <circle cx="21" cy="11.5" r="5.5" />
    <!-- Chubby cute muzzle/cheeks -->
    <ellipse cx="24" cy="13" rx="2.5" ry="2" />
    <!-- Cute perky ears -->
    <path d="M 18,7 C 17,7 16.5,4.5 17.5,3 C 18.5,1.8 20,2.5 19.8,4.5 L 19.5,7 Z" />
    <path d="M 21.5,7 C 20.5,7 20,4.5 21,3 C 22,1.8 23.5,2.5 23.3,4.5 L 23,7 Z" />
    <!-- Front stubby leg 1 forward -->
    <path d="M 19,23 Q 23,24 25,27 Q 24,28 22.5,27 Q 20,25 18,24 Z" />
    <!-- Front stubby leg 2 trailing -->
    <path d="M 17,23 Q 18,25 18.5,27.5 Q 17.5,28 16.5,27.5 Q 16,25 16,23 Z" />
    <!-- Back stubby leg 1 kicking back -->
    <path d="M 9,23 Q 6,24 4,26.5 Q 4.5,27.5 5.8,27 Q 8,25 10,23 Z" />
    <!-- Back stubby leg 2 pushing down -->
    <path d="M 11,23 Q 11.5,26 12,28 Q 11,28.5 10,28 Q 9.5,26 9.5,23 Z" />
  </g>
  <!-- Cute eye dot cutout -->
  <circle cx="22.5" cy="10.5" r="1.1" style="fill: #2e3436;" />
  <circle cx="25" cy="12.5" r="0.6" style="fill: #2e3436;" />
'''

# Frame 1: Gather (Body slightly lower, legs tucked under chubby tummy)
run1_svg = '''
  <g style="fill: currentColor; stroke: none;">
    <!-- Chubby body -->
    <ellipse cx="14" cy="21" rx="7.5" ry="5.5" />
    <!-- Tail -->
    <circle cx="6" cy="19.5" r="2" />
    <!-- Cute round head -->
    <circle cx="21" cy="12.5" r="5.5" />
    <!-- Chubby cute muzzle -->
    <ellipse cx="24" cy="14" rx="2.5" ry="2" />
    <!-- Ears -->
    <path d="M 18,8 C 17,8 16.8,5.5 17.8,4 C 18.8,2.8 20.2,3.5 20,5.5 L 19.5,8 Z" />
    <path d="M 21.5,8 C 20.5,8 20.2,5.5 21.2,4 C 22.2,2.8 23.6,3.5 23.4,5.5 L 23,8 Z" />
    <!-- Front legs gathered under chest -->
    <path d="M 19,24 Q 20,26 19.5,28 Q 18.5,28 18,26.5 Q 17.5,25 17.5,24 Z" />
    <path d="M 17,24 Q 18,26 17,27.5 Q 16,27.5 15.5,26 Q 15.5,25 15.5,24 Z" />
    <!-- Back legs tucked forward under belly -->
    <path d="M 10,24 Q 12,26 13,28 Q 12,28.5 11,27.5 Q 9.5,26 9,24 Z" />
    <path d="M 8.5,24 Q 10,26 11,27.5 Q 10,28 9,27 Q 8,25.5 7.5,24 Z" />
  </g>
  <circle cx="22.5" cy="11.5" r="1.1" style="fill: #2e3436;" />
  <circle cx="25" cy="13.5" r="0.6" style="fill: #2e3436;" />
'''

# Frame 2: Stride B (Opposite front leg reaching forward, opposite back leg reaching back)
run2_svg = '''
  <g style="fill: currentColor; stroke: none;">
    <!-- Chubby body -->
    <ellipse cx="14" cy="20" rx="7.5" ry="5.5" />
    <!-- Tail -->
    <circle cx="6" cy="18.5" r="2" />
    <!-- Cute round head -->
    <circle cx="21" cy="11.5" r="5.5" />
    <!-- Chubby cute muzzle -->
    <ellipse cx="24" cy="13" rx="2.5" ry="2" />
    <!-- Ears bouncy -->
    <path d="M 18.5,7 C 17.5,7 17,4.5 18,3 C 19,1.8 20.5,2.5 20.2,4.5 L 20,7 Z" />
    <path d="M 22,7 C 21,7 20.5,4.5 21.5,3 C 22.5,1.8 24,2.5 23.7,4.5 L 23.5,7 Z" />
    <!-- Front stubby leg 2 forward -->
    <path d="M 19,23 Q 23,24 24.5,26.5 Q 23.5,27.5 22,26.5 Q 20,25 18,24 Z" />
    <!-- Front stubby leg 1 trailing -->
    <path d="M 17,23 Q 17.5,25 17,27 Q 16,27 15.5,25.5 Q 15.5,24 16,23 Z" />
    <!-- Back stubby leg 2 kicking back -->
    <path d="M 9,23 Q 6.5,24.5 4.5,27 Q 5,28 6.2,27.5 Q 8,25.5 10,23 Z" />
    <!-- Back stubby leg 1 pushing down -->
    <path d="M 11,23 Q 11.5,25.5 12.5,27.5 Q 11.5,28 10.5,27.5 Q 10,25.5 10,23 Z" />
  </g>
  <circle cx="22.5" cy="10.5" r="1.1" style="fill: #2e3436;" />
  <circle cx="25" cy="12.5" r="0.6" style="fill: #2e3436;" />
'''

# Frame 3: Airborne Leap (Chubby alpaca in mid-air hop! High cuteness!)
run3_svg = '''
  <g style="fill: currentColor; stroke: none;">
    <!-- Chubby body raised up -->
    <ellipse cx="14" cy="18" rx="7.5" ry="5.5" />
    <!-- Tail high -->
    <circle cx="5.5" cy="16" r="2" />
    <!-- Head high -->
    <circle cx="21" cy="9.5" r="5.5" />
    <!-- Chubby muzzle -->
    <ellipse cx="24" cy="11" rx="2.5" ry="2" />
    <!-- Ears perked high -->
    <path d="M 17.5,5 C 16.5,5 16,2.5 17,1 C 18,-0.2 19.5,0.5 19.2,2.5 L 19,5 Z" />
    <path d="M 21,5 C 20,5 19.5,2.5 20.5,1 C 21.5,-0.2 23,0.5 22.7,2.5 L 22.5,5 Z" />
    <!-- Front legs flying forward -->
    <path d="M 19,21 Q 24,21 26.5,23 Q 26,24.2 24.5,24 Q 21.5,22.5 18,22 Z" />
    <path d="M 17,21 Q 21,22 23,24 Q 22,25 21,24.5 Q 18.5,23 16.5,22 Z" />
    <!-- Back legs flying back -->
    <path d="M 9,21 Q 5,21.5 2.5,23.5 Q 3,24.5 4.5,24.2 Q 7.5,22.8 10,22 Z" />
    <path d="M 10.5,21 Q 7,22.5 5,24.5 Q 5.5,25.5 7,25 Q 9.5,23.5 11.5,22 Z" />
  </g>
  <circle cx="22.5" cy="8.5" r="1.1" style="fill: #2e3436;" />
  <circle cx="25" cy="10.5" r="0.6" style="fill: #2e3436;" />
'''

# Idle frame (standing cute, but when load is 0% it will sleep per user request)
idle_svg = sleeping_svg

frames = [
    ("sleeping-symbolic.svg", "Ollama Alpaca: Sleeping", sleeping_svg),
    ("offline-symbolic.svg", "Ollama Alpaca: Sleeping (Offline)", sleeping_svg),
    ("idle-symbolic.svg", "Ollama Alpaca: Sleeping (0% Load)", sleeping_svg),
    ("running-0-symbolic.svg", "Ollama Alpaca: Running 0", run0_svg),
    ("running-1-symbolic.svg", "Ollama Alpaca: Running 1", run1_svg),
    ("running-2-symbolic.svg", "Ollama Alpaca: Running 2", run2_svg),
    ("running-3-symbolic.svg", "Ollama Alpaca: Running 3", run3_svg),
]

out_dir = "/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca"
os.makedirs(out_dir, exist_ok=True)

for fname, title, content in frames:
    full_path = os.path.join(out_dir, fname)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(create_svg(title, content))
    print(f"Generated cute SVG: {full_path}")
