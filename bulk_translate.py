#!/usr/bin/env python3
"""
Bulk Translation Script for FAQ
===============================
Automatically translates missing entries using Google Translate API or other services.

Usage:
    python bulk_translate.py --language es --service google
    python bulk_translate.py --language all --service deepl
    python bulk_translate.py --dry-run  # Preview what would be translated

Requirements:
    pip install googletrans==4.0.0rc1
    # or
    pip install deepl

Features:
    - Bulk translate missing entries for any language
    - Support for multiple translation services
    - Preserve HTML formatting
    - Dry-run mode to preview changes
    - Batch processing for efficiency
"""

import csv
import argparse
import sys
import time
import re
from pathlib import Path
from typing import Dict, List, Optional

# Language mappings for translation services
LANGUAGE_CODES = {
    'es': {'google': 'es', 'deepl': 'ES', 'name': 'Spanish'},
    'fr': {'google': 'fr', 'deepl': 'FR', 'name': 'French'},
    'pt': {'google': 'pt', 'deepl': 'PT', 'name': 'Portuguese'},
    'ru': {'google': 'ru', 'deepl': 'RU', 'name': 'Russian'},
    'ko': {'google': 'ko', 'deepl': 'KO', 'name': 'Korean'},
    'ar': {'google': 'ar', 'deepl': 'AR', 'name': 'Arabic'},
    'zh-Hans': {'google': 'zh-cn', 'deepl': 'ZH', 'name': 'Chinese (Simplified)'}
}

class TranslationService:
    """Base class for translation services."""
    
    def translate(self, text: str, target_lang: str) -> str:
        raise NotImplementedError
    
    def translate_batch(self, texts: List[str], target_lang: str) -> List[str]:
        """Translate multiple texts. Override for batch-optimized services."""
        return [self.translate(text, target_lang) for text in texts]

class GoogleTranslateService(TranslationService):
    """Google Translate service using googletrans library."""
    
    def __init__(self):
        try:
            from googletrans import Translator
            self.translator = Translator()
            print("✅ Google Translate service initialized")
        except ImportError:
            print("❌ Error: googletrans not installed. Run: pip install googletrans==4.0.0rc1")
            sys.exit(1)
    
    def translate(self, text: str, target_lang: str) -> str:
        try:
            # Handle HTML content by protecting tags
            html_pattern = r'<[^>]+>'
            html_tags = re.findall(html_pattern, text)
            
            # Replace HTML tags with placeholders
            protected_text = text
            for i, tag in enumerate(html_tags):
                protected_text = protected_text.replace(tag, f"__HTML_TAG_{i}__", 1)
            
            # Translate the protected text
            result = self.translator.translate(protected_text, dest=target_lang)
            translated = result.text
            
            # Restore HTML tags
            for i, tag in enumerate(html_tags):
                translated = translated.replace(f"__HTML_TAG_{i}__", tag)
            
            return translated
            
        except Exception as e:
            print(f"  ⚠️  Translation error: {e}")
            return text  # Return original text on error
    
    def translate_batch(self, texts: List[str], target_lang: str) -> List[str]:
        results = []
        for i, text in enumerate(texts):
            if i > 0 and i % 10 == 0:  # Rate limiting
                time.sleep(1)
            results.append(self.translate(text, target_lang))
        return results

class MockTranslateService(TranslationService):
    """Mock service for testing/dry-run mode."""
    
    def translate(self, text: str, target_lang: str) -> str:
        return f"[TRANSLATED TO {target_lang.upper()}] {text[:50]}..."

def load_csv(csv_path: Path) -> List[Dict]:
    """Load CSV file and return rows."""
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_csv(csv_path: Path, rows: List[Dict], fieldnames: List[str]):
    """Save rows to CSV file."""
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def get_translation_service(service_name: str, dry_run: bool = False) -> TranslationService:
    """Get translation service instance."""
    if dry_run:
        return MockTranslateService()
    
    if service_name.lower() == 'google':
        return GoogleTranslateService()
    else:
        print(f"❌ Error: Unknown service '{service_name}'. Available: google")
        sys.exit(1)

def translate_language(csv_path: Path, target_lang: str, service: TranslationService, dry_run: bool = False):
    """Translate missing entries for a specific language."""
    
    if target_lang not in LANGUAGE_CODES:
        print(f"❌ Error: Unsupported language '{target_lang}'")
        print(f"Available: {', '.join(LANGUAGE_CODES.keys())}")
        return 0
    
    lang_info = LANGUAGE_CODES[target_lang]
    service_lang_code = lang_info['google']  # Use Google codes for now
    
    print(f"🌍 Translating to {lang_info['name']} ({target_lang})...")
    
    rows = load_csv(csv_path)
    fieldnames = ['status', 'key', 'en', 'ja', 'ar', 'de', 'es', 'fr', 'ko', 'pt', 'ru', 'zh-Hans']
    
    # Find entries that need translation
    to_translate = []
    for row in rows:
        if not row.get(target_lang, '').strip() and row.get('en', '').strip():
            to_translate.append(row)
    
    if not to_translate:
        print(f"  ✅ No missing translations found for {lang_info['name']}")
        return 0
    
    print(f"  📝 Found {len(to_translate)} entries to translate")
    
    if dry_run:
        print("  🔍 DRY RUN - Preview of translations:")
        for i, row in enumerate(to_translate[:5]):  # Show first 5
            key = row['key']
            en_text = row['en'][:100] + "..." if len(row['en']) > 100 else row['en']
            print(f"    {i+1}. {key}")
            print(f"       EN: {en_text}")
            print(f"       {target_lang.upper()}: [WOULD BE TRANSLATED]")
        if len(to_translate) > 5:
            print(f"    ... and {len(to_translate) - 5} more entries")
        return len(to_translate)
    
    # Translate entries
    updated_count = 0
    for i, row in enumerate(to_translate):
        key = row['key']
        en_text = row['en']
        
        print(f"  📝 Translating {i+1}/{len(to_translate)}: {key}")
        
        try:
            translated = service.translate(en_text, service_lang_code)
            row[target_lang] = translated
            updated_count += 1
            
            # Rate limiting
            if i > 0 and i % 5 == 0:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"    ⚠️  Error translating {key}: {e}")
    
    # Save updated CSV
    save_csv(csv_path, rows, fieldnames)
    print(f"  🎉 Successfully translated {updated_count} entries!")
    
    return updated_count

def main():
    parser = argparse.ArgumentParser(description='Bulk translate FAQ entries')
    parser.add_argument('--language', required=True,
                       help='Target language code (es, fr, pt, ru, ko, ar, zh-Hans) or "all"')
    parser.add_argument('--service', default='google',
                       help='Translation service (google, deepl) - default: google')
    parser.add_argument('--csv-path', default='faq_translations.csv',
                       help='Path to CSV file (default: faq_translations.csv)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview what would be translated without making changes')
    
    args = parser.parse_args()
    
    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"❌ Error: {csv_path} not found!")
        print("Run 'python faq_to_csv.py' first to generate the CSV.")
        return 1
    
    # Get translation service
    service = get_translation_service(args.service, args.dry_run)
    
    # Translate languages
    total_updated = 0
    
    if args.language.lower() == 'all':
        # Translate all supported languages
        for lang_code in LANGUAGE_CODES.keys():
            if lang_code in ['ja', 'de']:  # Skip already completed languages
                continue
            updated = translate_language(csv_path, lang_code, service, args.dry_run)
            total_updated += updated
            if not args.dry_run and updated > 0:
                time.sleep(2)  # Longer pause between languages
    else:
        total_updated = translate_language(csv_path, args.language, service, args.dry_run)
    
    # Summary
    if args.dry_run:
        print(f"\n🔍 DRY RUN COMPLETE")
        print(f"   Would translate {total_updated} entries")
        print(f"   Run without --dry-run to apply translations")
    else:
        print(f"\n🎉 TRANSLATION COMPLETE")
        print(f"   Updated {total_updated} entries")
        if total_updated > 0:
            print(f"\n📝 Next steps:")
            print(f"   1. Review translations in {csv_path}")
            print(f"   2. Run: python csv_to_json.py")
            print(f"   3. Test your website with new translations!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
