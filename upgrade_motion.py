from pathlib import Path
import re

p = Path("index.html")
s = p.read_text()

# Remove the previous injected animation CSS.
marker = "/* Subtle professional animations */"
if marker in s:
    start = s.index(marker)
    end = s.find("</style>", start)
    if end == -1:
        raise SystemExit("Could not locate the end of the old CSS. No changes saved.")
    s = s[:start] + s[end:]

# Remove the previous interaction button and script.
s = re.sub(
    r'<button id="back-top".*?<!-- OC_INTERACTIONS_V1 -->.*?</script>',
    '',
    s,
    count=1,
    flags=re.S
)

# Remove old reveal classes if any were saved into the HTML.
s = re.sub(r'\sclass="motion-in visible"', '', s)
s = re.sub(r'\sclass="motion-in"', '', s)

css = r"""
/* Ambient constellation: subtle motion across the whole site */
#ambient-canvas {
  position:fixed;
  inset:0;
  width:100%;
  height:100%;
  pointer-events:none;
  z-index:0;
  opacity:.68;
}
body > *:not(#ambient-canvas) {
  position:relative;
  z-index:1;
}
#scroll-progress {
  position:fixed;
  top:0;
  left:0;
  width:0;
  height:2px;
  z-index:1000;
  pointer-events:none;
  background:linear-gradient(90deg,#7f91a5,var(--gold));
  box-shadow:0 0 10px #c5a87845;
}
.art {
  position:relative;
  overflow:hidden;
}
.ring {
  animation:orbit-slow 48s linear infinite;
  will-change:transform;
}
.ring.two {
  animation:orbit-counter 38s linear infinite;
}
.core {
  animation:core-glow 6s ease-in-out infinite;
}
@keyframes orbit-slow {
  from { transform:rotate(0deg); }
  to { transform:rotate(360deg); }
}
@keyframes orbit-counter {
  from { transform:scaleX(.58) rotate(0deg); }
  to { transform:scaleX(.58) rotate(-360deg); }
}
@keyframes core-glow {
  0%,100% { box-shadow:0 0 0 0 #c5a87808; }
  50% { box-shadow:0 0 30px 2px #c5a87822; }
}
@media(prefers-reduced-motion:reduce) {
  .ring,.ring.two,.core { animation:none!important; }
}
"""

if "</style>" not in s or "</body>" not in s:
    raise SystemExit("Expected HTML closing tags not found. No changes saved.")

s = s.replace("</style>", css + "\n</style>", 1)

js = r"""
<canvas id="ambient-canvas" aria-hidden="true"></canvas>
<div id="scroll-progress" aria-hidden="true"></div>
<script>
(() => {
  const canvas = document.getElementById('ambient-canvas');
  const ctx = canvas.getContext('2d', { alpha: true });
  const progress = document.getElementById('scroll-progress');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const smallScreen = matchMedia('(max-width: 700px)').matches;
  let w = 0, h = 0, dpr = 1, particles = [], frame = 0;
  const pointer = { x: -1000, y: -1000 };
  const count = smallScreen ? 28 : 52;
  const gold = [197, 168, 120];
  const blue = [122, 151, 177];

  function resize() {
    w = innerWidth;
    h = innerHeight;
    dpr = Math.min(devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - .5) * .28,
      vy: (Math.random() - .5) * .28,
      r: Math.random() * 1.35 + .45,
      tone: Math.random()
    }));
    draw();
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);

    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];

      if (!reduced) {
        a.x += a.vx;
        a.y += a.vy;
        if (a.x < -5) a.x = w + 5;
        if (a.x > w + 5) a.x = -5;
        if (a.y < -5) a.y = h + 5;
        if (a.y > h + 5) a.y = -5;

        const dx = a.x - pointer.x;
        const dy = a.y - pointer.y;
        const dist = Math.hypot(dx, dy);
        if (dist < 115 && dist > 0) {
          a.x += dx / dist * .24;
          a.y += dy / dist * .24;
        }
      }

      const tone = a.tone > .72 ? gold : blue;
      ctx.beginPath();
      ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${tone.join(',')},.7)`;
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        const dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (dist < 112) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(151,165,178,${(1 - dist / 112) * .17})`;
          ctx.lineWidth = .65;
          ctx.stroke();
        }
      }
    }

    if (!reduced && !document.hidden) {
      frame = requestAnimationFrame(draw);
    }
  }

  function updateProgress() {
    const max = document.documentElement.scrollHeight - innerHeight;
    const amount = max > 0 ? scrollY / max * 100 : 0;
    progress.style.width = amount + '%';
  }

  addEventListener('resize', resize, { passive: true });
  addEventListener('scroll', updateProgress, { passive: true });
  addEventListener('pointermove', e => {
    pointer.x = e.clientX;
    pointer.y = e.clientY;
  }, { passive: true });
  addEventListener('pointerleave', () => {
    pointer.x = pointer.y = -1000;
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(frame);
    else if (!reduced) draw();
  });

  resize();
  updateProgress();
})();
</script>
"""

s = s.replace("</body>", js + "\n</body>", 1)
p.write_text(s)
print("Installed site-wide constellation animation and scroll progress.")
