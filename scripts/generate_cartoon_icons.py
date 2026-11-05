import os
import xml.etree.ElementTree as ET

def wrap_svg(title, content):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32">
  <title>{title}</title>
  <defs>
    <style>
      .outline {{ stroke: #1e1e24; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
      .fill-white {{ fill: #ffffff; }}
      .detail-stroke {{ stroke: #1e1e24; stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; fill: none; }}
      .face-feature {{ fill: #1e1e24; stroke: none; }}
    </style>
  </defs>
  {content}
</svg>
'''

# =========================================================================
# 1. SLEEPING / IDLE POSE (Official Ollama mascot sleeping, head tilted, z Z)
# =========================================================================
sleeping_content = '''
  <g class="outline fill-white">
    <!-- Fluffy Body resting -->
    <path d="M 6,24 C 6,19 10,17 16,17 C 22,17 26,19 26,24 C 26,27.5 22,28.5 16,28.5 C 10,28.5 6,27.5 6,24 Z" />
    
    <!-- Folded Paws -->
    <ellipse cx="12" cy="27.5" rx="2.5" ry="1.5" />
    <ellipse cx="19" cy="27.5" rx="2.5" ry="1.5" />
    
    <!-- Puffy Tail -->
    <circle cx="5.5" cy="22.5" r="2.2" />

    <!-- Upright Ears (tilted) -->
    <path d="M 12.5,9.5 C 11.5,9.5 11,6 12,4 C 13,2.5 14.8,3.2 14.5,5.5 L 14,9.5 Z" />
    <path d="M 17.5,9.5 C 16.5,9.5 16,6 17,4 C 18,2.5 19.8,3.2 19.5,5.5 L 19,9.5 Z" />

    <!-- Chubby Head -->
    <circle cx="16" cy="14.5" r="6.2" />
    
    <!-- Muzzle oval -->
    <ellipse cx="16" cy="16.5" rx="3.2" ry="2.2" />
  </g>

  <!-- Inner Ear lines -->
  <path d="M 13,5.5 L 13.2,7.5" class="detail-stroke" />
  <path d="M 18,5.5 L 18.2,7.5" class="detail-stroke" />

  <!-- Sleeping Eyes (⌒ ⌒) and inverted Y mouth -->
  <g class="detail-stroke">
    <!-- Left sleeping eye -->
    <path d="M 12.8,13.8 Q 14.2,12.2 15.6,13.8" />
    <!-- Right sleeping eye -->
    <path d="M 16.4,13.8 Q 17.8,12.2 19.2,13.8" />
    <!-- Inverted Y nose/mouth -->
    <path d="M 16,16 L 16,17.2 M 16,17.2 L 15.2,18 M 16,17.2 L 16.8,18" />
  </g>
  <!-- Tiny nose dot -->
  <circle cx="16" cy="15.8" r="0.6" class="face-feature" />

  <!-- Cartoon Sleep Bubbles (z Z) -->
  <g class="outline fill-white">
    <!-- Small z -->
    <path d="M 22.5,8 H 25.5 L 23.2,11 H 26 V 12 H 22.2 L 24.5,9 H 22.5 Z" />
    <!-- Big Z -->
    <path d="M 24.5,2 H 28.5 L 25.8,5.5 H 29 V 6.5 H 24.5 L 27.2,3 H 24.5 Z" />
  </g>
'''

# =========================================================================
# 2. RUNNING CYCLE (4 Frames with crisp cartoon lines, white fill, cute face)
# =========================================================================

# Frame 0: Stride A (Front right foot forward, back left foot trailing)
run0_content = '''
  <g class="outline fill-white">
    <!-- Puffy Tail -->
    <circle cx="5.5" cy="18.5" r="2.2" />

    <!-- Rear Leg 2 (behind) -->
    <path d="M 9.5,21 Q 7.5,24 5.5,26.5 Q 4.8,26 6,25 Q 8.5,23.5 10.5,21 Z" />
    <!-- Front Leg 2 (behind) -->
    <path d="M 17,21 Q 18,24 18.5,27 Q 17.5,27.5 16.5,27 Q 16,24.5 16,21 Z" />

    <!-- Chubby Body -->
    <ellipse cx="14" cy="19" rx="8" ry="5.5" />

    <!-- Upright Perky Ears -->
    <path d="M 18,6.5 C 17,6.5 16.5,3.5 17.5,2 C 18.5,0.8 20,1.5 19.8,3.5 L 19.5,6.5 Z" />
    <path d="M 21.5,6.5 C 20.5,6.5 20,3.5 21,2 C 22,0.8 23.5,1.5 23.3,3.5 L 23,6.5 Z" />

    <!-- Chubby Head -->
    <circle cx="21" cy="11.5" r="5.8" />

    <!-- Muzzle -->
    <ellipse cx="24.5" cy="13" rx="2.8" ry="2" />

    <!-- Front Leg 1 (forward stride) -->
    <path d="M 19,21 Q 23,23 25.5,26.5 Q 24.5,27.5 23,26.5 Q 20,24 18,22 Z" />
    <!-- Rear Leg 1 (driving) -->
    <path d="M 11,21 Q 11.5,25 12,27.5 Q 11,28 10,27.5 Q 9.5,25 9.5,21 Z" />
  </g>

  <!-- Inner Ear lines -->
  <path d="M 18.5,3.2 L 18.8,5" class="detail-stroke" />
  <path d="M 22,3.2 L 22.3,5" class="detail-stroke" />

  <!-- Eye Dot -->
  <circle cx="22.2" cy="10.2" r="1.3" class="face-feature" />
  <!-- Eye Sparkle (white dot inside black eye) -->
  <circle cx="22.6" cy="9.8" r="0.4" fill="#ffffff" />

  <!-- Nose & Mouth on Muzzle -->
  <circle cx="25.2" cy="12.2" r="0.5" class="face-feature" />
  <path d="M 25.2,12.7 V 13.5 M 25.2,13.5 L 24.6,14.2 M 25.2,13.5 L 25.8,14.2" class="detail-stroke" />
'''

# Frame 1: Gather (Tucked legs, body slightly lowered, cute bouncy compression)
run1_content = '''
  <g class="outline fill-white">
    <!-- Puffy Tail -->
    <circle cx="5.5" cy="19.5" r="2.2" />

    <!-- Tucked Rear Leg 2 -->
    <path d="M 8.5,22 Q 10,24.5 11,26.5 Q 10,27 9,26 Q 8,24.5 7.5,22 Z" />
    <!-- Tucked Front Leg 2 -->
    <path d="M 17,22 Q 18,24.5 17,26.5 Q 16,26.5 15.5,25 Q 15.5,24 15.5,22 Z" />

    <!-- Chubby Body slightly lowered -->
    <ellipse cx="14" cy="20" rx="8" ry="5.5" />

    <!-- Ears bouncing -->
    <path d="M 18,7.5 C 17,7.5 16.5,4.5 17.5,3 C 18.5,1.8 20,2.5 19.8,4.5 L 19.5,7.5 Z" />
    <path d="M 21.5,7.5 C 20.5,7.5 20,4.5 21,3 C 22,1.8 23.5,2.5 23.3,4.5 L 23,7.5 Z" />

    <!-- Chubby Head -->
    <circle cx="21" cy="12.5" r="5.8" />

    <!-- Muzzle -->
    <ellipse cx="24.5" cy="14" rx="2.8" ry="2" />

    <!-- Front Leg 1 tucked under chest -->
    <path d="M 19,22 Q 20,24.5 19.5,27 Q 18.5,27 18,25.5 Q 17.5,24 17.5,22 Z" />
    <!-- Rear Leg 1 tucked under belly -->
    <path d="M 10,22 Q 12,24.5 13,27 Q 12,27.5 11,26.5 Q 9.5,24.5 9,22 Z" />
  </g>

  <!-- Inner Ear lines -->
  <path d="M 18.5,4.2 L 18.8,6" class="detail-stroke" />
  <path d="M 22,4.2 L 22.3,6" class="detail-stroke" />

  <!-- Eye Dot -->
  <circle cx="22.2" cy="11.2" r="1.3" class="face-feature" />
  <circle cx="22.6" cy="10.8" r="0.4" fill="#ffffff" />

  <!-- Nose & Mouth -->
  <circle cx="25.2" cy="13.2" r="0.5" class="face-feature" />
  <path d="M 25.2,13.7 V 14.5 M 25.2,14.5 L 24.6,15.2 M 25.2,14.5 L 25.8,15.2" class="detail-stroke" />
'''

# Frame 2: Stride B (Opposite front leg forward, opposite back leg trailing)
run2_content = '''
  <g class="outline fill-white">
    <!-- Puffy Tail -->
    <circle cx="5.5" cy="18.5" r="2.2" />

    <!-- Rear Leg 1 (trailing) -->
    <path d="M 11,21 Q 11.5,24.5 12.5,27 Q 11.5,27.5 10.5,27 Q 10,24.5 10,21 Z" />
    <!-- Front Leg 1 (trailing) -->
    <path d="M 17,21 Q 17.5,24 17,26 Q 16,26 15.5,24.5 Q 15.5,23 16,21 Z" />

    <!-- Chubby Body -->
    <ellipse cx="14" cy="19" rx="8" ry="5.5" />

    <!-- Ears -->
    <path d="M 18.5,6.5 C 17.5,6.5 17,3.5 18,2 C 19,0.8 20.5,1.5 20.2,3.5 L 20,6.5 Z" />
    <path d="M 22,6.5 C 21,6.5 20.5,3.5 21.5,2 C 22.5,0.8 24,1.5 23.7,3.5 L 23.5,6.5 Z" />

    <!-- Chubby Head -->
    <circle cx="21" cy="11.5" r="5.8" />

    <!-- Muzzle -->
    <ellipse cx="24.5" cy="13" rx="2.8" ry="2" />

    <!-- Front Leg 2 (forward reach) -->
    <path d="M 19,21 Q 23,23 24.5,26 Q 23.5,27 22,26 Q 20,24 18,22 Z" />
    <!-- Rear Leg 2 (kicking back) -->
    <path d="M 9,21 Q 6.5,23.5 4.5,26 Q 5,27 6.2,26.5 Q 8,24 10,21 Z" />
  </g>

  <!-- Inner Ear lines -->
  <path d="M 19,3.2 L 19.3,5" class="detail-stroke" />
  <path d="M 22.5,3.2 L 22.8,5" class="detail-stroke" />

  <!-- Eye Dot -->
  <circle cx="22.2" cy="10.2" r="1.3" class="face-feature" />
  <circle cx="22.6" cy="9.8" r="0.4" fill="#ffffff" />

  <!-- Nose & Mouth -->
  <circle cx="25.2" cy="12.2" r="0.5" class="face-feature" />
  <path d="M 25.2,12.7 V 13.5 M 25.2,13.5 L 24.6,14.2 M 25.2,13.5 L 25.8,14.2" class="detail-stroke" />
'''

# Frame 3: Airborne Hop (All 4 paws airborne, ears perky high, ultimate cuteness)
run3_content = '''
  <g class="outline fill-white">
    <!-- Puffy Tail high -->
    <circle cx="5.5" cy="16.5" r="2.2" />

    <!-- Rear Flying Leg 2 -->
    <path d="M 10.5,19 Q 7,20.5 5,22.5 Q 5.5,23.5 7,23 Q 9.5,21.5 11.5,19 Z" />
    <!-- Front Flying Leg 2 -->
    <path d="M 17,19 Q 21,20 23,22 Q 22,23 21,22.5 Q 18.5,21 16.5,19 Z" />

    <!-- Chubby Body raised up -->
    <ellipse cx="14" cy="17" rx="8" ry="5.5" />

    <!-- Ears flying high -->
    <path d="M 17.5,4.5 C 16.5,4.5 16,1.5 17,0 C 18,-1 19.5,0 19.2,2 L 19,4.5 Z" />
    <path d="M 21,4.5 C 20,4.5 19.5,1.5 20.5,0 C 21.5,-1 23,0 22.7,2 L 22.5,4.5 Z" />

    <!-- Chubby Head high -->
    <circle cx="21" cy="9.5" r="5.8" />

    <!-- Muzzle -->
    <ellipse cx="24.5" cy="11" rx="2.8" ry="2" />

    <!-- Front Flying Leg 1 (extended forward) -->
    <path d="M 19,19 Q 24,19 26.5,21 Q 26,22.2 24.5,22 Q 21.5,20.5 18,20 Z" />
    <!-- Rear Flying Leg 1 (extended back) -->
    <path d="M 9,19 Q 5,19.5 2.5,21.5 Q 3,22.5 4.5,22 Q 7.5,20.8 10,20 Z" />
  </g>

  <!-- Inner Ear lines -->
  <path d="M 18,1.2 L 18.3,3" class="detail-stroke" />
  <path d="M 21.5,1.2 L 21.8,3" class="detail-stroke" />

  <!-- Eye Dot -->
  <circle cx="22.2" cy="8.2" r="1.3" class="face-feature" />
  <circle cx="22.6" cy="7.8" r="0.4" fill="#ffffff" />

  <!-- Nose & Mouth -->
  <circle cx="25.2" cy="10.2" r="0.5" class="face-feature" />
  <path d="M 25.2,10.7 V 11.5 M 25.2,11.5 L 24.6,12.2 M 25.2,11.5 L 25.8,12.2" class="detail-stroke" />
'''

frames = [
    ("sleeping-symbolic.svg", "Ollama Alpaca: Sleeping (Cartoon Line-Art)", sleeping_content),
    ("idle-symbolic.svg", "Ollama Alpaca: Idle / 0% Load (Cartoon Line-Art)", sleeping_content),
    ("offline-symbolic.svg", "Ollama Alpaca: Offline (Cartoon Line-Art)", sleeping_content),
    ("running-0-symbolic.svg", "Ollama Alpaca: Running 0 (Cartoon Line-Art)", run0_content),
    ("running-1-symbolic.svg", "Ollama Alpaca: Running 1 (Cartoon Line-Art)", run1_content),
    ("running-2-symbolic.svg", "Ollama Alpaca: Running 2 (Cartoon Line-Art)", run2_content),
    ("running-3-symbolic.svg", "Ollama Alpaca: Running 3 (Cartoon Line-Art)", run3_content),
]

icons_dir = "/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/alpaca"
os.makedirs(icons_dir, exist_ok=True)

for fname, title, content in frames:
    full_svg = wrap_svg(title, content)
    # Validate XML before writing
    ET.fromstring(full_svg)
    target_path = os.path.join(icons_dir, fname)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"Generated and validated XML: {target_path}")
