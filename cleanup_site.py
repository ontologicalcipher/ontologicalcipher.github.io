from pathlib import Path
import re

p = Path("index.html")
s = p.read_text()

# Remove the old JavaScript that adds the "Explore details" buttons.
s = re.sub(
    r'\s*// Add expandable details to research cards.*?'
    r'\n\s*// Show a back-to-top control after scrolling\.',
    '\n  // Show a back-to-top control after scrolling.',
    s,
    flags=re.S
)

# Remove any buttons/details already inserted into the cards in the HTML.
s = re.sub(
    r'<button[^>]*class="card-toggle"[^>]*>.*?</button>\s*'
    r'<div[^>]*class="card-extra"[^>]*>.*?</div>',
    '',
    s,
    flags=re.S
)

# Remove the central OC orbital illustration, keeping the surrounding hero intact.
s = re.sub(
    r'<div class="art">.*?</div>\s*(?=</div>)',
    '',
    s,
    count=1,
    flags=re.S
)

# Hide any remaining illustration if its markup differs.
extra_css = """
/* Removed old card controls and central OC illustration */
.card-toggle, .card-extra { display:none !important; }
.art { display:none !important; }
"""

if "</style>" not in s:
    raise SystemExit("Could not find </style>; file not changed.")

if "Removed old card controls and central OC illustration" not in s:
    s = s.replace("</style>", extra_css + "\n</style>", 1)

p.write_text(s)
print("Removed Explore details controls and hid the OC illustration.")
