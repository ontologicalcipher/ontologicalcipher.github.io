from pathlib import Path

p = Path("index.html")
s = p.read_text()

if "OC_INTERACTIONS_V1" in s:
    print("Enhancements already installed.")
    raise SystemExit(0)

css = """
/* Subtle professional animations */
@keyframes orbit {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
@keyframes orbit-back {
  from { transform: rotate(0deg) scaleX(.58); }
  to { transform: rotate(-360deg) scaleX(.58); }
}
@keyframes breathe {
  0%,100% { box-shadow: 0 0 0 0 #c5a87808; }
  50% { box-shadow: 0 0 24px 4px #c5a87820; }
}
.ring.one { animation: orbit 32s linear infinite; }
.ring.two { animation: orbit-back 25s linear infinite; }
.core { animation: breathe 5s ease-in-out infinite; }
.card {
  position:relative;
  overflow:hidden;
  transition:transform .25s ease,border-color .25s ease;
}
.card::before {
  content:"";position:absolute;top:0;left:0;width:100%;height:2px;
  background:var(--gold);transform:scaleX(0);transform-origin:left;
  transition:transform .3s ease;
}
.card:hover { transform:translateY(-4px);border-color:#8e7959; }
.card:hover::before { transform:scaleX(1); }
.motion-in {
  opacity:0;transform:translateY(14px);
  transition:opacity .65s ease,transform .65s ease;
}
.motion-in.visible { opacity:1;transform:translateY(0); }
.card-toggle {
  display:inline-block;margin-top:16px;padding:7px 0;
  color:var(--gold);background:transparent;border:0;
  font:inherit;font-size:12px;cursor:pointer;
}
.card-extra {
  margin-top:12px;padding-top:12px;border-top:1px solid var(--line);
  color:var(--muted);font-size:13px;line-height:1.7;
}
#back-top {
  position:fixed;right:20px;bottom:20px;z-index:10;width:42px;height:42px;
  border:1px solid #56616c;border-radius:50%;background:#19212a;
  color:var(--gold);font-size:20px;cursor:pointer;opacity:0;
  pointer-events:none;transform:translateY(8px);
  transition:opacity .2s ease,transform .2s ease;
}
#back-top.shown { opacity:1;pointer-events:auto;transform:translateY(0); }
@media(prefers-reduced-motion:reduce) {
  *,*::before,*::after {
    animation:none!important;scroll-behavior:auto!important;
    transition:none!important;
  }
  .motion-in { opacity:1;transform:none; }
}
"""

if "</style>" not in s or "</body>" not in s:
    raise SystemExit("Expected HTML tags not found; index.html was not changed.")

s = s.replace("</style>", css + "\n</style>", 1)

script = """
<!-- OC_INTERACTIONS_V1 -->
<button id="back-top" type="button" aria-label="Back to top">↑</button>
<script>
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items = document.querySelectorAll(
    '.hero > div, .heading, .card, .method > div, .note, .contact'
  );

  if ('IntersectionObserver' in window && !reduced) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: 0.12});

    items.forEach((el, i) => {
      el.classList.add('motion-in');
      el.style.transitionDelay = (i % 4) * 75 + 'ms';
      observer.observe(el);
    });
  }

  const details = [
    'Explore the question, document the method, test the result, and record what remains uncertain.',
    'Build practical tools in small stages, with clear boundaries, useful tests, and privacy in mind.',
    'Compare interpretations against evidence instead of treating an interesting pattern as proof.',
    'Separate established facts, mathematical consequences, hypotheses, and claims needing tests.'
  ];

  document.querySelectorAll('.card').forEach((card, i) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'card-toggle';
    button.textContent = 'Explore details +';
    button.setAttribute('aria-expanded', 'false');

    const extra = document.createElement('div');
    extra.className = 'card-extra';
    extra.hidden = true;
    extra.textContent = details[i % details.length];

    button.addEventListener('click', () => {
      const opening = extra.hidden;
      extra.hidden = !opening;
      button.textContent = opening ? 'Close details −' : 'Explore details +';
      button.setAttribute('aria-expanded', String(opening));
    });
    card.append(button, extra);
  });

  const top = document.getElementById('back-top');
  addEventListener('scroll', () => {
    top.classList.toggle('shown', scrollY > 450);
  }, {passive:true});

  top.addEventListener('click', () => {
    scrollTo({top:0, behavior:reduced ? 'auto' : 'smooth'});
  });
})();
</script>
"""

s = s.replace("</body>", script + "\n</body>", 1)
p.write_text(s)
print("Added subtle animations, scroll reveals, expandable cards, and back-to-top.")
