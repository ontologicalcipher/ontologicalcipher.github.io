from pathlib import Path

p = Path("index.html")
s = p.read_text()

if 'id="channels"' in s:
    print("Channels section already exists; no duplicate added.")
    raise SystemExit(0)

css = """
/* Research and community links */
.channel-grid {
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:14px;
}
.channel-card {
  display:block;
  min-width:0;
  padding:20px;
  border:1px solid var(--line);
  border-radius:7px;
  background:linear-gradient(145deg,var(--panel),#141a20);
  transition:border-color .2s,transform .2s;
}
.channel-card:hover {
  border-color:var(--gold);
  transform:translateY(-3px);
}
.channel-symbol {
  display:grid;
  place-items:center;
  width:42px;
  height:42px;
  margin-bottom:16px;
  border:1px solid #8d7956;
  border-radius:50%;
  color:var(--gold);
  font:22px Georgia,serif;
}
.channel-card h3 { margin:0 0 8px;font-size:20px; }
.channel-card p { margin:0;color:var(--muted);font-size:13px; }
.channel-link {
  display:inline-block;
  margin-top:15px;
  color:var(--gold);
  font-size:12px;
}
@media(max-width:740px) {
  .channel-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .channel-card { padding:16px; }
}
@media(max-width:420px) {
  .channel-grid { grid-template-columns:1fr; }
}
"""

section = """
<section id="channels">
<div class="wrap">
  <div class="heading">
    <div>
      <div class="label">Find me around the web</div>
      <h2>Research, resources & community.</h2>
    </div>
    <p class="intro">Scientific exploration, creative resources, programming, software, and useful reading—all in their own channels.</p>
  </div>

  <div class="channel-grid">
    <a class="channel-card" href="https://t.me/fundanics" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">F</div>
      <h3>FUNDANICS</h3>
      <p>Scientific research, physics concepts, hypotheses, equations, and evidence-led exploration.</p>
      <span class="channel-link">Visit research channel ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/toxxicmen" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">T</div>
      <h3>Toxic Men</h3>
      <p>Editing inspiration and creative content.</p>
      <span class="channel-link">Open channel ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/+M0q9pSZkXg41ZmU9" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">D</div>
      <h3>Design & Editing</h3>
      <p>Design inspiration, editing content, visual ideas, and creative resources.</p>
      <span class="channel-link">Explore resources ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/+5iUa0obSjcpjNWU1" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">S</div>
      <h3>Softwares</h3>
      <p>Software resources and useful tools.</p>
      <span class="channel-link">Explore software ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/+F6DoXgkUpB4xYTI1" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">G</div>
      <h3>Graphic Software</h3>
      <p>Tools and resources for graphic design workflows.</p>
      <span class="channel-link">Explore tools ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/CSEGOODS" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">C</div>
      <h3>CSE Goods</h3>
      <p>Computer science resources and useful study material.</p>
      <span class="channel-link">Visit channel ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/+zBo6p5_8uNphNWE9" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">B</div>
      <h3>Books</h3>
      <p>Books and reading resources.</p>
      <span class="channel-link">Browse channel ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/+xAMlXE_1BEljOTdl" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">E</div>
      <h3>Editing Content</h3>
      <p>Creative edits, content ideas, and visual inspiration.</p>
      <span class="channel-link">View content ↗</span>
    </a>

    <a class="channel-card" href="https://t.me/+hHMjyIl6ul42YTUy" target="_blank" rel="noopener noreferrer">
      <div class="channel-symbol">&lt;/&gt;</div>
      <h3>Programming</h3>
      <p>Programming resources, coding, and development.</p>
      <span class="channel-link">Visit channel ↗</span>
    </a>
  </div>

  <div class="note">
    <strong style="color:var(--gold)">Direct contact</strong>
    <p style="margin:8px 0 0">Telegram: <a class="link" href="https://t.me/OntologicalCipher" target="_blank" rel="noopener noreferrer">@OntologicalCipher ↗</a></p>
  </div>
</div>
</section>
"""

if "</style>" not in s or '<section id="about">' not in s:
    raise SystemExit("Expected insertion points not found; index.html was not changed.")

s = s.replace("</style>", css + "\n</style>", 1)
s = s.replace('<section id="about">', section + '\n<section id="about">', 1)
s = s.replace(
    '<nav><a href="#work">Focus</a><a href="#method">Method</a><a href="#about">About</a></nav>',
    '<nav><a href="#work">Focus</a><a href="#channels">Channels</a><a href="#method">Method</a><a href="#about">About</a></nav>'
)

p.write_text(s)
print("Added 9 Telegram links, FUNDANICS feature card, contact link, and Channels navigation.")
