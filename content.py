"""Everything about the person. build.py renders it; nothing here is HTML.

Sections appear in the order of SECTIONS and only when listed, so a profile without
side projects or without an outcomes section simply leaves those entries out.
Each section entry: dict(id=..., type=<renderer>, nav=<nav label or None>, label=<numbered label>, **options).
Types: about, impact, experience, projects, gallery, publications, skills, contact.
"""
from build import img, phones  # slide helpers

PERSON = dict(
    name="Artem Liman", first="Artem", last="Liman", initials="AL",
    title="Artem Liman · Engineering Manager &amp; Team Lead",   # <title> and og:title (already HTML-escaped)
    description="Artem Liman, Engineering Manager and Team Lead in eHealth. 20+ years in software, 10 leading teams. Portfolio, career and side projects.",
    badge="Team Lead at CompuGroup Medical",       # small pill above the name; None hides it
    tagline="Engineering Manager &amp; Team Lead who still reads the diff.",
    lede="20+ years building software, 10 of them leading teams. Today I run two product teams at CompuGroup Medical shipping CGM Praxis, a cloud SaaS for medical practices in Germany.",
    meta=["Walldorf, Germany", "EN C1 · DE B2 · UA/RU native"],
    location="Walldorf, Germany",
    # profile links: (label, url, icon name from src/icons.json or None). The first is the primary button.
    links=[("LinkedIn", "https://www.linkedin.com/in/artem-liman", "LinkedIn"),
           ("GitHub", "https://github.com/limanartem", "GitHub")],
    hero_cta=("Side projects", "#projects"),       # third hero button; None hides it
)

THEME = dict(
    scheme="system",          # "dark" | "light" | "system": what a first-time visitor gets (CSS default is dark, light follows the OS)
    accent_dark="#6FC7B6", accent_light="#0E7A6B",
    display_font="Bricolage Grotesque", body_font="IBM Plex Sans", mono_font="JetBrains Mono",
    google_fonts="family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500",
)

HERO_PHOTOS = [  # order = slide order; one entry = no slider
 ('assets/hero/hero-1.jpg', 'Portrait of Artem Liman'),
 ('assets/hero/hero-2.jpg', 'Portrait of Artem Liman'),
]

# numbers under the hero; an empty list hides the strip
STATS = [("20", "+", "years in software engineering"), ("10", "", "years leading teams"),
         ("15", "", "engineers in two teams, DE &amp; RO"), ("4", "", "industries: eHealth, security, life sciences, aviation")]

# scrolling band of brand marks under the stats; empty list hides it
MARQUEE = ['TypeScript','React','Java','Kotlin','Spring Boot','C# / .NET','Node.js','Kubernetes','Kafka','PostgreSQL','AWS','Azure','GraphQL','Docker','GitLab CI/CD','Claude Code']

SECTIONS = [
    dict(id="about", type="about", nav="About", label="About",
         heading="Leading people, staying close to the code.",
         paragraphs=[
             "At <strong>CompuGroup Medical</strong> I lead two cross-functional product teams, 15 engineers across Germany and Romania, building <strong>CGM Praxis</strong>, a multi-tenant cloud SaaS for medical practices with deep TI/gematik integration. I own delivery, engineering practices and people development for both teams.",
             "Before that I managed the <strong>Avira Password Manager</strong> team through its integration into Gen, and spent eight years at <strong>inhive</strong> as lead engineer, team lead and architect on healthcare, life sciences and aviation projects for Roche, Lufthansa Group, Genentech, Merck and Bayer.",
             "I care about teams that ship steadily and engineers who keep growing. I stay hands-on with architecture reviews, CI/CD and automation, and use side projects to try new tools and AI workflows before bringing them to a team.",
         ],
         facts=[("Domain", "eHealth · TI/gematik"), ("Also shipped in", "Security · Life sciences · Aviation"), ("Works in", "Regulated, distributed teams")]),
    dict(id="impact", type="impact", nav="Impact", label="Selected impact", heading="Outcomes I'm proud of"),
    dict(id="experience", type="experience", nav="Career", label="Career", heading="Career path",
         era_label="2001 – 2012 · Earlier roles", start_label="2001 · first commit"),
    dict(id="projects", type="projects", nav="Projects", label="Side projects",
         heading="Where I keep my hands on the keyboard",
         intro="Products and playgrounds I build after hours to try architectures, tools and AI workflows before I bring them to a team.",
         cta=("All repositories", "https://github.com/limanartem", "GitHub")),
    dict(id="skills", type="skills", nav="Skills", label="Toolbox", heading="Skills &amp; stack"),
    dict(id="contact", type="contact", nav=None, label="Contact",
         heading="Let's talk <span class=\"accent\">engineering.</span>",
         text="Happy to connect about engineering leadership, eHealth, distributed systems or AI-assisted development. LinkedIn is the best way to reach me.",
         buttons=[("Connect on LinkedIn", "https://www.linkedin.com/in/artem-liman", "LinkedIn"), ("github.com/limanartem", "https://github.com/limanartem", "GitHub")]),
]

# Outcomes as constraint → decision → result. `shift=(before, after)` is the headline change; the arrow draws on reveal.
# A plain (where, metric, title, text) tuple still renders as a simple card.
IMPACT = [
 dict(where='CompuGroup Medical', shift=('MVP', 'Live'), title='Took CGM Praxis into production',
      constraint='Two teams in Germany and Romania, and a go-live that hinged on the TI/gematik modules (VSDM, KIM, ePA, eAU, eArztbrief, e-signature) working against external TI vendors.',
      decision='Owned the TI modules and the vendor coordination myself, and automated release preparation across ~35 repositories so releasing stopped being the bottleneck.',
      result='Live since 2025, with several dozen medical practices onboarded.'),
 dict(where='Avira / Gen', shift=('Avira backend', 'Gen backend'), title='Zero-knowledge backend migration',
      constraint='Zero-knowledge encryption: the server never sees a master password, so vaults cannot be re-encrypted in bulk.',
      decision='Move each vault on its owner’s next login, and run both backends for as long as the tail takes.',
      result='~200k Password Manager accounts moved safely over several months.'),
 dict(where='Roche', shift=('Prototype', 'Production'), title='Research collaboration platform shipped',
      constraint='A Confluence-based collaboration platform that research teams already wanted, built as a prototype.',
      decision='Led the team that hardened it for production use rather than starting over.',
      result='In production for Roche research teams.'),
 dict(where='Roche Diagnostics', shift=('SQL Server', 'SAP HANA'), title='Re-platformed a biospecimen system',
      constraint='A LIMS heading for larger datasets, more complex studies and samples spread across the globe.',
      decision='Move storage to SAP HANA and rework availability and replication in the same release, as architecture and development lead.',
      result='A release ready for the dataset sizes and distributed studies that followed.'),
 dict(where='Lufthansa Group', shift=('3 airlines', '1 platform'), title='Public web platform at airline scale',
      constraint='Three airline brands on one public-facing platform, with third-party APIs the team did not control.',
      decision='One white-labeled platform, delivered end to end by a single Scrum team from requirements to release.',
      result='Lufthansa, SWISS and Austrian Airlines served from the same codebase.'),
 dict(where='Genentech · Merck · Bayer', shift=('As-is', 'Target architecture'), title='Architecture advisory in regulated life sciences',
      constraint='Regulated R&D, and vendor decisions for systems that would run for years.',
      decision='Assess the as-is architecture, design the target and run a structured RFI/RFP rather than pick a vendor on reputation.',
      result='A LIMS selection for Genentech and a big-data and genome-analysis platform for Merck R&D.'),
]

JOBS = [
 dict(logo='cgm', period='Jun 2024 – Present', company='CompuGroup Medical', place='Germany', role='Team Leader · CGM Praxis',
      scope='Two teams, 15 engineers in Germany and Romania, 5 direct reports. Multi-tenant cloud SaaS for medical practices.',
      points=['Took CGM Praxis from MVP to production; responsible for TI/gematik modules and TI vendor coordination.',
              'Introduced automated engineering and product KPIs with team dashboards.',
              'Automated release preparation across ~35 repositories and built a signed, notarized macOS installer pipeline on Azure DevOps.',
              'Delivered my teams’ share of the C5 attestation: access automation, vulnerability handling, pentest follow-ups, SOPs.',
              'Hire and onboard engineers, run reviews, goal setting, promotions and calibration; helped introduce CoderPad for screening.',
              'Built agent skills that check implementations against requirements and an AI reviewer for AI-generated code.'],
      tech=['TypeScript','React','Java','Kotlin','Spring Boot','PostgreSQL','Kubernetes','Kafka','GitLab CI/CD','Azure DevOps']),
 dict(logo=['avira', 'gen'], period='Jun 2020 – Feb 2024', company='Avira / NortonLifeLock / Gen', place='Germany', role='Engineering Manager · Browser-Based Applications',
      scope='Team of 7–9 engineers (iOS, Android, web, AWS backend) in Germany and Romania on Avira Password Manager and next-generation products on a unified platform.',
      points=['Led the migration of ~200k Password Manager accounts to Gen’s shared backend under zero-knowledge constraints.',
              'Shipped Avira Security desktop integration, new onboarding, master-password recovery and file attachments.',
              'After the Gen merger, coordinated integration and white-labeling with a team in India.',
              'Won first place in the company hackathon with a Figma-to-code pipeline generating per-platform design assets.',
              'Took over AWS backend and DevOps when needed; set engineering standards, code reviews and CI across web, mobile and backend.'],
      tech=['TypeScript','React','Node.js','C# / .NET Core','Kotlin','Swift','Python','AWS','DynamoDB','Docker','Jenkins','A/B testing']),
 dict(logo='inhive', period='May 2012 – May 2020', company='inhive Group', place='Germany', role='Lead Engineer · Team Lead · Architect',
      scope='Lead and architect roles on healthcare, pharma and aviation projects for Roche, Lufthansa Group, Genentech, Merck and Bayer.',
      points=['Lufthansa Group: led a Scrum team on the white-labeled public web platform for Lufthansa, SWISS and Austrian Airlines.',
              'Roche Diagnostics: architecture and development lead on a biospecimen-management (LIMS) release moving to SAP HANA.',
              'Led inhive’s own eHealth platform (web portal, taxonomy API, developer portal) on Azure and SAP HANA Cloud Platform.',
              'Roche: led the team that took a Confluence-based research collaboration platform from prototype to production.',
              'Genentech, Merck, Bayer: architecture assessments, target architectures, RFI/RFP vendor selection and distributed PoCs.'],
      tech=['.NET','ASP.NET Core','C#','Java','Azure','SAP HANA','SQL Server','Cosmos DB','MongoDB','Atlassian SDK']),
]

EARLIER = [
 ('verivox','2012','Germany','Senior .NET Developer','Verivox','Germany’s largest independent energy and telecom comparison portal: PDF sign-up features and a standalone importer that brought provider tariffs into the online system.','C# · ASP.NET · SQL Server · NUnit · TDD'),
 ('nix','2009 – 2011','Ukraine','Team Lead / .NET Tech Lead','N-iX','Led 6 developers and 2 QA engineers as Scrum Master for Manodo (Sweden): a web portal to monitor and control energy use across large smart-building estates. Core features, database design, specs and planning.','Silverlight · C# · Prism · WCF · SQL Server'),
 ('edvantis','2007 – 2008','Ukraine','Senior .NET Developer / Team Lead','Edvantis','Led 3–7 developers within a 30-person team building property tax and appraisal software for True Automation (US); owned core logic and the billing module.','.NET 3.5 · C# · SQL Server · Crystal Reports'),
 ('ukeess','2005 – 2007','Ukraine','Senior .NET Developer','UKEESS Software House','Server-side development for Cabconnect’s taxi payment platform: portals for drivers, card holders and cab companies on in-house business and UI frameworks.','.NET 2.0 · C# · ASP.NET · SQL Server'),
 ('leonorm','2001 – 2005','Ukraine','Software Developer','Leonorm','Internal projects for a national standards organisation: database design and Windows Forms applications.','.NET 1.1 · C# · VB.NET · Caché'),
]

MONOGRAM = {'cgm': 'CGM', 'avira': 'AV', 'gen': 'GEN', 'inhive': 'IH', 'verivox': 'VX', 'nix': 'NX', 'edvantis': 'ED', 'ukeess': 'UK', 'leonorm': 'LN'}

PROJECTS = [
 dict(id='planner', name='Schift Manager', kind='Resource & shift planning SaaS', status='Private beta',
      desc='Staff scheduling and management for small teams, from medical practices to retail and hospitality: shifts, availability, time off, timesheets and payroll export in one place, in English and German. Running as an invite-only private beta.',
      points=['Coverage analysis: per-position staffing minimums, a coverage health score and understaffing alerts',
              'Week, month and day schedules grouped by position, with labour cost per day, budget alerts and weekly publishing with history',
              'Time off, leave balances, timesheets, open shifts and shift trading, announcements, payroll export and working-time compliance checks',
              'Multi-location orgs with role-based access, Google sign-in and MFA, Stripe subscription tiers, public holidays per region',
              'Built spec-first with a Claude Code agent pipeline (design, implement, verify, audit), with Vitest and Playwright suites gating CI/CD on GitHub Actions'],
      tech=['React','TypeScript','MUI','Firebase','Zod','Stripe','Playwright','GitHub Actions','Claude Code'],
      live=('https://beta.schiftmanager.de','beta.schiftmanager.de'), private=True,
      slides=[img('assets/schift-login.jpg','Sign in with Google or email','#0D0F14','0px'),
              img('assets/schift-schedule.jpg','Weekly schedule grouped by position, with hours per employee and labour cost per day','#F4F5F8','0px'),
              img('assets/schift-coverage.jpg','Coverage view: staffing minimums per position, health score and understaffing alerts','#0D0F14','0px'),
              img('assets/schift-dashboard.jpg','Dashboard: today’s shifts, coverage status, pending requests and quick actions','#0D0F14','0px')]),
 dict(id='training', name='My Workout', kind='Mobile fitness app', status='Android beta',
      desc='A mobile fitness app that builds a workout plan around the equipment you actually have: photograph your training space and an OpenAI model works out the equipment and generates a weekly programme, no account needed.',
      points=['Equipment recognition from photos: snap your home gym and get a plan that uses only what is there',
              'AI-generated weekly programme with sets, reps and rest, drawn from a curated exercise catalogue and validated against your equipment',
              'Per-exercise detail: target muscles, how-to, pro tips and common mistakes',
              'Localised UI and exercise content (English, German, Ukrainian); anonymous sign-in, so onboarding needs no account',
              'Expo app plus Firebase Cloud Functions in a TypeScript monorepo; Android builds go to testers through Firebase App Distribution'],
      tech=['React Native / Expo','TypeScript','Firebase','OpenAI API','Zod','Vitest','GitHub Actions'], private=True,
      slide_bg=('var(--surface2)', '0px'),  # default for slides that don't set their own
      slides=[phones(['assets/training-onboarding.jpg','assets/training-scan.jpg'],'Onboarding and equipment scan: photos of the training space feed the plan generator'),
              phones(['assets/training-programme.jpg','assets/training-exercise.jpg'],'Generated weekly programme and exercise detail with today’s target'),
              phones(['assets/training-ready.jpg'],'Plan ready: days per week, experience level and goal')]),
 dict(id='shop', name='Shop.App', kind='Distributed systems playground', status='Open source',
      desc='A web shop used as a playground for integrating distributed components: polyglot microservices, message-driven order processing and web and mobile clients, with the backend and web client running from a single docker-compose up.',
      points=['Orders move through pending, payment and dispatch workers on RabbitMQ; status changes reach web and mobile in real time over GraphQL subscriptions',
              'Catalog API in .NET 8 minimal APIs with EF Core; orders API in Node.js and Express with both REST and GraphQL',
              'Auth via SuperTokens on PostgreSQL; MongoDB for orders, MySQL for the catalog, Redis caching; data stores and workers on a private network',
              'npm-workspaces monorepo with shared packages; Jest and xUnit tests in CI on GitHub Actions'],
      tech=['React','Redux','MUI','React Native / Expo','TypeScript','Node.js','Express','GraphQL','.NET 8','RabbitMQ','MongoDB','MySQL','PostgreSQL','Redis','Docker'],
      repo='https://github.com/limanartem/Shop.App',
      slides=[img('assets/shop-architecture.png','Architecture: public and private subnets, services and message broker','#FFFFFF','14px'),
              img('assets/shop-logo.png','Shop.App brand mark for web and mobile','var(--surface2)','40px')]),
 dict(id='home', name='Home Control Panel', kind='Wall-mounted smart home panel', status='2017 build',
      desc='A wall-mounted family dashboard: a C# UWP app on a Raspberry Pi 3 running Windows 10 IoT Core, with a 10-inch touch screen in a picture frame. It started as a full-screen family calendar and grew into a panel for the day ahead: time, weather, room climate and the next departures from nearby stops.',
      points=['Widgets: clock, weather forecast with hourly outlook, Google Calendar, room temperature and humidity, and real-time public transport departures for nearby stops',
              'Room climate from a DHT22 sensor; an ambient light sensor switches the UI between light and dark themes',
              'Hardware built by hand: Pi, sensors and display stacked on a custom back plate with brass standoffs over a VESA wall mount'],
      tech=['C#','UWP','Windows 10 IoT Core','Raspberry Pi'],
      repo='https://github.com/limanartem/HomeControlPanel',
      slide_bg=('#0E1013', '0px'),
      slides=[img('assets/home-wall.jpg','The panel, wall-mounted in a picture frame: clock, weather, room climate, calendar and live tram departures'),
              img('assets/home-screen.jpg','Home Panel screenshot (2017): clock, weather with hourly forecast, room temperature and humidity, Google Calendar and real-time departures for a nearby station'),
              img('assets/home-rpi.jpg','Debugging the dashboard on a Raspberry Pi 3 with Windows 10 IoT Core and a 10-inch touch screen'),
              img('assets/home-parts.jpg','Parts: Raspberry Pi 3, 10-inch touch display, VESA mount, standoffs and a temperature/humidity sensor'),
              img('assets/home-backplate.jpg','Back plate: the Raspberry Pi 3 wired to the DHT22 temperature/humidity sensor and a light sensor'),
              img('assets/home-side.jpg','Side view: display, Pi and back plate stacked on brass standoffs over a VESA wall mount')]),
]

SKILLS = [
 ('Leadership',['Hiring','Onboarding','Performance reviews','Calibration','Mentoring','1:1s','Distributed teams']),
 ('Delivery & practices',['Scrum','Kanban','TDD / BDD','Engineering KPIs','Release automation','Regulated environments']),
 ('Languages & frameworks',['TypeScript','JavaScript','Java','Kotlin','C#','React','Node.js','Spring Boot','.NET','REST','GraphQL']),
 ('Cloud, DevOps & data',['AWS','Azure','Kubernetes','Docker','Kafka','GitLab CI/CD','GitHub Actions','PostgreSQL','SQL Server','MongoDB','DynamoDB','Cosmos DB','SAP HANA']),
 ('Domains',['eHealth','TI / gematik (VSDM, KIM, ePA, eAU)','Zero-knowledge encryption','Life sciences & pharma R&D','Aviation web platforms']),
 ('AI tooling',['Claude Code','GitHub Copilot','Windsurf','OpenCode','Custom agent skills','OpenAI API']),
]

EDUCATION = [("M.Sc., Power Engineering", "Lviv Polytechnic National University · 2003 – 2005"),
             ("B.Sc., Electric Networks and Systems", "Lviv Polytechnic Institute · 2000 – 2003")]
CERTIFICATIONS = [("Developing Winning Teams", "troodi leadership training · 2026"),
                  ("Certified ScrumMaster (CSM)", "Scrum Alliance · 2010"),
                  ("AWS training", "Architecting, Developing, Advanced Developing, Serverless Solutions"),
                  ("Microsoft MCPD &amp; MCTS", "ASP.NET Developer 3.5 · .NET Framework 3.5 ASP.NET Applications")]
LANGS = [('Ukrainian','Native',100),('Russian','Native',100),('English','C1',85),('German','B2',68)]

# Where brand marks appear on chips: "all", "projects" (only project chips) or "none".
CHIP_ICONS = "all"
ICON_ALIAS = {'ASP.NET': '.NET', 'ASP.NET Core': '.NET', '.NET 3.5': '.NET', '.NET 2.0': '.NET', '.NET 1.1': '.NET', 'VB.NET': '.NET', 'NUnit': '.NET', 'C# / .NET Core': '.NET', 'Prism': '.NET', 'WCF': '.NET'}

# optional modules this profile does not use (see examples/content-designer.py)
GALLERY = []
PUBLICATIONS = []

FOOTER = "© 2026 Artem Liman · Walldorf, Germany"
