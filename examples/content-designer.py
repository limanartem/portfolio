"""Example content for a creative profile (graphic designer): gallery-first, light theme, no timeline, no outcomes.

Build it with:  CONTENT=examples/content-designer.py python3 build.py
Assets referenced here live in examples/assets/; copy real work into src/assets/ for a real site.
The images are plain placeholders, not anyone's work.
"""
import os, shutil
from build import img, SRC

# the example keeps its placeholder art next to this file; copy it where asset() can find it
_ex = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(os.path.join(SRC, "assets", "example"), exist_ok=True)
for f in os.listdir(_ex): shutil.copy(os.path.join(_ex, f), os.path.join(SRC, "assets", "example", f))

PERSON = dict(
    name="Mira Keller", first="Mira", last="Keller", initials="MK",
    title="Mira Keller · Graphic Designer",
    description="Mira Keller, graphic designer in Berlin: brand identities, editorial design and packaging for small businesses and cultural institutions.",
    badge="Independent designer, Berlin",
    tagline="Identities and print that people keep.",
    lede="Twelve years of brand identities, editorial design and packaging for small businesses, publishers and cultural institutions. I work from research to final artwork, and I like the moment a client sees their own thing for the first time.",
    meta=["Berlin", "DE native · EN C1"],
    location="Berlin",
    links=[("Behance", "https://www.behance.net/", "Behance"), ("Instagram", "https://www.instagram.com/", "Instagram")],
    hero_cta=("See the work", "#work"),
)

THEME = dict(
    scheme="light",
    accent_dark="#E8A86B", accent_light="#B5551D",
    display_font="Fraunces", body_font="Work Sans", mono_font="JetBrains Mono",
    google_fonts="family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Work+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500",
)

HERO_PHOTOS = []        # no portrait: the text-only hero is used
STATS = []
MARQUEE = []

SECTIONS = [
    dict(id="work", type="gallery", nav="Work", label="Selected work",
         heading="Selected work", intro="Identities, books and packaging from the last few years. Click any piece to see it large.",
         cta=("Full portfolio on Behance", "https://www.behance.net/", "Behance")),
    dict(id="about", type="about", nav="About", label="About",
         heading="Research first, then the fun part.",
         paragraphs=[
             "I design <strong>brand identities</strong>, <strong>editorial work</strong> and <strong>packaging</strong>, mostly for small businesses, publishers and cultural institutions that need one designer who can take a project from the first conversation to print-ready files.",
             "Every project starts with a week of looking: at the client, their customers and what everyone else in their field is doing. The design comes after that, and it is usually quieter than the first ideas.",
         ],
         facts=[("Focus", "Identity · Editorial · Packaging"), ("Clients", "Publishers, museums, food & drink"), ("Works", "Berlin, remote across Europe")]),
    dict(id="press", type="publications", nav="Press", label="Press & talks",
         heading="Press &amp; talks"),
    dict(id="skills", type="skills", nav="Tools", label="Tools", heading="Tools &amp; training"),
    dict(id="contact", type="contact", nav=None, label="Contact",
         heading="Have a project? <span class=\"accent\">Let's talk.</span>",
         text="Best reached by email or Instagram. I take on two or three new identities a year and smaller editorial work in between.",
         buttons=[("Write me", "mailto:hello@example.com", None), ("Instagram", "https://www.instagram.com/", "Instagram")]),
]

GALLERY = [
    dict(src="assets/example/work-1.svg", caption="Kaffeehaus Nord: identity, menus and cups", wide=True),
    dict(src="assets/example/work-2.svg", caption="Stadtmuseum annual report, 96 pages"),
    dict(src="assets/example/work-3.svg", caption="Verlag Hain poetry series, 12 covers", tall=True),
    dict(src="assets/example/work-4.svg", caption="Gin label and gift box"),
    dict(src="assets/example/work-5.svg", caption="Festival wayfinding system"),
    dict(src="assets/example/work-6.svg", caption="Type specimen, self-initiated", wide=True),
]

PUBLICATIONS = [
    dict(title="Quiet branding for loud markets", venue="Talk, Typo Berlin", year=2025, href="https://example.com/talk"),
    dict(title="Stadtmuseum report: case study", venue="Slanted Magazine", year=2024, href="https://example.com/case"),
    dict(title="Interview: designing for publishers", venue="PAGE", year=2023),
]

SKILLS = [
    ("Craft", ["Identity systems", "Typography", "Editorial layout", "Packaging dielines", "Print production", "Art direction"]),
    ("Tools", ["Adobe InDesign", "Adobe Illustrator", "Figma", "Affinity", "Glyphs"]),
]
EDUCATION = [("Diploma, Communication Design", "HTW Berlin · 2009 – 2013")]
CERTIFICATIONS = []
LANGS = [("German", "Native", 100), ("English", "C1", 85)]
CHIP_ICONS = "none"      # a designer's chips stay text
ICON_ALIAS = {}

IMPACT, JOBS, EARLIER, PROJECTS = [], [], [], []
MONOGRAM = {}
FOOTER = "© 2026 Mira Keller · Berlin"
