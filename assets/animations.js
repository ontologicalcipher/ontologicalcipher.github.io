(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canvas = document.createElement('canvas');
  canvas.id = 'oc-particles';
  canvas.setAttribute('aria-hidden', 'true');
  Object.assign(canvas.style, {
    position: 'fixed', inset: '0', width: '100%', height: '100%',
    pointerEvents: 'none', zIndex: '0', opacity: '.6'
  });
  document.body.prepend(canvas);

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  let w, h, dpr, points = [], frame;
  const pointer = { x: -1000, y: -1000 };
  const count = innerWidth < 650 ? 24 : 52;

  function resize() {
    w = innerWidth;
    h = innerHeight;
    dpr = Math.min(devicePixelRatio || 1, 1.5);
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    points = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - .5) * .22,
      vy: (Math.random() - .5) * .22,
      gold: Math.random() > .76
    }));
    draw();
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);

    points.forEach((p, i) => {
      if (!reduced) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;

        const dx = p.x - pointer.x;
        const dy = p.y - pointer.y;
        const distance = Math.hypot(dx, dy);
        if (distance < 100 && distance > 0) {
          p.x += dx / distance * .25;
          p.y += dy / distance * .25;
        }
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.gold ? 1.5 : 1, 0, Math.PI * 2);
      ctx.fillStyle = p.gold ? '#dfbf80bb' : '#75a5d299';
      ctx.fill();

      for (let j = i + 1; j < points.length; j++) {
        const q = points[j];
        const distance = Math.hypot(p.x - q.x, p.y - q.y);
        if (distance < 100) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(140,165,190,${(1-distance/100)*.2})`;
          ctx.lineWidth = .6;
          ctx.stroke();
        }
      }
    });

    if (!reduced && !document.hidden) {
      frame = requestAnimationFrame(draw);
    }
  }

  addEventListener('resize', resize, { passive: true });
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

  // Scroll progress indicator.
  const bar = document.createElement('div');
  Object.assign(bar.style, {
    position: 'fixed', top: '0', left: '0', height: '2px',
    width: '0', zIndex: '1000', pointerEvents: 'none',
    background: 'linear-gradient(90deg,#75a5d2,#dfbf80)'
  });
  document.body.append(bar);

  function progress() {
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (max > 0 ? scrollY / max * 100 : 0) + '%';
  }
  addEventListener('scroll', progress, { passive: true });

  resize();
  progress();
})();
