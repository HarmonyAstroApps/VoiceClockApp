#!/usr/bin/env python3
"""
FAQ Translation: JSON → CSV
============================
Reads en.json (source of truth) + all language JSON files.
Generates faq_translations.csv with untranslated strings at the top.

Usage:
    python faq_to_csv.py

Output:
    faq_translations.csv (open in Google Sheets or Excel)
"""
import json
import csv
import os
from pathlib import Path

LANGUAGES = ["en", "ja", "ar", "de", "es", "fr", "ko", "pt", "ru", "zh-Hans"]
FAQ_DIR = Path(__file__).parent / "src" / "faq-translations"
OUTPUT_CSV = Path(__file__).parent / "faq_translations.csv"


def flatten_json(obj, prefix=""):
    """Flatten nested JSON into dot-notation keys, preserving order."""
    items = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            items.extend(flatten_json(v, new_key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{prefix}.{i}"
            items.extend(flatten_json(v, new_key))
    else:
        # Convert value to string, preserving HTML content
        items.append((prefix, str(obj)))
    return items


def load_lang(lang):
    """Load a language JSON file and return flattened key-value dict."""
    path = FAQ_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return dict(flatten_json(data))


def main():
    print("=" * 60)
    print("  FAQ Translation: JSON → CSV")
    print("=" * 60)

    if not (FAQ_DIR / "en.json").exists():
        print(f"\n❌ Error: {FAQ_DIR / 'en.json'} not found!")
        print("  English is the source of truth. Please create en.json first.")
        return

    # Load all languages
    lang_data = {}
    for lang in LANGUAGES:
        lang_data[lang] = load_lang(lang)
        count = len(lang_data[lang])
        status = "✅" if count > 0 else "⬜"
        print(f"  {status} {lang:>8}: {count} strings loaded")

    # English keys are the source of truth
    en_keys = list(lang_data["en"].keys())
    print(f"\n📋 Source of truth (en.json): {len(en_keys)} translatable strings")

    # Skip structural keys (like section IDs, icons) that shouldn't be translated
    skip_patterns = [".id", ".icon"]

    # Build rows
    rows = []
    for key in en_keys:
        # Skip non-translatable keys
        if any(key.endswith(p) for p in skip_patterns):
            continue

        row = {"key": key}
        missing_langs = []
        for lang in LANGUAGES:
            value = lang_data[lang].get(key, "")
            row[lang] = value
            if lang != "en" and not value.strip():
                missing_langs.append(lang)

        total_other = len(LANGUAGES) - 1  # exclude English
        translated = total_other - len(missing_langs)

        if len(missing_langs) == 0:
            row["status"] = "✅"
        elif len(missing_langs) == total_other:
            row["status"] = "⚠️ NEW"
        else:
            row["status"] = f"🔶 {translated}/{total_other}"

        rows.append(row)

    # Sort: untranslated first (NEW), then partial, then fully translated
    def sort_key(r):
        if r["status"] == "⚠️ NEW":
            return (0, r["key"])
        elif r["status"] == "✅":
            return (2, r["key"])
        else:
            return (1, r["key"])

    rows.sort(key=sort_key)

    # Write CSV with BOM for Excel compatibility
    fieldnames = ["status", "key"] + LANGUAGES
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Print stats
    new_count = sum(1 for r in rows if r["status"] == "⚠️ NEW")
    partial_count = sum(1 for r in rows if r["status"].startswith("🔶"))
    done_count = sum(1 for r in rows if r["status"] == "✅")
    total = len(rows)

    print(f"\n{'─' * 40}")
    print(f"  📊 Translation Status")
    print(f"{'─' * 40}")
    print(f"  ⚠️  Untranslated (NEW):  {new_count}")
    print(f"  🔶 Partially translated: {partial_count}")
    print(f"  ✅ Fully translated:     {done_count}")
    print(f"  📝 Total strings:        {total}")
    print(f"{'─' * 40}")
    print(f"\n✅ Generated: {OUTPUT_CSV}")
    print(f"\n📝 Next steps:")
    print(f"   1. Open {OUTPUT_CSV.name} in Google Sheets or Excel")
    print(f"   2. Fill in empty cells (⚠️ NEW rows are at the top)")
    print(f"   3. Save/download as CSV")
    print(f"   4. Run: python csv_to_json.py")


if __name__ == "__main__":
    main()

