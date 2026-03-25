# OffGrid AI — Business Plan
### Local AI Installation & Setup Service for Remote & Off-Grid Use

---

## The Problem You're Solving

South Africa has a unique intersection of challenges that make offline AI not just useful, but essential:

- **Load shedding** — Eskom outages can last 4–12 hours a day, killing cloud access
- **Remote terrain** — The Drakensberg, Karoo, and coastal farms have zero or weak connectivity
- **Rural connectivity gaps** — Farming communities, game reserves, and rural schools can't reliably reach cloud AI
- **Disaster risk** — Cape Town faces wildfires, flooding, and infrastructure failures regularly
- **Data costs** — Running cloud AI is expensive on South African mobile data; offline AI is free after setup

**Offline AI on a device sidesteps all of these problems.**

---

## What You're Actually Selling

You're not just selling software. You're selling **peace of mind, productivity, and independence from the grid.**

### Core Service Tiers

| Tier | What They Get | Target Customer | Price Range (ZAR) |
|---|---|---|---|
| **Basic Install** | Ollama + 1–2 models (Llama3, Mistral) on their existing device | Individuals, students | R500–R800 |
| **Pro Setup** | Optimised install, model selection for use case, custom system prompt, UI | Freelancers, small business | R1,200–R2,500 |
| **Device Package** | Pre-configured mini PC or laptop ready to go, branded | Outdoors enthusiasts, farmers | R3,500–R8,000 |
| **Enterprise/Org** | Multi-device setup, training, support contract | NGOs, schools, field teams | R10,000–R50,000+ |

---

## The Tech Stack

### Option 1: Ollama (Recommended Starting Point)

**Ollama** is open source (MIT licensed), free to use commercially, and extremely easy to set up.

- Runs on Mac, Windows, Linux
- Dead simple — one command to pull and run a model
- Has a REST API so you can build apps on top of it
- Active community, well-maintained

**What a "reskin" looks like:**
1. Fork the Ollama repo on GitHub (or just use it as-is via its API)
2. Replace branding (name, logo, colours, system prompt defaults)
3. Bundle a curated set of pre-downloaded models (Llama 3.2, Mistral, Phi-3)
4. Add a custom default system prompt (e.g. "You are OffGrid AI, a South African assistant...")
5. Package an installer (`.exe` for Windows, `.dmg` for Mac, `.deb`/`.AppImage` for Linux)
6. Ship a simple desktop launcher (using Electron or Tauri for a custom chat UI)

You don't need to change the core Ollama engine — you're layering a branded experience on top.

### Option 2: Jan.ai

Jan is a fully offline ChatGPT alternative with a polished desktop UI. Open source, free.
- Already has a beautiful interface
- Supports multiple models
- You can theme it and pre-configure it

### Option 3: LM Studio

Popular, polished, easy for non-technical users. Not open source but free to use.
- Best UI out of the box
- Cannot be rebranded (licence restriction)
- Good for demos and proof of concept

### Recommended Model Stack

| Use Case | Model | Size |
|---|---|---|
| General chat/writing | Llama 3.2 3B | ~2GB |
| Coding help | Phi-3 Mini | ~2.3GB |
| Heavy tasks (if device allows) | Mistral 7B | ~4.1GB |
| Lightweight / old hardware | TinyLlama 1.1B | ~700MB |

### The Qwen Angle

Qwen3.5 (by Alibaba) is competitive with GPT-4 at smaller sizes and handles multilingual well — useful for Afrikaans, Zulu, Xhosa, and Sotho speakers. Worth including as a language-specific option.

---

## Hardware Recommendations

### For Customer Devices

| Device Type | Min Specs | Notes |
|---|---|---|
| Laptop (existing) | 8GB RAM, modern CPU | Works for 3B models |
| Laptop (ideal) | 16GB RAM, GPU optional | Handles 7B models well |
| Mini PC (pre-config) | Intel N100 / Ryzen 5, 16GB | ~R3,000–R5,000 to source |
| Raspberry Pi 5 | 8GB model | Slow but ultra-portable, great for field work |

### Pre-Configured Device Business

Buy mini PCs in bulk (Minisforum, Beelink, AliExpress via local freight forwarders), pre-install your branded OffGrid AI stack, sell at a margin. A R3,500 mini PC could retail at R6,500–R8,000 with software + setup + warranty.

---

## Cape Town Market Opportunities

### Who Needs This Right Now

1. **Eskom-affected home workers** — anyone WFH who loses productivity during load shedding
2. **Cape Winelands farms** — farm managers, admin, estate communications
3. **Outdoor/adventure businesses** — guides, rangers, trail operators needing offline tools
4. **NGOs and field workers** — social workers, health workers in townships and rural areas
5. **Schools in low-connectivity areas** — Mitchells Plain, Khayelitsha, rural Western Cape
6. **Legal/medical professionals** — anyone who can't put sensitive data on cloud AI (POPIA compliance)
7. **Filmmakers and creatives on location** — script help, subtitles, transcription offline

### POPIA Angle (Big One)

South Africa's POPIA law means businesses are cautious about what data they send to US/EU cloud services. Offline AI = zero data leaves the device. This is a legitimate business and legal argument.

---

## Go-To-Market Strategy

### Phase 1: Validate (Month 1–2)
- Offer 5–10 free installs to people in your network
- Target: freelancers, small business owners, one farmer contact
- Document every install — time, problems, what they needed
- Get testimonials

### Phase 2: Launch (Month 2–4)
- Build a simple landing page (see the interactive site in this repo)
- Post in Cape Town Facebook groups, Reddit (r/southafrica), LinkedIn
- Offer a free "AI readiness check" call — assess their device, recommend a package
- Partner with a local PC repair shop for referrals

### Phase 3: Scale (Month 4+)
- Target schools and NGOs (longer sales cycle but bigger contracts)
- Hire a helper for installs if demand grows
- Consider a monthly support/update subscription (R200–R500/month)

---

## Revenue Projections (Conservative)

| Month | Installs | Avg Revenue | Monthly Total |
|---|---|---|---|
| 1 | 3 | R800 | R2,400 |
| 2 | 6 | R1,200 | R7,200 |
| 3 | 10 | R1,500 | R15,000 |
| 6 | 20 | R2,000 | R40,000 |

One enterprise deal (school or NGO) = R15,000–R50,000. One of those a month changes everything.

---

## Competitive Advantage

- **Local knowledge** — you understand load shedding, SA connectivity, local languages
- **Personal service** — not a faceless tech product, someone who comes to you or guides you
- **First mover** — nobody is doing this as a formal service in Cape Town right now
- **Open source stack** — no licensing fees, you keep the margin

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Hardware becomes cheaper / easier to self-install | Focus on service, support, and customisation — not just the install |
| Ollama becomes paid | Switch to Jan.ai or LM Studio; stack is modular |
| Cloud AI gets cheaper / offline becomes less relevant | This is years away in SA given infrastructure |
| Competition from big tech players | They won't do house calls in Hout Bay |

---

## Next Steps

1. Install Ollama on your own machine — get comfortable with it
2. Download Llama 3.2 and Mistral 7B — test them for different use cases
3. Build your branded system prompt ("OffGrid AI" persona)
4. Create your first package offer and test it with 3 people you know
5. Set up the landing page (in this repo)
6. Post in one Cape Town community group about your service

---

*Built for Cape Town. Runs anywhere.*
