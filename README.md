# Sanity Engine Cached (Gemini Long-Context Edition)

**Sanity Engine Cached** is an adversarial scientific hypothesis auditor powered by **Google Gemini Long-Context Caching**, a **Level 0 Deterministic Math Firewall (SymPy / Pint)**, and **Programmatic Quote Verification**.

Instead of relying solely on paragraph-by-paragraph vector/keyword search (which misses non-local boundary conditions, footnotes, and mathematical proofs), Sanity Engine Cached front-loads a curated **~500,000-token canonical textbook library** directly into Gemini's 1,000,000-token context window with prefix caching.

---

## 🏛️ Architecture: The Gemini-Hybrid Framework

```text
                        ┌────────────────────────────────────────┐
                        │   Scientist / Student Input            │
                        │   (Hypothesis + Blind Guess)           │
                        └───────────────────┬────────────────────┘
                                            │
                                            ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ 1. Dual-Track Context & Verification Layer                                             │
 │                                                                                        │
 │  Track A: Static Foundation (500k Tokens)        Track B: Dynamic Literature Lookup    │
 │  ┌─────────────────────────────────────┐         ┌───────────────────────────────────┐ │
 │  │ Gemini API Context Cache            │         │ Scientist Hypothesis & Parameters │ │
 │  │ (11 Foundational Science Textbooks) │         │ (Unpublished Notes, ArXiv Papers) │ │
 │  └──────────────────┬──────────────────┘         └─────────────────┬─────────────────┘ │
 └─────────────────────┼──────────────────────────────────────────────┼───────────────────┘
                       │                                              │
                       └──────────────────────┬───────────────────────┘
                                              │
                                              ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ 2. Level 0 Deterministic Math Firewall                                                 │
 │  - SymPy equation parsing & Pint dimensional consistency verification                 │
 │  - Hard rejection of dimensionally non-homogeneous physical claims                    │
 └────────────────────────────────────────────┬───────────────────────────────────────────┘
                                              │
                                              ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ 3. Gemini Adversarial Critic Engine                                                    │
 │  - Evaluates hypothesis against full theoretical foundations in active memory          │
 │  - Enforces mandatory Quote-and-Locate citations                                       │
 │  - Programmatic substring verification against local plain-text corpus                 │
 └────────────────────────────────────────────┬───────────────────────────────────────────┘
                                              │
                                              ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ 4. Output Delivery & Socratic Module (`--teach`)                                       │
 │  - Audit Report: Verdict, Issue Board, Edge Conditions, Confidence                    │
 │  - teach_pack.md: Socratic Inquiry Sequence + NotebookLM-Ready System Prompts         │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💰 The Context Budget & Economics

### Why 500k Tokens?
Gemini models feature a unified **1,048,576-token context window** shared across inputs, internal chain-of-thought thinking, and outputs.

| Context Segment | Token Allocation | Purpose |
| :--- | :--- | :--- |
| **Static Reference Library (Track A)** | **~500,000 tokens** | 11 canonical textbooks (Berg, Feynman, Winter, Johnston & Wu, etc.). Automatically qualifies for Gemini's **90–95% cache discount**. |
| **Dynamic Input (Track B)** | **~100,000 tokens** | Scientist's hypothesis, experimental variables, recent preprints. |
| **Thinking Headroom** | **~250,000 tokens** | Internal reasoning steps for deep scientific derivations. |
| **Generated Output** | **~50,000 tokens** | Structured Issue Board, proofs, and Socratic learning packs. |

### Economics: Gemini Flash vs. Pro vs. Argon
- **Gemini Flash (`gemini-2.5-flash` / `gemini-3.8-flash`):**
  - Standard input: ~\$0.10 / 1M tokens.
  - Cached input (90% discount): **~\$0.01 / 1M tokens**.
  - Query cost for 500k tokens: **~\$0.005 – \$0.01 per run**.
- **Gemini 4 Argon (`gemini-4-argon`):**
  - Implicit caching: **\$0.00 idle storage fee**; 95% discount on cached reads.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/goldspruce/Sanity_Engine_Cached.git
cd Sanity_Engine_Cached
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and set your `GEMINI_API_KEY`:
```bash
GEMINI_API_KEY="your-gemini-api-key"
GEMINI_MODEL="gemini-2.5-flash"
```

### 3. Run via CLI
```bash
python run.py \
  --hypothesis "We propose unimpeded molecular diffusion across a 15-micron neuronal soma as the sole vesicular delivery mechanism." \
  --blind-guess "Diffusion time will be too slow over 15 microns" \
  --teach \
  --model gemini-2.5-flash
```

### 4. Launch the Interactive Dashboard
```bash
streamlit run app.py
```

---

## 🎓 Socratic Teaching Pack (`--teach`)

When `--teach` is enabled, the engine outputs `teach_pack.md` containing:
1. **Blind-First Reflection:** Compares the author's initial guess against the engine's identified vulnerabilities.
2. **Step-by-Step Socratic Questions:** Prompts designed to guide the author to discover the governing physical laws themselves.
3. **NotebookLM Tutor System Prompt:** Copy-paste prompt instructing LLMs to act as Socratic tutors using only the loaded textbooks.
4. **Revision Deliverable Template:** Pre-structured template for resubmitting an improved hypothesis.
