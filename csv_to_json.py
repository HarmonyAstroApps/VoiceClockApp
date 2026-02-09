#!/usr/bin/env python3
"""
FAQ Translation: CSV → JSON
============================
Reads faq_translations.csv and generates/updates all language JSON files.

Usage:
    python csv_to_json.py

Input:
    faq_translations.csv (edited with translations)

Output:
    src/faq-translations/{lang}.json for each language
"""
import json
import csv
import os
from pathlib import Path

LANGUAGES = ["en", "ja", "ar", "de", "es", "fr", "ko", "pt", "ru", "zh-Hans"]
FAQ_DIR = Path(__file__).parent / "src" / "faq-translations"
INPUT_CSV = Path(__file__).parent / "faq_translations.csv"


def set_nested(obj, keys, value):
    """Set a value in a nested dict/list structure using a list of keys."""
    for i, key in enumerate(keys[:-1]):
        next_key = keys[i + 1]
        is_next_index = next_key.isdigit()

        if key.isdigit():
            key = int(key)
            # Ensure list is long enough
            if isinstance(obj, list):
                while len(obj) <= key:
                    obj.append([] if is_next_index else {})
                obj = obj[key]
            else:
                raise ValueError(f"Expected list but got {type(obj)} at key {key}")
        else:
            if isinstance(obj, dict):
                if key not in obj:
                    obj[key] = [] if is_next_index else {}
                obj = obj[key]
            elif isinstance(obj, list):
                raise ValueError(f"Expected dict but got list at key {key}")

    # Set the final value
    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)
        if isinstance(obj, list):
            while len(obj) <= last_key:
                obj.append(None)
            obj[last_key] = value
    else:
        if isinstance(obj, dict):
            obj[last_key] = value


def main():
    print("=" * 60)
    print("  FAQ Translation: CSV → JSON")
    print("=" * 60)

    if not INPUT_CSV.exists():
        print(f"\n❌ Error: {INPUT_CSV} not found!")
        print("  Run 'python faq_to_csv.py' first to generate the CSV.")
        return

    FAQ_DIR.mkdir(parents=True, exist_ok=True)

    # Read CSV
    with open(INPUT_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"\n📋 Read {len(rows)} rows from {INPUT_CSV.name}")

    # Also load en.json to preserve structural keys (id, icon)
    en_path = FAQ_DIR / "en.json"
    en_structure = {}
    if en_path.exists():
        with open(en_path, "r", encoding="utf-8") as f:
            en_structure = json.load(f)

    # Build JSON for each language
    stats = {}
    for lang in LANGUAGES:
        result = {}
        filled = 0
        empty = 0

        for row in rows:
            key = row.get("key", "").strip()
            value = row.get(lang, "").strip()

            if not key:
                continue

            if value:
                keys = key.split(".")
                try:
                    set_nested(result, keys, value)
                    filled += 1
                except (ValueError, IndexError) as e:
                    print(f"  ⚠️  Warning: Could not set {key} for {lang}: {e}")
            else:
                empty += 1

        # Restore structural fields (id, icon) from English structure
        if "sections" in en_structure and "sections" in result:
            for i, en_section in enumerate(en_structure.get("sections", [])):
                if i < len(result.get("sections", [])):
                    section = result["sections"][i]
                    if isinstance(section, dict):
                        if "id" in en_section:
                            section["id"] = en_section["id"]
                        if "icon" in en_section:
                            section["icon"] = en_section["icon"]

        # Write JSON file
        output_path = FAQ_DIR / f"{lang}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        stats[lang] = {"filled": filled, "empty": empty}

    # Print stats
    print(f"\n{'─' * 60}")
    print(f"  {'Language':<12} {'Translated':<14} {'Missing':<10} {'Progress'}")
    print(f"{'─' * 60}")

    for lang in LANGUAGES:
        s = stats[lang]
        total = s["filled"] + s["empty"]
        pct = (s["filled"] / total * 100) if total > 0 else 0
        bar_filled = int(pct / 5)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        emoji = "✅" if pct == 100 else ("🔶" if pct > 0 else "⬜")
        print(f"  {emoji} {lang:<10} {s['filled']:<14} {s['empty']:<10} {bar} {pct:.0f}%")

    print(f"{'─' * 60}")
    print(f"\n✅ All language JSON files updated in: {FAQ_DIR}/")
    print(f"\n📝 Files generated:")
    for lang in LANGUAGES:
        path = FAQ_DIR / f"{lang}.json"
        size = path.stat().st_size if path.exists() else 0
        print(f"   {'📄'} {lang}.json ({size:,} bytes)")


if __name__ == "__main__":
    main()

