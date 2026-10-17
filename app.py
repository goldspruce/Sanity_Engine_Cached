"""Streamlit Dashboard for Sanity_Engine_Cached.

Provides an interactive GUI for:
1. Running Dual-Track Long-Context Audits using Gemini Flash with Context Caching.
2. Visualizing Level 0 Mathematical consistency checks (SymPy / Pint).
3. Reviewing the Falsification Issue Board with verified textbook quotes.
4. Generating and downloading the Socratic teach_pack.md for NotebookLM.
"""

import json
import os
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from engine import SanityEngineCached
from teach import generate_teach_pack

st.set_page_config(
    page_title="Sanity Engine Cached | Gemini Long-Context Auditor",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 Sanity Engine Cached")
st.caption("Adversarial Scientific Falsification powered by Gemini Long-Context Caching & Level 0 Math Firewall")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Engine Configuration")
    model_choice = st.selectbox(
        "Gemini Model Tier",
        ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-2.5-pro", "gemini-4-argon"],
        index=0,
        help="Gemini Flash models support 1M context with 90% cache discounts (~$0.01/call).",
    )
    cache_mode = st.radio(
        "Caching Mechanism",
        ["Implicit Prefix Caching (Auto / $0 storage)", "Explicit Session Cache (TTL-based)"],
        index=0,
    )
    st.divider()
    st.markdown("### 📚 Reference Library Context")
    st.info("~500,000 tokens of canonical textbooks pre-loaded (Berg, Feynman, Johnston & Wu, Winter, Cover, etc.).")
    
    nb_url = os.environ.get("NOTEBOOKLM_URL", "https://notebook.google.com/notebook/3eed2329-aeef-4e67-81ef-c5bc2c06f5bd")
    if nb_url:
        st.link_button("🔗 Open Shared NotebookLM Library", nb_url)

# Main Input Section
col_left, col_right = st.columns([2, 1])

with col_left:
    hypothesis_input = st.text_area(
        "Scientific Hypothesis / Mechanism",
        height=180,
        placeholder="Describe the biological/physical mechanism, variables, and scaling assumptions...\n\nExample:\nWe propose that intracellular transport across a 15-micrometer neuron soma occurs via unimpeded molecular diffusion, with Brownian motion delivering vesicles at a characteristic velocity of v = 50 um/s.",
    )

with col_right:
    blind_guess = st.text_input(
        "Blind-First Guess (Pre-Audit Intuition)",
        placeholder="What do you guess is the #1 physical limit on this idea?",
        help="Answering this before the audit improves Socratic reflection and mirrors peer-review best practices.",
    )
    generate_teach = st.checkbox("Generate Socratic Teaching Pack (`teach_pack.md`)", value=True)
    run_btn = st.button("🚀 Run Adversarial Audit", type="primary", use_container_width=True)

if run_btn:
    if not hypothesis_input.strip():
        st.warning("Please enter a hypothesis to audit.")
    else:
        with st.spinner("Analyzing hypothesis against ~500k-token canonical textbook library..."):
            engine = SanityEngineCached(
                corpus_dir="corpus",
                model_name=model_choice,
                use_explicit_cache="Explicit" in cache_mode,
            )
            result = engine.evaluate_hypothesis(
                hypothesis_text=hypothesis_input,
                blind_guess=blind_guess,
            )
            st.session_state["last_result"] = result
            st.session_state["last_hypothesis"] = hypothesis_input
            st.session_state["last_blind_guess"] = blind_guess

if "last_result" in st.session_state:
    res = st.session_state["last_result"]
    verdict = res.get("verdict", "UNKNOWN")

    # Verdict Banner
    if verdict == "SOUND":
        st.success(f"### Verdict: {verdict} (Confidence: {res.get('confidence')}%)")
    elif verdict == "CONDITIONALLY_PLAUSIBLE":
        st.warning(f"### Verdict: {verdict} (Confidence: {res.get('confidence')}%)")
    else:
        st.error(f"### Verdict: {verdict} (Confidence: {res.get('confidence')}%)")

    st.markdown(f"**Executive Summary:** {res.get('summary')}")

    # Tabs for detailed breakdown
    tab_issues, tab_math, tab_edges, tab_teach = st.tabs([
        f"🚨 Issue Board ({len(res.get('issues', []))})",
        "🧮 Level 0 Math Firewall",
        "📐 Edge Conditions & Green Flags",
        "🎓 Socratic Teach Pack",
    ])

    with tab_issues:
        st.subheader("Identified Physical & Mathematical Vulnerabilities")
        if not res.get("issues"):
            st.info("No physical contradictions or fatal vulnerabilities identified.")
        else:
            for i, iss in enumerate(res.get("issues", []), 1):
                sev = iss.get("severity", "MODERATE")
                badge = "🔴 FATAL" if sev == "FATAL" else ("🟠 HIGH" if sev == "HIGH" else "🟡 MODERATE")
                verified = iss.get("verified", False)
                ver_badge = "✅ Verbatim Quote Verified" if verified else "⚠️ Check Source"

                with st.expander(f"{badge} Issue #{i}: {iss.get('claim')}", expanded=True):
                    st.markdown(f"**Physical Violation:** {iss.get('contradiction')}")
                    st.markdown(f"**Governing Law:** `{iss.get('physical_law')}`")
                    st.markdown(f"**Authoritative Source:** *{iss.get('source')}* ({ver_badge})")
                    st.info(f"\"{iss.get('quote')}\"")

    with tab_math:
        st.subheader("Deterministic Equation & Dimensional Validation (SymPy / Pint)")
        math_res = res.get("math_firewall", {})
        if math_res.get("firewall_passed"):
            st.success("✅ All extracted equations passed dimensional consistency checks.")
        else:
            st.error("❌ Dimensional inconsistency detected in proposed equations.")

        if math_res.get("equations"):
            st.write(f"**Extracted Equations ({len(math_res['equations'])}):**")
            for eq in math_res["equations"]:
                st.code(eq, language="python")
        else:
            st.caption("No mathematical equations detected in the input payload.")

    with tab_edges:
        col_ec, col_gf = st.columns(2)
        with col_ec:
            st.subheader("Required Boundary Conditions")
            for ec in res.get("edge_conditions", []):
                st.markdown(f"- **`{ec.get('parameter')}`:** `{ec.get('threshold')}`")
                st.caption(ec.get("rationale"))

        with col_gf:
            st.subheader("Grounded Green Flags")
            for gf in res.get("green_flags", []):
                st.markdown(f"- **{gf.get('claim')}**")
                st.caption(f"Consistent with *{gf.get('principle')}* ({gf.get('source')})")

    with tab_teach:
        st.subheader("Socratic Learning Pack (`teach_pack.md`)")
        teach_md = generate_teach_pack(
            hypothesis_text=st.session_state.get("last_hypothesis", ""),
            blind_guess=st.session_state.get("last_blind_guess", ""),
            verdict=res.get("verdict", ""),
            issues=res.get("issues", []),
            edge_conditions=res.get("edge_conditions", []),
            notebooklm_url=os.environ.get("NOTEBOOKLM_URL", ""),
        )
        st.download_button(
            "📥 Download teach_pack.md",
            teach_md,
            file_name="teach_pack.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.markdown(teach_md)
