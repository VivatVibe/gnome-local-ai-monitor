import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ollama Alpaca Mascot Animation Arena - 10 Candidate Gallery</title>
  <style>
    :root {
      --bg-dark: #1e1e24;
      --card-bg: #2b2b36;
      --card-hover: #353542;
      --panel-bg: #101014;
      --accent-color: #6366f1;
      --accent-hover: #4f46e5;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --alpaca-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      padding: 24px;
      line-height: 1.5;
    }

    header {
      max-width: 1200px;
      margin: 0 auto 28px;
    }

    h1 {
      font-size: 26px;
      font-weight: 700;
      margin-bottom: 6px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    p.subtitle {
      color: var(--text-muted);
      font-size: 14px;
    }

    /* Live Top Bar Simulator */
    .simulator-container {
      max-width: 1200px;
      margin: 0 auto 32px;
      background: #18181f;
      border: 1px solid #3f3f4e;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }

    .sim-header {
      padding: 12px 18px;
      background: #23232c;
      border-bottom: 1px solid #3f3f4e;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .gnome-topbar {
      height: 36px;
      background-color: var(--panel-bg);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 16px;
      font-size: 13px;
      font-weight: 500;
      color: #e5e7eb;
      user-select: none;
    }

    .topbar-left, .topbar-center, .topbar-right {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .live-indicator-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.08);
      padding: 3px 10px;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      cursor: pointer;
      transition: background 0.2s;
    }

    .live-indicator-pill:hover {
      background: rgba(255, 255, 255, 0.16);
    }

    .live-indicator-pill svg {
      width: 24px;
      height: 24px;
    }

    .live-badge-text {
      font-weight: 700;
      font-size: 12px;
      color: #ffffff;
      min-width: 28px;
    }

    /* Interactive Controls */
    .controls-panel {
      max-width: 1200px;
      margin: 0 auto 32px;
      background: #23232c;
      padding: 18px 24px;
      border-radius: 10px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 28px;
      border: 1px solid #373748;
    }

    .control-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .control-group label {
      font-size: 14px;
      font-weight: 600;
    }

    input[type=range] {
      width: 220px;
      accent-color: var(--accent-color);
      cursor: pointer;
    }

    .load-val {
      font-weight: 700;
      font-size: 15px;
      color: #60a5fa;
      min-width: 45px;
    }

    .state-badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      background: #374151;
      color: #e5e7eb;
    }

    .state-badge.sleeping {
      background: #1e3a8a;
      color: #93c5fd;
    }

    .state-badge.running {
      background: #065f46;
      color: #6ee7b7;
    }

    /* Candidates Grid */
    .grid {
      max-width: 1200px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 20px;
    }

    .candidate-card {
      background: var(--card-bg);
      border: 2px solid transparent;
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      cursor: pointer;
    }

    .candidate-card:hover {
      background: var(--card-hover);
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(0,0,0,0.3);
    }

    .candidate-card.selected {
      border-color: var(--accent-color);
      background: #303040;
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.35);
    }

    .cand-num {
      position: absolute;
      top: 12px;
      left: 14px;
      font-size: 12px;
      font-weight: 700;
      background: #1f1f28;
      padding: 2px 8px;
      border-radius: 10px;
      color: #9ca3af;
    }

    .cand-preview-box {
      width: 90px;
      height: 90px;
      background: #121217;
      border: 1px solid #3f3f50;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 16px 0 14px;
      position: relative;
    }

    .cand-preview-box svg {
      width: 48px;
      height: 48px;
      transition: transform 0.2s;
    }

    .cand-title {
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 6px;
      color: #fff;
    }

    .cand-desc {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 14px;
      min-height: 38px;
    }

    .cand-select-btn {
      width: 100%;
      padding: 8px 14px;
      border-radius: 8px;
      border: none;
      font-size: 13px;
      font-weight: 600;
      background: #3e3e52;
      color: #fff;
      cursor: pointer;
      transition: background 0.2s;
    }

    .candidate-card.selected .cand-select-btn {
      background: var(--accent-color);
    }

    .candidate-card:hover .cand-select-btn {
      background: var(--accent-hover);
    }
  </style>
</head>
<body>

  <header>
    <h1>🦙 Ollama Alpaca Mascot Animation Arena</h1>
    <p class="subtitle">10 competing high-contrast pure white (#FFFFFF) candidates in 24px GNOME top panel proportions. Move the load slider to test sleeping and galloping dynamics.</p>
  </header>

  <!-- Live GNOME Top Bar Simulator -->
  <div class="simulator-container">
    <div class="sim-header">
      <span>🖥️ Live GNOME Shell Top Bar Simulation (Scale: 24px)</span>
      <span id="activeModelLabel">Active Selection: #1 Official Ollama 3/4</span>
    </div>
    <div class="gnome-topbar">
      <div class="topbar-left">
        <span>Activities</span>
        <span>Files</span>
        <span>Terminal</span>
      </div>
      <div class="topbar-center">
        <span>Thu Nov 5 22:45</span>
      </div>
      <div class="topbar-right">
        <!-- Live Extension Pill -->
        <div class="live-indicator-pill" id="simPill" title="Local AI Monitor Indicator">
          <div id="simIconSlot"></div>
          <span class="live-badge-text" id="simBadge">0%</span>
        </div>
        <span>📶</span>
        <span>🔊</span>
        <span>🔋 95%</span>
      </div>
    </div>
  </div>

  <!-- Interactive Controls -->
  <div class="controls-panel">
    <div class="control-group">
      <label for="loadSlider">GPU / AI Load Simulation:</label>
      <input type="range" id="loadSlider" min="0" max="100" value="0">
      <span class="load-val" id="loadDisplay">0%</span>
    </div>
    <div class="control-group">
      <span class="state-badge sleeping" id="stateBadge">💤 Sleeping (0% Load)</span>
    </div>
    <div class="control-group">
      <span style="font-size: 13px; color: #9ca3af;">Animation Frame Interval: <strong id="intervalDisplay" style="color:#fff;">--</strong></span>
    </div>
  </div>

  <!-- 10 Candidates Grid -->
  <div class="grid" id="candidatesGrid"></div>

  <script>
    // 10 Distinct Candidate SVG Definitions
    // Each candidate has:
    // - sleeping: SVG inner markup for sleeping with z Z bubbles
    // - running: Array of 4 SVG inner markups for gallop frames
    const CANDIDATES = [
      {
        id: 1,
        title: "1. Official Ollama 3/4",
        desc: "Faithful to official logo proportions. Round chubby head, curved snout, upright bunny ears, dark eye contrast.",
        sleeping: `
          <g fill="#ffffff">
            <ellipse cx="14" cy="22" rx="9" ry="6"/>
            <circle cx="5" cy="20" r="2.5"/>
            <circle cx="21" cy="14" r="6"/>
            <ellipse cx="24.5" cy="15.5" rx="3" ry="2.2"/>
            <path d="M18,9 C17,9 16.5,6 17.5,4 C18.5,2.5 20,3 19.8,5.5 L19.5,9 Z"/>
            <path d="M21.5,9 C20.5,9 20,6 21,4 C22,2.5 23.5,3 23.3,5.5 L23,9 Z"/>
          </g>
          <!-- Closed eye and smile -->
          <path d="M19,13.5 Q20.5,12 22,13.5" stroke="#101014" stroke-width="1.2" stroke-linecap="round" fill="none"/>
          <circle cx="25" cy="15" r="0.8" fill="#101014"/>
          <!-- z Z bubbles -->
          <g fill="#ffffff">
            <path d="M25,8 H27 L25.5,10.5 H27.5 V11.2 H25 L26.5,9 H25 Z"/>
            <path d="M27.5,2.5 H30.5 L28,6 H31 V6.8 H27.5 L30,3.3 H27.5 Z"/>
          </g>
        `,
        running: [
          // Frame 0
          `<g fill="#ffffff">
            <ellipse cx="14" cy="19" rx="8" ry="5.5"/>
            <circle cx="5.5" cy="17.5" r="2.2"/>
            <circle cx="21" cy="11.5" r="5.8"/>
            <ellipse cx="24.5" cy="13" rx="2.8" ry="2"/>
            <path d="M18,6.5 C17,6.5 16.5,3.5 17.5,2 C18.5,0.8 20,1.5 19.8,3.5 L19.5,6.5 Z"/>
            <path d="M21.5,6.5 C20.5,6.5 20,3.5 21,2 C22,0.8 23.5,1.5 23.3,3.5 L23,6.5 Z"/>
            <path d="M19,22 Q23,23 25,27 Q24,28 22.5,27 Q20,24.5 18,23 Z"/>
            <path d="M17,22 Q18,24 18.5,27 Q17.5,27.5 16.5,27 Q16,24.5 16,22 Z"/>
            <path d="M9,22 Q6,23 3.5,26 Q4,27 5.5,26.5 Q8,24.5 10,22 Z"/>
            <path d="M11,22 Q11.5,25 12,27.5 Q11,28 10,27.5 Q9.5,25 9.5,22 Z"/>
          </g>
          <circle cx="22.5" cy="10" r="1.2" fill="#101014"/>
          <circle cx="25" cy="12.5" r="0.7" fill="#101014"/>`,
          // Frame 1
          `<g fill="#ffffff">
            <ellipse cx="14" cy="20" rx="8" ry="5.5"/>
            <circle cx="5.5" cy="18.5" r="2.2"/>
            <circle cx="21" cy="12.5" r="5.8"/>
            <ellipse cx="24.5" cy="14" rx="2.8" ry="2"/>
            <path d="M18,7.5 C17,7.5 16.5,4.5 17.5,3 C18.5,1.8 20,2.5 19.8,4.5 L19.5,7.5 Z"/>
            <path d="M21.5,7.5 C20.5,7.5 20,4.5 21,3 C22,1.8 23.5,2.5 23.3,4.5 L23,7.5 Z"/>
            <path d="M19,23 Q20,25 19.5,27.5 Q18.5,27.5 18,26 Q17.5,24.5 17.5,23 Z"/>
            <path d="M17,23 Q18,25 17,27 Q16,27 15.5,25.5 Q15.5,24 15.5,23 Z"/>
            <path d="M10,23 Q12,25 13,27.5 Q12,28 11,27 Q9.5,25 9,23 Z"/>
            <path d="M8.5,23 Q10,25 11,27 Q10,27.5 9,26.5 Q8,25 7.5,23 Z"/>
          </g>
          <circle cx="22.5" cy="11" r="1.2" fill="#101014"/>
          <circle cx="25" cy="13.5" r="0.7" fill="#101014"/>`,
          // Frame 2
          `<g fill="#ffffff">
            <ellipse cx="14" cy="19" rx="8" ry="5.5"/>
            <circle cx="5.5" cy="17.5" r="2.2"/>
            <circle cx="21" cy="11.5" r="5.8"/>
            <ellipse cx="24.5" cy="13" rx="2.8" ry="2"/>
            <path d="M18.5,6.5 C17.5,6.5 17,3.5 18,2 C19,0.8 20.5,1.5 20.2,3.5 L20,6.5 Z"/>
            <path d="M22,6.5 C21,6.5 20.5,3.5 21.5,2 C22.5,0.8 24,1.5 23.7,3.5 L23.5,6.5 Z"/>
            <path d="M19,22 Q23,23 24.5,26 Q23.5,27 22,26 Q20,24.5 18,23 Z"/>
            <path d="M17,22 Q17.5,24 17,26.5 Q16,26.5 15.5,25 Q15.5,23.5 16,22 Z"/>
            <path d="M9,22 Q6.5,23.5 4.5,26.5 Q5,27.5 6.2,27 Q8,24.5 10,22 Z"/>
            <path d="M11,22 Q11.5,24.5 12.5,27 Q11.5,27.5 10.5,27 Q10,24.5 10,22 Z"/>
          </g>
          <circle cx="22.5" cy="10" r="1.2" fill="#101014"/>
          <circle cx="25" cy="12.5" r="0.7" fill="#101014"/>`,
          // Frame 3
          `<g fill="#ffffff">
            <ellipse cx="14" cy="17" rx="8" ry="5.5"/>
            <circle cx="5.5" cy="15.5" r="2.2"/>
            <circle cx="21" cy="9.5" r="5.8"/>
            <ellipse cx="24.5" cy="11" rx="2.8" ry="2"/>
            <path d="M17.5,4.5 C16.5,4.5 16,1.5 17,0 C18,-1 19.5,0 19.2,2 L19,4.5 Z"/>
            <path d="M21,4.5 C20,4.5 19.5,1.5 20.5,0 C21.5,-1 23,0 22.7,2 L22.5,4.5 Z"/>
            <path d="M19,20 Q24,20 26.5,22 Q26,23.2 24.5,23 Q21.5,21.5 18,21 Z"/>
            <path d="M17,20 Q21,21 23,23 Q22,24 21,23.5 Q18.5,22 16.5,21 Z"/>
            <path d="M9,20 Q5,20.5 2.5,22.5 Q3,23.5 4.5,23 Q7.5,21.8 10,21 Z"/>
            <path d="M10.5,20 Q7,21.5 5,23.5 Q5.5,24.5 7,24 Q9.5,22.5 11.5,21 Z"/>
          </g>
          <circle cx="22.5" cy="8" r="1.2" fill="#101014"/>
          <circle cx="25" cy="10.5" r="0.7" fill="#101014"/>`
        ]
      },

      {
        id: 2,
        title: "2. Chibi Marshmallow",
        desc: "Oversized round head with chubby cheek squish and bouncy little bunny ears. Ultra-cute aesthetic.",
        sleeping: `
          <g fill="#ffffff">
            <circle cx="15" cy="22" r="8"/>
            <circle cx="18" cy="13" r="7.5"/>
            <ellipse cx="22" cy="15" rx="3.5" ry="2.5"/>
            <path d="M14,6 C13,6 12,3 13.5,1.5 C15,0.5 16.5,2 16,4.5 L15.5,7 Z"/>
            <path d="M18.5,6 C17.5,6 16.5,3 18,1.5 C19.5,0.5 21,2 20.5,4.5 L20,7 Z"/>
          </g>
          <path d="M16.5,13 Q18,11.5 19.5,13" stroke="#101014" stroke-width="1.3" stroke-linecap="round" fill="none"/>
          <ellipse cx="14" cy="27" rx="3" ry="1.5" fill="#ffffff"/>
          <path d="M23,6 H25.5 L23.5,9 H26 V9.8 H23 L25,7 H23 Z" fill="#ffffff"/>
          <path d="M26,1.5 H29 L26.5,5 H29.5 V5.8 H26 L28.5,2.5 H26 Z" fill="#ffffff"/>
        `,
        running: [
          `<g fill="#ffffff">
            <circle cx="13" cy="19" r="7.5"/>
            <circle cx="19" cy="12" r="7.2"/>
            <ellipse cx="23" cy="14" rx="3.5" ry="2.5"/>
            <path d="M15,5 C14,5 13,2 14.5,0.5 C16,-0.5 17.5,1 17,3.5 L16.5,6 Z"/>
            <path d="M19.5,5 C18.5,5 17.5,2 19,0.5 C20.5,-0.5 22,1 21.5,3.5 L21,6 Z"/>
            <ellipse cx="21" cy="25" rx="2.5" ry="1.8" transform="rotate(25 21 25)"/>
            <ellipse cx="6" cy="24" rx="2.5" ry="1.8" transform="rotate(-30 6 24)"/>
          </g>
          <circle cx="19.5" cy="11.5" r="1.4" fill="#101014"/>`,
          `<g fill="#ffffff">
            <circle cx="13" cy="20" r="7.5"/>
            <circle cx="19" cy="13" r="7.2"/>
            <ellipse cx="23" cy="15" rx="3.5" ry="2.5"/>
            <path d="M15,6 C14,6 13,3 14.5,1.5 C16,0.5 17.5,2 17,4.5 L16.5,7 Z"/>
            <path d="M19.5,6 C18.5,6 17.5,3 19,1.5 C20.5,0.5 22,2 21.5,4.5 L21,7 Z"/>
            <ellipse cx="17" cy="26" rx="2.2" ry="1.8"/>
            <ellipse cx="10" cy="26" rx="2.2" ry="1.8"/>
          </g>
          <circle cx="19.5" cy="12.5" r="1.4" fill="#101014"/>`,
          `<g fill="#ffffff">
            <circle cx="13" cy="19" r="7.5"/>
            <circle cx="19" cy="12" r="7.2"/>
            <ellipse cx="23" cy="14" rx="3.5" ry="2.5"/>
            <path d="M15,5 C14,5 13,2 14.5,0.5 C16,-0.5 17.5,1 17,3.5 L16.5,6 Z"/>
            <path d="M19.5,5 C18.5,5 17.5,2 19,0.5 C20.5,-0.5 22,1 21.5,3.5 L21,6 Z"/>
            <ellipse cx="19" cy="25" rx="2.5" ry="1.8" transform="rotate(-20 19 25)"/>
            <ellipse cx="8" cy="25" rx="2.5" ry="1.8" transform="rotate(35 8 25)"/>
          </g>
          <circle cx="19.5" cy="11.5" r="1.4" fill="#101014"/>`,
          `<g fill="#ffffff">
            <circle cx="13" cy="17" r="7.5"/>
            <circle cx="19" cy="10" r="7.2"/>
            <ellipse cx="23" cy="12" rx="3.5" ry="2.5"/>
            <path d="M14,3 C13,3 12,0 13.5,-1.5 C15,-2.5 16.5,-1 16,1.5 L15.5,4 Z"/>
            <path d="M18.5,3 C17.5,3 16.5,0 18,-1.5 C19.5,-2.5 21,-1 20.5,1.5 L20,4 Z"/>
            <ellipse cx="22" cy="22" rx="2.5" ry="1.5" transform="rotate(15 22 22)"/>
            <ellipse cx="5" cy="22" rx="2.5" ry="1.5" transform="rotate(-15 5 22)"/>
          </g>
          <circle cx="19.5" cy="9.5" r="1.4" fill="#101014"/>`
        ]
      },

      {
        id: 3,
        title: "3. Fluffy Cloud Alpaca",
        desc: "Cloud-like scalloped fleece puffs forming the torso and mane. Instantly distinct from non-alpaca animals.",
        sleeping: `
          <g fill="#ffffff">
            <circle cx="10" cy="22" r="5"/><circle cx="16" cy="22" r="6"/><circle cx="22" cy="22" r="5"/>
            <circle cx="13" cy="17" r="5"/><circle cx="19" cy="17" r="5.5"/>
            <circle cx="21" cy="12" r="4.5"/>
            <path d="M19,6 C18,6 17.5,3 18.5,1.5 C19.5,0.5 21,1 20.8,3.5 Z"/>
            <path d="M22,6 C21,6 20.5,3 21.5,1.5 C22.5,0.5 24,1 23.8,3.5 Z"/>
          </g>
          <path d="M19,12 Q20.5,10.5 22,12" stroke="#101014" stroke-width="1.2" stroke-linecap="round" fill="none"/>
          <g fill="#ffffff"><path d="M24,7 H26 L24.5,9.5 H26.5 V10.2 H24 Z"/></g>
        `,
        running: [
          `<g fill="#ffffff">
            <circle cx="8" cy="19" r="4.5"/><circle cx="14" cy="19" r="5.5"/><circle cx="19" cy="18" r="5"/>
            <circle cx="13" cy="14" r="4.5"/><circle cx="18" cy="13" r="5"/>
            <circle cx="21" cy="9" r="4.2"/>
            <path d="M19,4 L19,1 L21,2 Z"/><path d="M22,4 L22,1 L24,2 Z"/>
            <path d="M18,22 L24,26 L22,27 L17,23 Z"/>
            <path d="M10,22 L5,26 L3,25 L8,22 Z"/>
          </g><circle cx="21" cy="8.5" r="1.1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <circle cx="8" cy="20" r="4.5"/><circle cx="14" cy="20" r="5.5"/><circle cx="19" cy="19" r="5"/>
            <circle cx="13" cy="15" r="4.5"/><circle cx="18" cy="14" r="5"/>
            <circle cx="21" cy="10" r="4.2"/>
            <path d="M19,5 L19,2 L21,3 Z"/><path d="M22,5 L22,2 L24,3 Z"/>
            <path d="M17,23 L19,27 L17,27.5 L15,24 Z"/>
            <path d="M11,23 L13,27 L11,27.5 L9,24 Z"/>
          </g><circle cx="21" cy="9.5" r="1.1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <circle cx="8" cy="19" r="4.5"/><circle cx="14" cy="19" r="5.5"/><circle cx="19" cy="18" r="5"/>
            <circle cx="13" cy="14" r="4.5"/><circle cx="18" cy="13" r="5"/>
            <circle cx="21" cy="9" r="4.2"/>
            <path d="M19,4 L19,1 L21,2 Z"/><path d="M22,4 L22,1 L24,2 Z"/>
            <path d="M17,22 L21,26 L19,27 L16,23 Z"/>
            <path d="M9,22 L5,26 L4,25 L8,22 Z"/>
          </g><circle cx="21" cy="8.5" r="1.1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <circle cx="8" cy="17" r="4.5"/><circle cx="14" cy="17" r="5.5"/><circle cx="19" cy="16" r="5"/>
            <circle cx="13" cy="12" r="4.5"/><circle cx="18" cy="11" r="5"/>
            <circle cx="21" cy="7" r="4.2"/>
            <path d="M19,2 L19,-1 L21,0 Z"/><path d="M22,2 L22,-1 L24,0 Z"/>
            <path d="M18,20 L25,22 L24,23 L17,21 Z"/>
            <path d="M8,20 L2,22 L3,23 L9,21 Z"/>
          </g><circle cx="21" cy="6.5" r="1.1" fill="#101014"/>`
        ]
      },

      {
        id: 4,
        title: "4. Classic Side Galloper",
        desc: "High upright neck and elongated athletic strides. Emphasizes the regal llama neck silhouette.",
        sleeping: `
          <g fill="#ffffff">
            <ellipse cx="14" cy="23" rx="9" ry="5"/>
            <path d="M18,21 L19,14 L23,14 L24,21 Z"/>
            <circle cx="21" cy="12" r="4.5"/>
            <path d="M19,8 L19,4 L21,5 Z"/><path d="M22,8 L22,4 L24,5 Z"/>
          </g>
          <path d="M20,12 Q21.5,10.5 23,12" stroke="#101014" stroke-width="1.2" fill="none"/>
          <g fill="#ffffff"><path d="M25,6 H27.5 L25.5,8.5 H28 V9.2 H25 Z"/></g>
        `,
        running: [
          `<g fill="#ffffff">
            <ellipse cx="14" cy="19" rx="8" ry="4.5"/>
            <path d="M17,17 L19,9 L23,9 L21,17 Z"/>
            <circle cx="21" cy="7.5" r="4.2"/>
            <path d="M19,4 L19,1 L21,2 Z"/><path d="M22,4 L22,1 L24,2 Z"/>
            <path d="M18,21 L26,26 L24,27 L17,22 Z"/>
            <path d="M10,21 L3,26 L2,25 L9,21 Z"/>
          </g><circle cx="22" cy="6.5" r="1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="20" rx="8" ry="4.5"/>
            <path d="M17,18 L19,10 L23,10 L21,18 Z"/>
            <circle cx="21" cy="8.5" r="4.2"/>
            <path d="M19,5 L19,2 L21,3 Z"/><path d="M22,5 L22,2 L24,3 Z"/>
            <path d="M18,22 L19,27 L17,27.5 L16,23 Z"/>
            <path d="M10,22 L12,27 L10,27.5 L8,23 Z"/>
          </g><circle cx="22" cy="7.5" r="1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="19" rx="8" ry="4.5"/>
            <path d="M17,17 L19,9 L23,9 L21,17 Z"/>
            <circle cx="21" cy="7.5" r="4.2"/>
            <path d="M19,4 L19,1 L21,2 Z"/><path d="M22,4 L22,1 L24,2 Z"/>
            <path d="M18,21 L23,26 L21,27 L16,22 Z"/>
            <path d="M10,21 L5,26 L4,25 L9,21 Z"/>
          </g><circle cx="22" cy="6.5" r="1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="17" rx="8" ry="4.5"/>
            <path d="M17,15 L19,7 L23,7 L21,15 Z"/>
            <circle cx="21" cy="5.5" r="4.2"/>
            <path d="M19,2 L19,-1 L21,0 Z"/><path d="M22,2 L22,-1 L24,0 Z"/>
            <path d="M18,19 L27,21 L26,22 L17,20 Z"/>
            <path d="M9,19 L1,21 L2,22 L10,20 Z"/>
          </g><circle cx="22" cy="4.5" r="1" fill="#101014"/>`
        ]
      },

      {
        id: 5,
        title: "5. Bold Solid Glyph",
        desc: "Thick, high-contrast silhouette with deep dark cutouts. Designed for razor-sharp readability on 4K HiDPI screens.",
        sleeping: `
          <g fill="#ffffff">
            <path d="M6,21 C6,18 10,16 16,16 C22,16 26,18 26,21 C26,25 21,27 16,27 C11,27 6,25 6,21 Z"/>
            <circle cx="21" cy="13" r="5.5"/>
            <path d="M19,8 L19,4 L21,5 Z"/><path d="M22,8 L22,4 L24,5 Z"/>
          </g>
          <line x1="19" y1="13" x2="23" y2="13" stroke="#101014" stroke-width="1.8" stroke-linecap="round"/>
          <g fill="#ffffff"><path d="M25,6 H28 L26,8.5 H28.5 V9.5 H25 Z"/></g>
        `,
        running: [
          `<g fill="#ffffff">
            <path d="M7,17 C7,15 11,14 17,14 C21,14 24,15 25,18 L27,26 L24,26 L22,19 L12,19 L10,26 L7,26 Z"/>
            <circle cx="21" cy="10" r="5"/>
            <path d="M19,6 L19,2 L21,3 Z"/><path d="M22,6 L22,2 L24,3 Z"/>
          </g><circle cx="22.5" cy="9" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <path d="M7,18 C7,16 11,15 17,15 C21,15 24,16 25,19 L21,26 L19,26 L19,20 L13,20 L13,26 L11,26 Z"/>
            <circle cx="21" cy="11" r="5"/>
            <path d="M19,7 L19,3 L21,4 Z"/><path d="M22,7 L22,3 L24,4 Z"/>
          </g><circle cx="22.5" cy="10" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <path d="M7,17 C7,15 11,14 17,14 C21,14 24,15 25,18 L25,26 L22,26 L20,19 L12,19 L8,26 L5,26 Z"/>
            <circle cx="21" cy="10" r="5"/>
            <path d="M19,6 L19,2 L21,3 Z"/><path d="M22,6 L22,2 L24,3 Z"/>
          </g><circle cx="22.5" cy="9" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <path d="M7,15 C7,13 11,12 17,12 C21,12 24,13 25,16 L28,22 L25,23 L22,17 L12,17 L6,23 L3,22 Z"/>
            <circle cx="21" cy="8" r="5"/>
            <path d="M19,4 L19,0 L21,1 Z"/><path d="M22,4 L22,0 L24,1 Z"/>
          </g><circle cx="22.5" cy="7" r="1.3" fill="#101014"/>`
        ]
      },

      {
        id: 6,
        title: "6. Pixel-Art Retro Alpaca",
        desc: "Chunky 8-bit / 16-bit pixel block style. Perfect retro match for users coming from RunCat.",
        sleeping: `
          <g fill="#ffffff">
            <rect x="8" y="18" width="16" height="8"/>
            <rect x="18" y="10" width="8" height="8"/>
            <rect x="19" y="5" width="2" height="5"/>
            <rect x="23" y="5" width="2" height="5"/>
          </g>
          <rect x="21" y="13" width="3" height="2" fill="#101014"/>
          <g fill="#ffffff">
            <rect x="26" y="6" width="3" height="1"/>
            <rect x="27" y="7" width="2" height="1"/>
            <rect x="26" y="8" width="3" height="1"/>
          </g>
        `,
        running: [
          `<g fill="#ffffff">
            <rect x="8" y="14" width="14" height="8"/>
            <rect x="18" y="6" width="8" height="8"/>
            <rect x="19" y="1" width="2" height="5"/>
            <rect x="23" y="1" width="2" height="5"/>
            <rect x="20" y="22" width="4" height="6"/>
            <rect x="6" y="22" width="4" height="5"/>
          </g><rect x="22" y="9" width="2" height="2" fill="#101014"/>`,
          `<g fill="#ffffff">
            <rect x="8" y="15" width="14" height="8"/>
            <rect x="18" y="7" width="8" height="8"/>
            <rect x="19" y="2" width="2" height="5"/>
            <rect x="23" y="2" width="2" height="5"/>
            <rect x="16" y="23" width="3" height="5"/>
            <rect x="11" y="23" width="3" height="5"/>
          </g><rect x="22" y="10" width="2" height="2" fill="#101014"/>`,
          `<g fill="#ffffff">
            <rect x="8" y="14" width="14" height="8"/>
            <rect x="18" y="6" width="8" height="8"/>
            <rect x="19" y="1" width="2" height="5"/>
            <rect x="23" y="1" width="2" height="5"/>
            <rect x="18" y="22" width="4" height="5"/>
            <rect x="8" y="22" width="4" height="6"/>
          </g><rect x="22" y="9" width="2" height="2" fill="#101014"/>`,
          `<g fill="#ffffff">
            <rect x="8" y="12" width="14" height="8"/>
            <rect x="18" y="4" width="8" height="8"/>
            <rect x="19" y="-1" width="2" height="5"/>
            <rect x="23" y="-1" width="2" height="5"/>
            <rect x="22" y="19" width="5" height="4"/>
            <rect x="3" y="19" width="5" height="4"/>
          </g><rect x="22" y="7" width="2" height="2" fill="#101014"/>`
        ]
      },

      {
        id: 7,
        title: "7. Geometric Papercut",
        desc: "Modern low-poly faceted edges with crisp upright triangular ears. Scandinavian minimalist vibe.",
        sleeping: `
          <g fill="#ffffff">
            <polygon points="6,24 12,18 22,18 26,24 20,27 10,27"/>
            <polygon points="17,18 20,11 25,12 24,19"/>
            <polygon points="18,11 19,5 21,11"/>
            <polygon points="22,11 23,5 25,12"/>
          </g>
          <line x1="20" y1="14" x2="23" y2="14" stroke="#101014" stroke-width="1.2"/>
          <g fill="#ffffff"><path d="M25,5 H27.5 L25.5,7.5 H28 V8.2 H25 Z"/></g>
        `,
        running: [
          `<g fill="#ffffff">
            <polygon points="7,20 12,15 20,15 23,20 20,22 10,22"/>
            <polygon points="17,15 19,8 24,9 22,16"/>
            <polygon points="18,8 19,2 21,8"/>
            <polygon points="22,8 23,2 25,9"/>
            <polygon points="19,21 24,26 22,27 17,22"/>
            <polygon points="11,21 6,26 4,25 9,21"/>
          </g><circle cx="21.5" cy="11" r="1.1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <polygon points="7,21 12,16 20,16 23,21 20,23 10,23"/>
            <polygon points="17,16 19,9 24,10 22,17"/>
            <polygon points="18,9 19,3 21,9"/>
            <polygon points="22,9 23,3 25,10"/>
            <polygon points="18,22 19,27 17,27 16,23"/>
            <polygon points="11,22 13,27 11,27 9,23"/>
          </g><circle cx="21.5" cy="12" r="1.1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <polygon points="7,20 12,15 20,15 23,20 20,22 10,22"/>
            <polygon points="17,15 19,8 24,9 22,16"/>
            <polygon points="18,8 19,2 21,8"/>
            <polygon points="22,8 23,2 25,9"/>
            <polygon points="18,21 21,26 19,27 16,22"/>
            <polygon points="10,21 7,26 5,25 9,21"/>
          </g><circle cx="21.5" cy="11" r="1.1" fill="#101014"/>`,
          `<g fill="#ffffff">
            <polygon points="7,17 12,12 20,12 23,17 20,19 10,19"/>
            <polygon points="17,12 19,5 24,6 22,13"/>
            <polygon points="18,5 19,-1 21,5"/>
            <polygon points="22,5 23,-1 25,6"/>
            <polygon points="19,18 26,20 25,21 17,19"/>
            <polygon points="10,18 3,20 4,21 10,19"/>
          </g><circle cx="21.5" cy="8" r="1.1" fill="#101014"/>`
        ]
      },

      {
        id: 8,
        title: "8. Expressive Peeking Llama",
        desc: "Focuses on a larger expressive face and perked tall ears. Maximizes facial emotion and eye clarity.",
        sleeping: `
          <g fill="#ffffff">
            <ellipse cx="16" cy="20" rx="10" ry="7"/>
            <ellipse cx="20" cy="14" rx="6.5" ry="5.5"/>
            <path d="M16,9 C15,9 14,5 15.5,3 C17,1.8 18.5,3 18,6 L17.5,9 Z"/>
            <path d="M20.5,9 C19.5,9 18.5,5 20,3 C21.5,1.8 23,3 22.5,6 L22,9 Z"/>
          </g>
          <path d="M18.5,14 Q20,12.5 21.5,14" stroke="#101014" stroke-width="1.3" stroke-linecap="round" fill="none"/>
          <g fill="#ffffff"><path d="M24,6 H26.5 L24.5,8.5 H27 V9.2 H24 Z"/></g>
        `,
        running: [
          `<g fill="#ffffff">
            <ellipse cx="14" cy="18" rx="9" ry="6"/>
            <ellipse cx="20" cy="12" rx="6.5" ry="5.5"/>
            <path d="M16,7 C15,7 14,3 15.5,1 C17,-0.2 18.5,1 18,4 L17.5,7 Z"/>
            <path d="M20.5,7 C19.5,7 18.5,3 20,1 C21.5,-0.2 23,1 22.5,4 L22,7 Z"/>
            <path d="M19,23 Q23,24 25,27 Q23.5,28 22,27 Q19.5,25 18,24 Z"/>
            <path d="M9,23 Q6,24 4,26.5 Q4.5,27.5 6,27 Q8,25 10,23 Z"/>
          </g><circle cx="21.5" cy="11.5" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="19" rx="9" ry="6"/>
            <ellipse cx="20" cy="13" rx="6.5" ry="5.5"/>
            <path d="M16,8 C15,8 14,4 15.5,2 C17,0.8 18.5,2 18,5 L17.5,8 Z"/>
            <path d="M20.5,8 C19.5,8 18.5,4 20,2 C21.5,0.8 23,2 22.5,5 L22,8 Z"/>
            <path d="M18,24 Q19,26 18.5,27.5 Q17.5,27.5 17,26 Q16.5,25 16.5,24 Z"/>
            <path d="M11,24 Q12,26 11.5,27.5 Q10.5,27.5 10,26 Q9.5,25 9.5,24 Z"/>
          </g><circle cx="21.5" cy="12.5" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="18" rx="9" ry="6"/>
            <ellipse cx="20" cy="12" rx="6.5" ry="5.5"/>
            <path d="M16,7 C15,7 14,3 15.5,1 C17,-0.2 18.5,1 18,4 L17.5,7 Z"/>
            <path d="M20.5,7 C19.5,7 18.5,3 20,1 C21.5,-0.2 23,1 22.5,4 L22,7 Z"/>
            <path d="M18,23 Q22,24 23.5,26.5 Q22.5,27.5 21,26.5 Q19,25 17,24 Z"/>
            <path d="M9,23 Q6.5,24.5 5,27 Q5.5,28 7,27.5 Q9,25.5 10,23 Z"/>
          </g><circle cx="21.5" cy="11.5" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="16" rx="9" ry="6"/>
            <ellipse cx="20" cy="10" rx="6.5" ry="5.5"/>
            <path d="M16,5 C15,5 14,1 15.5,-1 C17,-2.2 18.5,-1 18,2 L17.5,5 Z"/>
            <path d="M20.5,5 C19.5,5 18.5,1 20,-1 C21.5,-2.2 23,-1 22.5,2 L22,5 Z"/>
            <path d="M19,20 Q24,20.5 26.5,22.5 Q26,23.5 24.5,23 Q21.5,22 18,21 Z"/>
            <path d="M9,20 Q5,20.5 2.5,22.5 Q3,23.5 4.5,23 Q7.5,22 10,21 Z"/>
          </g><circle cx="21.5" cy="9.5" r="1.3" fill="#101014"/>`
        ]
      },

      {
        id: 9,
        title: "9. Bouncy Jelly Trotter",
        desc: "Squash-and-stretch cartoon physics with rubbery leg extensions and ear flops. High animation energy.",
        sleeping: `
          <g fill="#ffffff">
            <ellipse cx="16" cy="22" rx="11" ry="5.5"/>
            <circle cx="21" cy="15" r="5"/>
            <path d="M19,10 C18,10 17,7 18,5 C19,4 20.5,5 20,7 L19.5,10 Z"/>
            <path d="M22,10 C21,10 20,7 21,5 C22,4 23.5,5 23,7 L22.5,10 Z"/>
          </g>
          <path d="M19.5,15 Q21,13.5 22.5,15" stroke="#101014" stroke-width="1.2" stroke-linecap="round" fill="none"/>
          <g fill="#ffffff"><path d="M25,7 H27.5 L25.5,9.5 H28 V10.2 H25 Z"/></g>
        `,
        running: [
          `<g fill="#ffffff">
            <ellipse cx="14" cy="18" rx="8" ry="6"/>
            <circle cx="21" cy="11" r="5.5"/>
            <path d="M18,6 C17,6 16,3 17,1 C18,0 19.5,1 19,3 L18.5,6 Z"/>
            <path d="M21,6 C20,6 19,3 20,1 C21,0 22.5,1 22,3 L21.5,6 Z"/>
            <path d="M18,22 Q23,24 26,27 Q24.5,28 23,27 Q19.5,24.5 17,23 Z"/>
            <path d="M9,22 Q5,24 3,27 Q3.5,28 5,27 Q8,24.5 10,22 Z"/>
          </g><circle cx="22" cy="10" r="1.2" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="20" rx="9" ry="5"/>
            <circle cx="21" cy="13" r="5.2"/>
            <path d="M18,8 C17,8 16,5 17,3 C18,2 19.5,3 19,5 L18.5,8 Z"/>
            <path d="M21,8 C20,8 19,5 20,3 C21,2 22.5,3 22,5 L21.5,8 Z"/>
            <ellipse cx="18" cy="26" rx="2.5" ry="1.8"/>
            <ellipse cx="10" cy="26" rx="2.5" ry="1.8"/>
          </g><circle cx="22" cy="12" r="1.2" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="18" rx="8" ry="6"/>
            <circle cx="21" cy="11" r="5.5"/>
            <path d="M18,6 C17,6 16,3 17,1 C18,0 19.5,1 19,3 L18.5,6 Z"/>
            <path d="M21,6 C20,6 19,3 20,1 C21,0 22.5,1 22,3 L21.5,6 Z"/>
            <path d="M18,22 Q22,24 24,27 Q23,28 21.5,27 Q19,24.5 17,23 Z"/>
            <path d="M10,22 Q6,24 4.5,27 Q5.5,28 7,27 Q9,24.5 11,22 Z"/>
          </g><circle cx="22" cy="10" r="1.2" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="15" rx="7" ry="6.5"/>
            <circle cx="21" cy="8" r="5.5"/>
            <path d="M18,3 C17,3 16,0 17,-2 C18,-3 19.5,-2 19,0 L18.5,3 Z"/>
            <path d="M21,3 C20,3 19,0 20,-2 C21,-3 22.5,-2 22,0 L21.5,3 Z"/>
            <path d="M18,19 Q23,19.5 27,21 Q26.5,22.2 25,22 Q21.5,20.5 17,20 Z"/>
            <path d="M9,19 Q4,19.5 1.5,21 Q2,22.2 3.5,22 Q7.5,20.5 10,20 Z"/>
          </g><circle cx="22" cy="7" r="1.2" fill="#101014"/>`
        ]
      },

      {
        id: 10,
        title: "10. Dual-State Snowball",
        desc: "Curled into a perfectly round fluffy white sleeping snowball at 0% load. Leaps out into an elongated runner at >0%.",
        sleeping: `
          <g fill="#ffffff">
            <!-- Round sleeping snowball -->
            <circle cx="16" cy="18" r="9.5"/>
            <!-- Cute tucked ears -->
            <path d="M13,9 C12,9 11.5,7 12.5,5.5 C13.5,4.5 14.5,5 14.5,7 Z"/>
            <path d="M18,9 C17,9 16.5,7 17.5,5.5 C18.5,4.5 19.5,5 19.5,7 Z"/>
            <ellipse cx="16" cy="27" rx="6" ry="1.5"/>
          </g>
          <!-- Happy closed curved eyes -->
          <path d="M12.5,16 Q14,14 15.5,16" stroke="#101014" stroke-width="1.3" stroke-linecap="round" fill="none"/>
          <path d="M16.5,16 Q18,14 19.5,16" stroke="#101014" stroke-width="1.3" stroke-linecap="round" fill="none"/>
          <!-- Little smile -->
          <path d="M15,19 Q16,20 17,19" stroke="#101014" stroke-width="1" stroke-linecap="round" fill="none"/>
          <!-- z Z bubbles -->
          <g fill="#ffffff">
            <path d="M23,8 H25.5 L23.5,10.5 H26 V11.2 H23 L25,9 H23 Z"/>
            <path d="M26,2.5 H29 L26.5,6 H29.5 V6.8 H26 L28.5,3.3 H26 Z"/>
          </g>
        `,
        running: [
          `<g fill="#ffffff">
            <ellipse cx="14" cy="18" rx="8.5" ry="6"/>
            <circle cx="21" cy="11" r="5.8"/>
            <path d="M18,6 C17,6 16.5,3 17.5,1.5 C18.5,0.5 20,1 19.8,3.5 L19.5,6 Z"/>
            <path d="M21.5,6 C20.5,6 20,3 21,1.5 C22,0.5 23.5,1 23.3,3.5 L23,6 Z"/>
            <path d="M19,22 Q23,23 25,27 Q24,28 22.5,27 Q20,24.5 18,23 Z"/>
            <path d="M9,22 Q6,23 3.5,26 Q4,27 5.5,26.5 Q8,24.5 10,22 Z"/>
          </g><circle cx="22.5" cy="10" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="19" rx="8.5" ry="6"/>
            <circle cx="21" cy="12" r="5.8"/>
            <path d="M18,7 C17,7 16.5,4 17.5,2.5 C18.5,1.5 20,2 19.8,4.5 L19.5,7 Z"/>
            <path d="M21.5,7 C20.5,7 20,4 21,2.5 C22,1.5 23.5,2 23.3,4.5 L23,7 Z"/>
            <ellipse cx="18" cy="26" rx="2.5" ry="1.8"/>
            <ellipse cx="10" cy="26" rx="2.5" ry="1.8"/>
          </g><circle cx="22.5" cy="11" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="18" rx="8.5" ry="6"/>
            <circle cx="21" cy="11" r="5.8"/>
            <path d="M18,6 C17,6 16.5,3 17.5,1.5 C18.5,0.5 20,1 19.8,3.5 L19.5,6 Z"/>
            <path d="M21.5,6 C20.5,6 20,3 21,1.5 C22,0.5 23.5,1 23.3,3.5 L23,6 Z"/>
            <path d="M19,22 Q23,23 24.5,26 Q23.5,27 22,26 Q20,24.5 18,23 Z"/>
            <path d="M9,22 Q6.5,23.5 4.5,26.5 Q5,27.5 6.2,27 Q8,24.5 10,22 Z"/>
          </g><circle cx="22.5" cy="10" r="1.3" fill="#101014"/>`,
          `<g fill="#ffffff">
            <ellipse cx="14" cy="16" rx="8.5" ry="6"/>
            <circle cx="21" cy="9" r="5.8"/>
            <path d="M18,4 C17,4 16.5,1 17.5,-0.5 C18.5,-1.5 20,-1 19.8,1.5 L19.5,4 Z"/>
            <path d="M21.5,4 C20.5,4 20,1 21,-0.5 C22,-1.5 23.5,-1 23.3,1.5 L23,4 Z"/>
            <path d="M19,20 Q24,20 26.5,22 Q26,23.2 24.5,23 Q21.5,21.5 18,21 Z"/>
            <path d="M9,20 Q5,20.5 2.5,22.5 Q3,23.5 4.5,23 Q7.5,21.8 10,21 Z"/>
          </g><circle cx="22.5" cy="8" r="1.3" fill="#101014"/>`
        ]
      }
    ];

    let currentLoad = 0;
    let selectedCandidateId = 1;
    let animFrameIndex = 0;
    let animTimer = null;

    const grid = document.getElementById('candidatesGrid');
    const loadSlider = document.getElementById('loadSlider');
    const loadDisplay = document.getElementById('loadDisplay');
    const stateBadge = document.getElementById('stateBadge');
    const intervalDisplay = document.getElementById('intervalDisplay');
    const simBadge = document.getElementById('simBadge');
    const simIconSlot = document.getElementById('simIconSlot');
    const activeModelLabel = document.getElementById('activeModelLabel');

    // Build Cards
    CANDIDATES.forEach(cand => {
      const card = document.createElement('div');
      card.className = `candidate-card ${cand.id === selectedCandidateId ? 'selected' : ''}`;
      card.id = `card-${cand.id}`;
      card.onclick = () => selectCandidate(cand.id);

      card.innerHTML = `
        <span class="cand-num">#${cand.id}</span>
        <div class="cand-preview-box">
          <svg id="svg-cand-${cand.id}" viewBox="0 0 32 32">
            ${cand.sleeping}
          </svg>
        </div>
        <div class="cand-title">${cand.title}</div>
        <div class="cand-desc">${cand.desc}</div>
        <button class="cand-select-btn">${cand.id === selectedCandidateId ? '✓ Selected Style' : 'Select This Style'}</button>
      `;

      grid.appendChild(card);
    });

    function selectCandidate(id) {
      selectedCandidateId = id;
      document.querySelectorAll('.candidate-card').forEach(c => {
        c.classList.remove('selected');
        c.querySelector('.cand-select-btn').textContent = 'Select This Style';
      });
      const selected = document.getElementById(`card-${id}`);
      selected.classList.add('selected');
      selected.querySelector('.cand-select-btn').textContent = '✓ Selected Style';

      const candObj = CANDIDATES.find(c => c.id === id);
      activeModelLabel.textContent = `Active Selection: ${candObj.title}`;
      updateVisuals();
    }

    function calculateInterval(load) {
      if (load === 0) return null;
      return Math.max(60, Math.round(220 - (load * 1.6)));
    }

    function updateVisuals() {
      simBadge.textContent = `${currentLoad}%`;
      loadDisplay.textContent = `${currentLoad}%`;

      if (currentLoad === 0) {
        stateBadge.className = 'state-badge sleeping';
        stateBadge.textContent = '💤 Sleeping (0% Load)';
        intervalDisplay.textContent = 'Stopped (Idle)';

        // Update all cards to sleeping
        CANDIDATES.forEach(c => {
          const el = document.getElementById(`svg-cand-${c.id}`);
          if (el) el.innerHTML = c.sleeping;
        });

        // Update Simulator
        const active = CANDIDATES.find(c => c.id === selectedCandidateId);
        simIconSlot.innerHTML = `<svg viewBox="0 0 32 32">${active.sleeping}</svg>`;

        if (animTimer) {
          clearInterval(animTimer);
          animTimer = null;
        }
      } else {
        stateBadge.className = 'state-badge running';
        stateBadge.textContent = `🏃 Galloping (${currentLoad}% GPU Load)`;
        const ms = calculateInterval(currentLoad);
        intervalDisplay.textContent = `${ms} ms per frame`;

        restartTimer(ms);
      }
    }

    function restartTimer(ms) {
      if (animTimer) clearInterval(animTimer);
      animTimer = setInterval(() => {
        animFrameIndex = (animFrameIndex + 1) % 4;

        CANDIDATES.forEach(c => {
          const el = document.getElementById(`svg-cand-${c.id}`);
          if (el) el.innerHTML = c.running[animFrameIndex];
        });

        const active = CANDIDATES.find(c => c.id === selectedCandidateId);
        simIconSlot.innerHTML = `<svg viewBox="0 0 32 32">${active.running[animFrameIndex]}</svg>`;
      }, ms);
    }

    loadSlider.addEventListener('input', (e) => {
      currentLoad = parseInt(e.target.value, 10);
      updateVisuals();
    });

    // Initial render
    updateVisuals();
  </script>
</body>
</html>
'''

# Write to both project docs and the artifact brain directory
doc_path = "/home/mrnv/Documents/local-ai-monitor/docs/alpaca_gallery.html"
brain_path = "/home/mrnv/.gemini/antigravity/brain/6a31e139-ea5a-4089-b458-8aa8b4fb0fa4/alpaca_gallery.html"

with open(doc_path, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(brain_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated gallery at: {doc_path}")
print(f"Generated gallery artifact at: {brain_path}")
