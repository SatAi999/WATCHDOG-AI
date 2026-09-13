# WATCHDOG — Autonomous Web Intelligence & Action Agent Platform

<p align="center">
  <img src="https://img.shields.io/badge/Hackathon-Anakin%20Forge-emerald?style=for-the-badge&logo=ai" alt="Anakin Forge Hackathon">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/TypeScript-5.0%2B-3178C6?style=for-the-badge&logo=typescript" alt="TypeScript">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> **"Don't just watch the web. Understand what changed, why it matters, and what should happen next."**

Built for the **Anakin Forge Hackathon**: *Build AI Agents That Read, Reason, and Act.*

---

## 📑 Table of Contents

- [Overview & Vision](#-overview--vision)
- [The Core 10-Step Autonomous Loop](#-the-core-10-step-autonomous-loop)
- [System Architecture](#-system-architecture)
- [First-Class Anakin Integration](#-first-class-anakin-integration)
- [8 Application Modes](#-8-application-modes)
- [Impact Engine Math & Decision Safety](#-impact-engine-math--decision-safety)
- [Action Registry & Verification Engine](#-action-registry--verification-engine)
- [Failure Recovery & Replanning](#-failure-recovery--replanning)
- [Project Directory Structure](#-project-directory-structure)
- [Local Setup & Windows Commands](#-local-setup--windows-commands)
- [Deployment Guide (Render & Vercel)](#-deployment-guide-render--vercel)
- [3-Minute Hackathon Demo Script](#-3-minute-hackathon-demo-script)
- [Security & License](#-security--license)

---

## 🛡️ Overview & Vision

**WATCHDOG** is a production-style, autonomous web intelligence agent system. It is **NOT** a chatbot, **NOT** a static mockup dashboard, and **NOT** a simplistic HTML line-comparator.

When given a natural language mission (e.g. *"Watch Sony WH-1000XM6 and tell me when it drops below ₹25,000 from a trustworthy seller with valid warranty"*), WATCHDOG converts the goal into a persistent machine-executable mission that operates 24/7.

### What WATCHDOG Does Genuinely:
1. **Discovers Relevant Sources**: Automatically identifies official stores, pricing matrix pages, product documentation, news outlets, careers pages, Reddit threads, and public reviews.
2. **Establishes Structured Baselines**: Extracts normalized fields (price, stock, warranty, return days, job openings, sentiment score) + sha256 content & semantic hashes.
3. **Monitors Continuously**: Executes background periodic polling via an integrated scheduler.
4. **Detects Meaningful Changes**: Filters out cosmetic copy edits (e.g., *"Get started today"* vs *"Start now"* is classified as `COSMETIC` and ignored).
5. **Investigates Cross-Source Correlations**: Correlates multiple independent web signals into a synthesized evidence graph (e.g. hiring spike + new enterprise pricing + product page update = Strategic Repositioning).
6. **Calculates Mathematical Impact Scores**: Computes normalized 0–100 impact scores deterministically to avoid LLM arithmetic hallucination.
7. **Renders Action Decisions**: Enforces strict user approval policies (`NOTIFY`, `RECOMMEND`, `PREPARE`, `EXECUTE`).
8. **Executes Authorized Actions**: Triggers controlled tasks via Anakin Wire or Browser workflows.
9. **Verifies Post-Execution State**: Checks DOM and API responses to confirm intended state before declaring success.
10. **Autonomously Recovers & Replans**: Automatically switches strategies (e.g., Wire 503 error → Anakin Headless Browser workflow fallback) when execution fails.

---

## 🔁 The Core 10-Step Autonomous Loop

```text
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                           CORE AGENTIC LOOP                              │
  └──────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                         1. OBSERVE (Fetch Live Web)
                                       │
                                       ▼
                      2. DETECT (Level 1 & 2 Change Diff)
                                       │
                                       ▼
                   3. UNDERSTAND (Filter Copy & Noise)
                                       │
                                       ▼
                 4. INVESTIGATE (Cross-Source Correlation)
                                       │
                                       ▼
                 5. ASSESS IMPACT (Weighted Math 0-100)
                                       │
                                       ▼
                     6. DECIDE (Evaluate Rules & Policy)
                                       │
                                       ▼
                    7. ACT (Execute Permitted Action)
                                       │
                                       ▼
                     8. VERIFY (Confirm State Integrity)
                                       │
                       ┌───────────────┴───────────────┐
                       │                               │
                [ Verification Passed ]       [ Verification Failed ]
                       │                               │
                       ▼                               ▼
            10. CONTINUE MONITORING            9. LEARN / REPLAN
                       ▲                               │
                       └───────────────────────────────┘
```

---

## 🏗️ System Architecture

WATCHDOG is architected as a stateful, event-driven monolith with clean separation between the FastAPI backend and Next.js frontend:

```text
                               WATCHDOG FRONTEND (Next.js 14)
                                             │
                                             ▼
                                FASTAPI BACKEND (Python 3.10+)
                                             │
                                      MISSION ENGINE
                                             │
                   ┌─────────────────────────┴─────────────────────────┐
                   │                                                   │
                   ▼                                                   ▼
            SOURCE ENGINE                                         AGENT ENGINE
                   │                                                   │
                   │                                   ┌───────────────┼───────────────┐
                   ▼                                   │               │               │
         FETCH MANAGER (Anakin/Jina)                   ▼               ▼               ▼
                   │                               REASONING       IMPACT MATH      DECISION
                   └───────────────────────────────────┬───────────────┴───────────────┘
                                                       │
                                                       ▼
                                                 ACTION ENGINE
                                                       │
                                                       ▼
                                              VERIFICATION ENGINE
                                                       │
                                                       ▼
                                            SQLITE PERSISTENCE DB
```

### Technology Stack:
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2.0, SQLite, APScheduler, Pytest, HTTPX, BeautifulSoup4.
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons, Framer Motion.
- **Integrations**: Anakin Search, Anakin Agentic Search, Anakin Wire, Anakin Scrape, Anakin Browser, Anakin Webhooks, Jina Reader API, Groq LLM API.

---

## ⚡ First-Class Anakin Integration

Anakin infrastructure powers WATCHDOG's web reading, multi-source research, structured site operations, and async job delivery:

- **`AnakinSearchService`**: Performs live SERP and web search queries for source discovery.
- **`AnakinAgenticSearchService`**: Executes deep multi-source research across targets to synthesize evidence snippets and confidence scores.
- **`AnakinWireService`**: Discovers and executes structured site operations (`amazon.product_detail`, `amazon.prepare_cart`, `saas.compare_plans`).
- **`AnakinScrapeService`**: Extracts clean markdown and HTML content.
- **`AnakinBrowserService`**: Executes headless browser automation steps (navigate, click, fill, extract) for fallback workflows.
- **`AnakinWebhookService`**: HMAC SHA-256 signature verification and delivery ID idempotency tracking (`POST /api/webhooks/anakin`).

---

## 🎯 8 Application Modes

WATCHDOG powers 8 application modes using **ONE single reusable agent engine**:

1. **DEALS**: Qualifies price drops with seller rating, return policy window, and manufacturer warranty verification.
2. **COMPETITOR INTELLIGENCE**: Correlates pricing changes, new product pages, job opening spikes, and press announcements into strategic insights.
3. **REPUTATION WATCH**: Tracks complaint velocity spikes across Reddit, YouTube, and news, linking issues to specific firmware/product versions.
4. **POLICY WATCH**: Monitors return, refund, and shipping policy clauses (e.g. 30-day → 15-day return window reduction).
5. **NEWS & EVENTS**: Clusters duplicate coverage and identifies underlying industry events.
6. **SOFTWARE / SaaS**: Tracks free tier user limits, storage shifts, and recommends alternatives when team limits are exceeded.
7. **AI VISIBILITY**: Tracks brand presence, cited sources, and recommendation frequency in AI discovery engines.
8. **CUSTOM / ANYTHING**: Converts any natural language goal into a machine-executable mission.

---

## 📐 Impact Engine Math & Decision Safety

To prevent LLM hallucination in quantitative scoring, the backend computes impact scores mathematically:

$$\text{Impact Score} = (0.25 \times \text{Magnitude}) + (0.25 \times \text{Relevance}) + (0.20 \times \text{Urgency}) + (0.15 \times \text{Confidence}) + (0.15 \times \text{Strategic Importance})$$

### Score Classification:
- **0 – 24**: `LOW`
- **25 – 49**: `MEDIUM`
- **50 – 74**: `HIGH`
- **75 – 100**: `CRITICAL`

### Action Permission Levels:
- `NOTIFY`: Inform user via alert.
- `RECOMMEND`: Provide strategic next steps.
- `PREPARE`: Prepare cart or draft action for user sign-off.
- `EXECUTE`: Automatically execute authorized safe actions.

> [!IMPORTANT]
> Financial transactions (such as final store checkouts) default to `PREPARE` and require human authorization in the Action Control Center before execution.

---

## 🛠️ Action Registry & Verification Engine

WATCHDOG enforces strict action safety through a controlled Action Registry:

| Action ID | Provider | Description | Risk Level | Verification Strategy |
|---|---|---|---|---|
| `amazon.product_detail` | Anakin Wire | Extract live Amazon price, seller, rating & warranty | LOW | API / DOM Check |
| `amazon.prepare_cart` | Anakin Wire | Prepare item in shopping cart for user review | LOW | Cart URL / State |
| `saas.compare_plans` | Anakin Wire | Extract pricing matrix & free tier limits | LOW | Structured Hash |
| `browser.execute_workflow` | Anakin Browser | Headless browser automation step execution | MEDIUM | DOM Extraction |
| `notify_user` | Internal | Send categorized push/dashboard alert | LOW | Log Audit Check |

---

## 🔄 Failure Recovery & Replanning

When an action or endpoint fails:
1. **Error Inspection**: Classifies error (`ACTION_UNAVAILABLE`, `TEMPORARY_NETWORK`, `AUTH_REQUIRED`).
2. **Autonomous Replanning**: Switches from Anakin Wire to Anakin Headless Browser workflow, or schedules exponential backoff retry.
3. **Re-Execution & State Verification**: Executes the fallback action and verifies outcome state before completing the run.

---

## 📂 Project Directory Structure

```text
WATCHDOG/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes (missions, events, actions, sources, dashboard, webhooks, demo, health)
│   │   ├── agents/       # Core 10-step agent modules (planner, discovery, baseline, change_detector, investigator, impact, decision, action_engine, verifier, recovery, engine)
│   │   ├── core/         # Config, security, scheduler
│   │   ├── db/           # SQLAlchemy database models & session setup
│   │   ├── demo/         # Deterministic seed scenarios & fixtures
│   │   ├── integrations/ # Anakin & Jina service integration layer
│   │   ├── schemas/      # Pydantic v2 validation models
│   │   └── main.py       # FastAPI application assembly
│   ├── tests/            # Pytest test suite (100% pass)
│   └── requirements.txt
├── frontend/
│   ├── app/              # Next.js 14 App Router pages (dashboard, missions, events, actions, sources, activity, demo)
│   ├── components/       # UI components (Sidebar, Navbar, TopMetrics, DemoControlBar, LiveFeedCard, ExecutionTimeline, EvidenceGraph, MissionCreatorModal)
│   ├── lib/              # API helper module & TypeScript types
│   ├── package.json
│   └── tailwind.config.js
├── docs/                 # Architecture, agent design, API reference, demo script
├── .gitignore
└── README.md
```

---

## 💻 Local Setup & Windows Commands

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup
```cmd
cd d:\WatchDog\backend

# Create & activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Run Pytest test suite (Verify 100% pass)
python -m pytest tests/test_watchdog.py

# Start FastAPI backend server (Port 8000)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup
```cmd
cd d:\WatchDog\frontend

# Install node packages
npm install

# Start Next.js development server (Port 3005)
npm run dev
```

Open `http://localhost:3005` in your browser.

---

## 🚀 Deployment Guide (Render & Vercel)

### Deploying Backend to Render.com
1. Create a new **Web Service** on [Render.com](https://render.com).
2. Connect your GitHub repository `https://github.com/SatAi999/WATCHDOG-AI.git`.
3. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `ANAKIN_API_KEY`: `your_anakin_api_key`
   - `JINA_API_KEY`: `your_jina_api_key`
   - `GROQ_API_KEY`: `your_groq_api_key`
   - `LLM_MODEL`: `llama-3.3-70b-versatile`
   - `EXECUTION_MODE`: `LIVE`

### Deploying Frontend to Vercel.com
1. Import your GitHub repository `WATCHDOG-AI` into [Vercel](https://vercel.com).
2. Set **Framework Preset**: `Next.js`
3. Set **Root Directory**: `frontend`
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://watchdog-ai.onrender.com/api`
5. Click **Deploy**.

---

## 🎬 3-Minute Hackathon Demo Script

1. **0:00 - 0:30 (Vision)**: Open `http://localhost:3005/dashboard`. Point out the **Attention Saved** counter (`6h 45m`) and explain that WATCHDOG is a persistent autonomous web agent.
2. **0:30 - 1:30 (Hero Scenario 1)**: Click **"1. Price Drop"** on the Judge Demo Control Center bar. Click **"View Investigation"** to inspect the Before/After state diff and 3-signal **Cross-Source Evidence Graph**.
3. **1:30 - 2:15 (Hero Scenario 5)**: Click **"5. Action Recovery"** to demonstrate failure recovery: Wire action fails → WATCHDOG automatically replans to Anakin Browser workflow → Verifies state.
4. **2:15 - 3:00 (Natural Language Mission & Human Authorization)**: Click **"+ New Mission"**, enter `"Watch Sony WH-1000XM6 below ₹25,000"`, activate the mission, and approve the cart action in the **Actions** tab.

---

## 🔒 Security & License

- `.env` files are strictly excluded via `.gitignore` to prevent credential leakage.
- Webhooks use HMAC SHA-256 signature verification and delivery ID idempotency.
- Distributed under the [MIT License](LICENSE).
