"""CLI entry point for Sanity_Engine_Cached.

Usage:
    python run.py --hypothesis "My hypothesis text..." [--blind-guess "Diffusion is too slow"] [--teach] [--model gemini-2.5-flash]
"""

import argparse
import json
import os
import sys

from engine import SanityEngineCached
from teach import generate_teach_pack


def main():
    parser = argparse.ArgumentParser(description="Sanity Engine Cached: Gemini Long-Context Scientific Auditor")
    parser.add_argument("--hypothesis", type=str, required=True, help="Hypothesis text or path to hypothesis file")
    parser.add_argument("--blind-guess", type=str, default="", help="Your pre-audit intuition on the top bottleneck")
    parser.add_argument("--teach", action="store_true", help="Generate teach_pack.md Socratic learning pack")
    parser.add_argument("--model", type=str, default="gemini-3.8-flash", help="Gemini model tier (default: gemini-3.8-flash)")
    parser.add_argument("--explicit-cache", action="store_true", help="Use explicit cache creation instead of implicit caching")
    parser.add_argument("--out", type=str, default="out", help="Directory to save audit report and teach pack")
    args = parser.parse_args()

    # Load hypothesis text
    if os.path.exists(args.hypothesis):
        with open(args.hypothesis, "r", encoding="utf-8") as f:
            hypo_text = f.read()
    else:
        hypo_text = args.hypothesis

    print("=" * 70)
    print(" SANITY ENGINE CACHED: GEMINI LONG-CONTEXT AUDITOR")
    print(f" Model: {args.model}")
    print("=" * 70)

    engine = SanityEngineCached(
        corpus_dir="corpus",
        model_name=args.model,
        use_explicit_cache=args.explicit_cache,
    )

    print(f"[+] Loaded ~{engine.prefix_tokens:,} tokens into reference context.")
    print("[*] Running Level 0 Math Firewall & Adversarial Review...")

    result = engine.evaluate_hypothesis(
        hypothesis_text=hypo_text,
        blind_guess=args.blind_guess,
    )

    os.makedirs(args.out, exist_ok=True)
    report_path = os.path.join(args.out, "audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\n" + "=" * 70)
    print(f" VERDICT: {result['verdict']} (Confidence: {result['confidence']}%)")
    print("=" * 70)
    print(f"\nSummary:\n{result['summary']}\n")

    print(f"[-] Identified Vulnerabilities ({len(result['issues'])}):")
    for idx, iss in enumerate(result["issues"], 1):
        verified_mark = "✅ Verified" if iss.get("verified") else "⚠️ Unverified"
        print(f"  {idx}. [{iss.get('severity')}] {iss.get('claim')}")
        print(f"     Law: {iss.get('physical_law')}")
        print(f"     Source: {iss.get('source')} ({verified_mark})")
        print(f"     Quote: \"{iss.get('quote')}\"\n")

    if result.get("edge_conditions"):
        print("[-] Required Edge Conditions:")
        for ec in result["edge_conditions"]:
            print(f"  • {ec.get('parameter')}: {ec.get('threshold')} ({ec.get('rationale')})")

    if args.teach:
        teach_text = generate_teach_pack(
            hypothesis_text=hypo_text,
            blind_guess=args.blind_guess,
            verdict=result["verdict"],
            issues=result["issues"],
            edge_conditions=result.get("edge_conditions", []),
            notebooklm_url=os.environ.get("NOTEBOOKLM_URL", ""),
        )
        teach_path = os.path.join(args.out, "teach_pack.md")
        with open(teach_path, "w", encoding="utf-8") as f:
            f.write(teach_text)
        print(f"\n[+] Socratic Teaching Pack generated: {teach_path}")

    print(f"[+] Full JSON Report written to: {report_path}")


if __name__ == "__main__":
    main()
