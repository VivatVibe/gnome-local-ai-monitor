import os
import xml.etree.ElementTree as ET

def create_gpu_svg(title, fan_angle, is_idle=False, is_offline=False):
    # Card shroud geometry
    # Shroud body from x=4 to x=30, y=9 to y=23
    # Left fan at (11.5, 16), Right fan at (22.5, 16)
    
    fan_blade_path = """
      <!-- 4 Aerodynamic Curved Fan Blades -->
      <path d="M 0,0 C 0.8,-1.8 2.2,-3.5 3.8,-3.8 C 4.2,-3.2 3.8,-2 2.5,-1 C 1.5,-0.2 0.8,0 0,0 Z
               M 0,0 C 1.8,0.8 3.5,2.2 3.8,3.8 C 3.2,4.2 2,3.8 1,2.5 C 0.2,1.5 0,0.8 0,0 Z
               M 0,0 C -0.8,1.8 -2.2,3.5 -3.8,3.8 C -4.2,3.2 -3.8,2 -2.5,1 C -1.5,0.2 -0.8,0 0,0 Z
               M 0,0 C -1.8,-0.8 -3.5,-2.2 -3.8,-3.8 C -3.2,-4.2 -2,-3.8 -1,-2.5 C -0.2,-1.5 0,-0.8 0,0 Z"
            fill="#ffffff" />
      <circle cx="0" cy="0" r="1.3" fill="#ffffff" stroke="#18181f" stroke-width="0.5" />
    """

    status_led = ""
    if is_offline:
        status_led = '<circle cx="28" cy="11" r="0.9" fill="#e01b24" />'
    elif is_idle:
        status_led = '<circle cx="28" cy="11" r="0.9" fill="#9a9996" />'
    else:
        status_led = '<circle cx="28" cy="11" r="0.9" fill="#33d17a" />'

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32">
  <title>{title}</title>
  
  <!-- PCIe Bracket (Silver/White) -->
  <path d="M 2,6 H 4 V 26 H 2 Z M 1,5 H 4 V 7 H 1 Z" fill="#ffffff" opacity="0.9" />
  <rect x="2.5" y="10" width="1" height="3" fill="#18181f" />
  <rect x="2.5" y="15" width="1" height="3" fill="#18181f" />

  <!-- PCIe Slot Connector Tab (Bottom) -->
  <path d="M 6,23.5 H 14 V 25.5 H 6 Z" fill="#ffffff" opacity="0.75" />
  <line x1="8" y1="24" x2="8" y2="25" stroke="#18181f" stroke-width="0.6" />
  <line x1="10" y1="24" x2="10" y2="25" stroke="#18181f" stroke-width="0.6" />
  <line x1="12" y1="24" x2="12" y2="25" stroke="#18181f" stroke-width="0.6" />

  <!-- 8-Pin Power Connector (Top) -->
  <rect x="23.5" y="7.5" width="5" height="1.8" rx="0.5" fill="#ffffff" opacity="0.8" />
  <line x1="25" y1="7.5" x2="25" y2="9" stroke="#18181f" stroke-width="0.5" />
  <line x1="27" y1="7.5" x2="27" y2="9" stroke="#18181f" stroke-width="0.5" />

  <!-- Main GPU Shroud Body -->
  <rect x="4" y="9.5" width="26.5" height="13.5" rx="1.8" fill="#18181f" stroke="#ffffff" stroke-width="1.3" />
  
  <!-- Subtle Backplate / Shroud Accent lines -->
  <line x1="5.5" y1="11" x2="29" y2="11" stroke="#ffffff" stroke-width="0.6" opacity="0.4" />
  <line x1="5.5" y1="21.5" x2="29" y2="21.5" stroke="#ffffff" stroke-width="0.6" opacity="0.4" />

  <!-- Left Fan Housing (Recessed Circular Vent) -->
  <circle cx="11.5" cy="16.2" r="4.6" fill="#101014" stroke="#ffffff" stroke-width="0.8" />
  <!-- Left Fan Blades (Rotated by {fan_angle} deg) -->
  <g transform="translate(11.5, 16.2) rotate({fan_angle})">
    {fan_blade_path}
  </g>

  <!-- Right Fan Housing (Recessed Circular Vent) -->
  <circle cx="22.5" cy="16.2" r="4.6" fill="#101014" stroke="#ffffff" stroke-width="0.8" />
  <!-- Right Fan Blades (Rotated by {fan_angle} deg) -->
  <g transform="translate(22.5, 16.2) rotate({fan_angle})">
    {fan_blade_path}
  </g>

  <!-- Status / Power LED -->
  {status_led}
</svg>
'''

out_dir = "/home/mrnv/Documents/local-ai-monitor/extension/resources/icons/gpu"
os.makedirs(out_dir, exist_ok=True)

# Generate 4 running frames (0, 22.5, 45, 67.5 degrees)
frames = [
    ("fan-0.svg", "GPU Card: Fan Rotation 0°", 0, False, False),
    ("fan-1.svg", "GPU Card: Fan Rotation 22.5°", 22.5, False, False),
    ("fan-2.svg", "GPU Card: Fan Rotation 45°", 45, False, False),
    ("fan-3.svg", "GPU Card: Fan Rotation 67.5°", 67.5, False, False),
    ("idle.svg", "GPU Card: Zero-RPM Idle", 0, True, False),
    ("offline.svg", "GPU Card: Offline", 0, False, True),
]

for fname, title, angle, is_idle, is_off in frames:
    svg_str = create_gpu_svg(title, angle, is_idle, is_off)
    ET.fromstring(svg_str)  # validate XML
    fpath = os.path.join(out_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(svg_str)
    print(f"Generated GPU SVG: {fpath}")
