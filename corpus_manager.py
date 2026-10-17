"""Corpus Manager for Sanity_Engine_Cached.

Handles:
1. Sizing and packing the canonical textbook library for Gemini Context Caching.
   - Profile 'cached_500k' (~500k tokens) for Paid / Pay-as-you-go tiers.
   - Profile 'free_tier_200k' (~180k tokens) for Google AI Studio Free Tier (250k token/min limit).
2. Programmatic Quote-and-Locate verification against local plain-text files.
"""

import glob
import os
import re
from typing import Dict, List, Optional, Tuple


class CorpusManager:
    """Manages textbook text files, contextual front-loading, and quote verification."""

    def __init__(self, corpus_dir: str = "corpus", profile: str = "cached_500k"):
        self.corpus_dir = corpus_dir
        self.profile = profile
        self.files: Dict[str, str] = {}
        self.load_corpus()

    def load_corpus(self):
        """Load text files from corpus/ into memory for fast lookup and verification."""
        for path in sorted(glob.glob(os.path.join(self.corpus_dir, "*.txt"))):
            base = os.path.basename(path)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    self.files[base] = f.read()
            except Exception as e:
                print(f"[!] Warning: Could not read {path}: {e}")

    def build_cached_prefix(self) -> Tuple[str, int]:
        """Assembles the canonical reference library string to front-load into Gemini."""
        sections: List[str] = []
        current_words = 0

        if self.profile == "free_tier_200k":
            # Fits within the 250k tokens/min limit on Google AI Studio Free Tier (~130k words)
            priority_files = [
                "Berg_Random_Walks_in_Biology_1993.txt",
                "Johnston_Foundations_of_Cellular_Neurophysiology_1ed_1995.txt",
                "Winter_Biomechanics_and_Motor_Control_of_Human_Movement_5ed_2020.txt",
                "Feynman_Lectures_on_Physics_Vol1_1963.txt",
                "Strogatz_Nonlinear_Dynamics_and_Chaos_3ed_2024.txt",
                "Murray_Mathematical_Biology_an_Introduction_2ed_1993.txt",
            ]
            quotas = {
                "Berg_Random_Walks_in_Biology_1993.txt": 25_000,
                "Johnston_Foundations_of_Cellular_Neurophysiology_1ed_1995.txt": 30_000,
                "Winter_Biomechanics_and_Motor_Control_of_Human_Movement_5ed_2020.txt": 25_000,
                "Feynman_Lectures_on_Physics_Vol1_1963.txt": 25_000,
                "Strogatz_Nonlinear_Dynamics_and_Chaos_3ed_2024.txt": 20_000,
                "Murray_Mathematical_Biology_an_Introduction_2ed_1993.txt": 15_000,
            }
        else:
            # Full 500k token cached profile for Paid/Pay-as-you-go tiers (~375k words)
            priority_files = [
                "Berg_Random_Walks_in_Biology_1993.txt",
                "Johnston_Foundations_of_Cellular_Neurophysiology_1ed_1995.txt",
                "Winter_Biomechanics_and_Motor_Control_of_Human_Movement_5ed_2020.txt",
                "Strogatz_Nonlinear_Dynamics_and_Chaos_3ed_2024.txt",
                "Cover_Elements_of_Information_Theory_2ed_2006.txt",
                "Murray_Mathematical_Biology_an_Introduction_2ed_1993.txt",
                "Feynman_Lectures_on_Physics_Vol1_1963.txt",
                "Feynman_Lectures_on_Physics_Vol2_1964.txt",
                "Alberts_Molecular_Biology_of_the_Cell_7ed_2022.txt",
                "Nelson_Lehninger_Principles_of_Biochemistry_8ed_2021.txt",
                "Kreyszig_Advanced_Engineering_Mathematics_10ed_2011.txt",
            ]
            quotas = {
                "Berg_Random_Walks_in_Biology_1993.txt": 25_000,
                "Johnston_Foundations_of_Cellular_Neurophysiology_1ed_1995.txt": 55_000,
                "Winter_Biomechanics_and_Motor_Control_of_Human_Movement_5ed_2020.txt": 35_000,
                "Strogatz_Nonlinear_Dynamics_and_Chaos_3ed_2024.txt": 40_000,
                "Cover_Elements_of_Information_Theory_2ed_2006.txt": 35_000,
                "Murray_Mathematical_Biology_an_Introduction_2ed_1993.txt": 35_000,
                "Feynman_Lectures_on_Physics_Vol1_1963.txt": 40_000,
                "Feynman_Lectures_on_Physics_Vol2_1964.txt": 30_000,
                "Alberts_Molecular_Biology_of_the_Cell_7ed_2022.txt": 40_000,
                "Nelson_Lehninger_Principles_of_Biochemistry_8ed_2021.txt": 35_000,
                "Kreyszig_Advanced_Engineering_Mathematics_10ed_2011.txt": 20_000,
            }

        header = (
            "================================================================================\n"
            "CANONICAL SCIENTIFIC REFERENCE CORPUS (FOUNDATIONAL TEXTBOOK LIBRARY)\n"
            "Authoritative theorems, physical laws, boundary conditions, and experimental limits.\n"
            "================================================================================\n\n"
        )
        sections.append(header)

        for filename in priority_files:
            text = self.files.get(filename, "")
            if not text:
                continue

            max_words = quotas.get(filename, 25_000)
            words = text.split()
            trimmed_text = " ".join(words[:max_words])

            book_title = filename.replace(".txt", "").replace("_", " ")
            section = (
                f"### START TEXTBOOK: {book_title} ###\n"
                f"{trimmed_text}\n"
                f"### END TEXTBOOK: {book_title} ###\n\n"
            )
            sections.append(section)
            current_words += len(trimmed_text.split())

        combined_text = "".join(sections)
        estimated_tokens = int(current_words * 1.33)
        return combined_text, estimated_tokens

    def verify_quote(self, quote: str, source_hint: Optional[str] = None) -> Tuple[bool, str, float]:
        """Programmatically checks if a quote exists verbatim in the local corpus files."""
        clean_q = re.sub(r"\s+", " ", quote.strip().lower())
        if len(clean_q) < 15:
            return False, "", 0.0

        candidates = [source_hint] if source_hint and source_hint in self.files else list(self.files.keys())

        # Exact substring check
        for fname in candidates:
            content = self.files[fname]
            clean_content = re.sub(r"\s+", " ", content.lower())
            if clean_q in clean_content:
                return True, fname, 1.0

        # Normalized punctuation check
        norm_q = re.sub(r"[^\w\s]", "", clean_q)
        for fname in candidates:
            content = self.files[fname]
            norm_content = re.sub(r"[^\w\s]", "", re.sub(r"\s+", " ", content.lower()))
            if norm_q in norm_content:
                return True, fname, 0.95

        # Sub-phrase match
        words = norm_q.split()
        if len(words) >= 8:
            prefix = " ".join(words[:8])
            for fname in candidates:
                content = self.files[fname]
                norm_content = re.sub(r"[^\w\s]", "", re.sub(r"\s+", " ", content.lower()))
                if prefix in norm_content:
                    return True, fname, 0.85

        return False, "", 0.0
