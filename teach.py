"""Socratic Educational Module (--teach) for Sanity_Engine_Cached.

Generates `teach_pack.md` alongside the engine report, designed for:
1. Blind-First Intuition Comparison: Author's initial guess vs. Engine's top vulnerabilities.
2. Step-by-Step Socratic Inquiry Sequences: Seeded per identified issue.
3. NotebookLM / Project Socratic Tutor System Prompts: Enforces non-sycophantic, citation-first learning.
4. One-Page Revision Deliverable Templates: Pre-structured for revised hypothesis resubmission.
"""

from typing import Any, Dict, List


def generate_teach_pack(
    hypothesis_text: str,
    blind_guess: str,
    verdict: str,
    issues: List[Dict[str, Any]],
    edge_conditions: List[Dict[str, Any]],
    notebooklm_url: str = "",
) -> str:
    """Renders the comprehensive Socratic teach_pack.md."""

    lines = [
        "# 🎓 Sanity Engine Socratic Teaching & Revision Pack (`teach_pack.md`)",
        "",
        "> **Purpose:** This pack turns an engine audit into an active Socratic learning assignment.",
        "> Rather than memorizing the engine's answers, work through the identified physical limits",
        "> using the canonical textbooks to understand *why* the failure mode exists and how to revise it.",
        "",
        "---",
        "",
        "## Part 1: Blind-First Intuition Check",
        "",
        "Before opening the full critique, compare your pre-audit intuition with the engine's findings:",
        "",
        f"- **Your Pre-Audit Guess:** *\"{blind_guess or 'No prior guess recorded.'}\"*",
        f"- **Engine Verdict:** **{verdict}**",
        f"- **Critical Vulnerabilities Found:** {len(issues)} issue(s) identified.",
        "",
        "### Reflection Questions:",
        "1. Did your intuition anticipate the primary physical bottleneck flagged by the engine?",
        "2. If not, was the blind spot mathematical (e.g. dimensional scale), thermodynamic (e.g. efficiency/entropy), or kinetic (e.g. diffusion vs. drift)?",
        "",
        "---",
        "",
        "## Part 2: Guided Socratic Inquiry Sequences",
        "",
        "Work through each issue below one by one using the reference textbooks:",
        "",
    ]

    for idx, iss in enumerate(issues, 1):
        claim = iss.get("claim", "Specific mechanism")
        contradiction = iss.get("contradiction", "Physical constraint")
        quote = iss.get("quote", "")
        source = iss.get("source", "Canonical Textbook")
        verified = iss.get("verified", False)

        status_badge = "✅ Verbatim Verified" if verified else "⚠️ Unverified / Check Source"

        lines.extend([
            f"### Issue #{idx}: {claim}",
            f"- **Physical Bottleneck:** {contradiction}",
            f"- **Authoritative Reference:** *{source}* ({status_badge})",
            f"- **Textbook Citation:** > *\"{quote}\"*",
            "",
            "#### Socratic Step-by-Step Questions for the Author:",
            f"1. *What fundamental physical law or boundary condition is violated by the proposed mechanism in Issue #{idx}?*",
            f"2. *Look up `{source}`. Locate the page or section discussing this phenomenon. What parameter or constant governs the upper limit?*",
            f"3. *Can the hypothesis be adjusted by changing the operational scale (e.g. temperature, concentration, geometry) to satisfy this limit?*",
            "",
        ])

    if edge_conditions:
        lines.extend([
            "---",
            "",
            "## Part 3: Critical Edge Conditions to Satisfy",
            "",
            "A revised hypothesis must explicitly satisfy these physical boundary constraints:",
            "",
        ])
        for ec in edge_conditions:
            param = ec.get("parameter", "Parameter")
            threshold = ec.get("threshold", "Limit")
            rationale = ec.get("rationale", "Physical basis")
            lines.append(f"- **`{param}`:** Must satisfy `{threshold}` — *{rationale}*")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Part 4: Pre-Configured Socratic Tutor System Prompt",
        "",
        "Copy and paste the prompt below into **Google NotebookLM**, **Claude Projects**, or **ChatGPT**",
        "alongside the attached textbooks to conduct an interactive Socratic coaching session:",
        "",
        "```markdown",
        "SYSTEM PROMPT: Socratic Falsification Tutor",
        "",
        "You are a strict, Socratic scientific tutor. You must use ONLY the attached textbooks and reference documents.",
        "Your objective is NOT to give me the answers, but to help me discover the physical limits of my hypothesis through guided questioning.",
        "",
        "Core Rules:",
        "1. Never explain the physical solution or give away the answer directly.",
        "2. Ask exactly ONE question at a time.",
        "3. Start by asking me about this issue: \"" + (issues[0].get("contradiction", "the primary physical limit") if issues else "the main claim") + "\".",
        "4. When I answer, ask what specific passage in the loaded textbooks supports my claim.",
        "5. Require me to provide an exact verbatim quote and chapter/page location before validating my reasoning.",
        "6. If I make an error or state an impossible physical scaling, ask a question that exposes the mathematical or thermodynamic contradiction.",
        "7. Keep responses concise, inquisitive, and academically rigorous.",
        "```",
        "",
    ])

    if notebooklm_url:
        lines.extend([
            f"> 🔗 **Launch Preloaded NotebookLM Library:** [Open Shared Textbook Notebook]({notebooklm_url})",
            "",
        ])

    lines.extend([
        "---",
        "",
        "## Part 5: One-Page Revision Deliverable Template",
        "",
        "Fill out this template for each resolved issue before resubmitting your hypothesis to the engine:",
        "",
        "```markdown",
        "# Revision Deliverable: [Hypothesis Title]",
        "",
        "## 1. Identified Physical Limit",
        "- Issue Addressed: [e.g. Stokes-Einstein diffusion limit at low Reynolds number]",
        "- Relevant Governing Equation: [e.g. D = kT / (6 * pi * eta * r)]",
        "",
        "## 2. Verified Textbook Citation",
        "- Textbook: [e.g. Berg, Random Walks in Biology, Chapter 1]",
        "- Verbatim Quote: \"...\"",
        "- Location/Page: [Page N]",
        "",
        "## 3. Revised Mechanism & Parameter Shifts",
        "- What Changed in the Hypothesis: [Explain how the new design meets the boundary condition]",
        "- New Parameter Values: [e.g. Reduced radius from 5um to 10nm to increase diffusion flux]",
        "",
        "## 4. Resubmission Checklist",
        "- [ ] Dimensional consistency verified with SymPy/Pint",
        "- [ ] Thermodynamic boundary conditions satisfied",
        "- [ ] Exact quotes verified in local text corpus",
        "```",
    ])

    return "\n".join(lines)
