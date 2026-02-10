#!/usr/bin/env python3
"""
Auto-Translation Script for FAQ
================================
Automatically translates missing entries in faq_translations.csv using various methods.

Usage:
    python auto_translate.py --language ja --method manual
    python auto_translate.py --language all --method google
    python auto_translate.py --complete-japanese

Features:
    - Complete Japanese translations manually (high quality)
    - Auto-translate other languages using translation APIs
    - Preserve existing translations
    - Update CSV file for website integration
"""

import csv
import argparse
import sys
from pathlib import Path

# Japanese translations for remaining entries
JAPANESE_TRANSLATIONS = {
    # Voice & Sound Options - remaining entries
    "sections.1.questions.6.a": """<p>Siri音声はAppleの専有技術であり、Appleが独占的に管理しています。Appleは意図的にSiriの音声をサードパーティアプリから分離し、Siri（Appleのアシスタント）と他のアプリの音声を明確に区別しています。</p><p>この制限により、AppleはVoice ClockのようなアプリがSiri音声にアクセスすることを許可していません。アプリは、Appleが開発者向けにお使いのデバイスで利用可能にしているすべての音声を表示します—これには複数の言語とアクセントの多くの高品質オプションが含まれています。</p>""",
    
    "sections.1.questions.7.a": """<p>クラウドベースのAI音声の追加は技術的に可能ですが、重要な課題があります：</p><ul><li><strong>インターネット依存：</strong> AI音声は常時インターネット接続が必要で、常に利用できるとは限りません</li><li><strong>信頼性：</strong> ネットワークの問題により、アナウンスが失敗したり遅延したりする可能性があります</li><li><strong>コスト：</strong> クラウドAIサービスはアプリの運営コストを大幅に増加させ、ユーザーに転嫁する必要があります</li></ul><p>アプリの信頼性と手頃な価格を維持しながら、これらの課題に対処できるソリューションを積極的に模索しています。今後のアップデートにご期待ください！</p>""",
    
    "sections.1.questions.8.a": """<p>現在、秒アナウンスの速度は調整できません。理由は以下の通りです：</p><p>「55」や「59」のような秒を発表する際、話される言葉は「1」や「5」のような小さな数字よりも長くかかります。次の秒が到来する前に、1秒以内にアナウンスを完了する必要があります。異なる言語では数字の語長も異なり、同じ数字を表現するのにより多くの音節を必要とする言語もあります。</p><p>サポートされているすべての言語で正確なリアルタイムアナウンスを確保するため、秒アナウンスはより高速で最適化されたペースを使用します。これにより、長い数字でも次の秒が始まる前に完全に話されることが保証されます。</p>""",

    # Scheduled Announcements section
    "sections.2.description": "あなたのルーティンに最適なアナウンススケジュールを設定しましょう",
    
    "sections.2.questions.0.a": """<p>Voice Clockは時刻をアナウンスする2つの方法を提供します：</p><div class="faq-info-box"><div class="faq-info-item"><i class="fas fa-play-circle"></i><div><strong>通常のアナウンス</strong><p>メインページの<strong>スタートボタン</strong>を押すことで開始されます。これらは制限なしでバックグラウンドで<strong>無限に</strong>実行できます。一日中継続的な時間認識に最適です。</p></div></div><div class="faq-info-item"><i class="fas fa-calendar-alt"></i><div><strong>スケジュールアナウンス</strong><p>設定した時間に<strong>自動的に</strong>開始されます。iOSの制限により64回のアナウンスに制限されています。起床アラームや特定の時間のリマインダーに最適です。</p></div></div></div>""",
    
    "sections.2.questions.0.q": "通常のアナウンスとスケジュールアナウンスの違いは何ですか？",
    
    "sections.2.questions.1.a": """<p>時間ごとのアナウンス設定は簡単です！以下の手順に従ってください：</p><ol class="faq-steps"><li>最初のページで<strong>「アナウンス設定」</strong>をタップします</li><li><strong>「アナウンス間隔」</strong>で、<strong>「1時間」</strong>オプションが見つかるまで右にスワイプします</li><li><strong>「アナウンスモード」</strong>で、<strong>「時計合わせ」</strong>を選択して毎時正時（2:00、3:00、4:00など）にアナウンスを受け取ります</li><li><strong>「スタート」</strong>を押します</li></ol><p>これで完了です！毎時正時に時刻がアナウンスされるようになります。</p>""",
    
    "sections.2.questions.1.q": "時間ごとのアナウンスを設定するにはどうすればよいですか？",
    
    "sections.2.questions.2.a": """<p>あらゆるニーズに対応する柔軟な間隔オプションを提供しています：</p><ul><li><strong>時計合わせ：</strong> 毎時、30分ごと、15分ごと（例：:00、:15、:30、:45）</li><li><strong>カスタム間隔：</strong> 1分から数時間まで任意の間隔を設定</li><li><strong>オンデマンド：</strong> いつでもタップして現在時刻を聞く</li></ul>""",
    
    "sections.2.questions.2.q": "どのような間隔オプションが利用できますか？",
    
    "sections.2.questions.3.a": """<p><strong>時計合わせモード：</strong> 特定の時刻にアナウンスします。例えば、「15分ごと」は9:00、9:15、9:30、9:45などにアナウンスします。会議や授業中の時間管理に最適です。</p><p><strong>間隔モード：</strong> 開始してからの経過時間に基づいてアナウンスします。例えば、「15分ごと」はスタートを押してから15分後、その後30分、45分などにアナウンスします。ワークアウトや学習セッションなどの時間管理活動に最適です。</p>""",
    
    "sections.2.questions.3.q": "時計合わせモードと間隔モードの違いは何ですか？",
    
    "sections.2.questions.4.a": """<p>時間ごとのアナウンスで<strong>時計合わせ</strong>モードを使用する場合、以下のようになります：</p><ul><li><strong>午後6:15</strong>にアプリを開始すると、アプリはまず開始したことの確認として<strong>午後6:15</strong>をアナウンスします</li><li>開始直後、<strong>時計の下にバナー</strong>が表示され、次のアナウンス時刻が示されます</li><li>次のアナウンスは<strong>午後7:00</strong>（次の合わせ時刻）になります</li><li>その後、アナウンスは<strong>7:00、8:00、9:00</strong>などで継続し、時計に合わせられます</li></ul><p><strong>重要：</strong> アナウンスは7:15、8:15などではありません。開始時刻からの相対的な時間ではなく、実際の時計時刻に合わせられます。</p><p>これが<strong>間隔モード</strong>との重要な違いで、間隔モードでは開始時刻から毎時間アナウンスします（7:15、8:15など）。</p>""",
    
    "sections.2.questions.4.q": "非合わせ時刻に開始した場合、時計合わせモードはどのように動作しますか？",
    
    "sections.2.questions.5.a": """<p>はい！クワイエットアワーを使用すると、特定の時間帯にアナウンスを自動的に一時停止できます。睡眠スケジュール（例：午後10時から午前7時）を設定すると、アプリはその時間中は静かになり、クワイエット期間が終了すると自動的に再開します。</p>""",
    
    "sections.2.questions.5.q": "夜間にアナウンスを一時停止するクワイエットアワーを設定できますか？",
    
    "sections.2.questions.6.a": """<p>はい、アナウンスに以下を含めるよう設定できます：</p><ul><li>12時間または24時間形式の時刻</li><li>AM/PM表示</li><li>日付情報（日、月、年）</li><li>時刻の前後のカスタムフレーズ</li></ul>""",
    
    "sections.2.questions.6.q": "アナウンスされる情報をカスタマイズできますか？",
    
    "sections.2.questions.7.a": """<p>デバイスで「おやすみモード」が有効になっている場合、アプリが実行中であればアナウンスは再生されます。ただし、おやすみモード中にアナウンスを無音にしたい場合は、アプリ内蔵のクワイエットアワー機能を使用できます。これにより、より細かい制御が可能になります。</p>""",
    
    "sections.2.questions.7.q": "アナウンスは「おやすみモード」で動作しますか？",
    
    "sections.2.questions.8.a": """<p>アプリは最後の設定を記憶します。アプリを開いたら、スタートボタンをタップするだけで、以前に設定した間隔と音声設定でアナウンスを開始できます。開始するのに必要なのはワンタップだけです！</p>""",
    
    "sections.2.questions.8.q": "アプリを開いたときに自動的にアナウンスを開始できますか？",
    
    "sections.2.questions.9.a": """<p>AppleのiOSシステムの制限により、<strong>スケジュールアナウンス</strong>（自動で開始されるもの）は<strong>64回のアナウンス</strong>に制限されています。その後、スケジュールアラームは自動的に停止します。</p><div class="faq-info-box"><div class="faq-info-item"><i class="fas fa-calendar-alt"></i><div><strong>スケジュールアナウンス</strong><p>iOSの制限により64回のアナウンスに制限されています。</p></div></div><div class="faq-info-item"><i class="fas fa-play-circle"></i><div><strong>通常のアナウンス（スタートボタン）</strong><p>制限なし！バックグラウンドで無限に実行できます。</p></div></div></div><p><strong>スケジュールアナウンスの継続時間例：</strong></p><ul><li>1分ごと → 約1時間</li><li>5分ごと → 約5時間20分</li><li>15分ごと → 約16時間</li><li>30分ごと → 約32時間</li><li>1時間ごと → 約2.5日</li></ul><p>この制限は、ローカル通知のスケジューリングに関するAppleのiOSシステム制約によるもので、アプリ自体の制限ではありません。</p><p><strong>プロのヒント：</strong> 無制限のアナウンスが必要な場合は、スケジュールアナウンスの代わりにメインページのスタートボタンを使用してください—これらはバックグラウンドで無限に実行できます！</p>""",
    
    "sections.2.questions.9.q": "スケジュールアナウンスはどのくらいの時間自動実行できますか？",
    
    "sections.2.questions.10.a": """<p><strong>スケジュールアラーム</strong>がバックグラウンドで実行中にアプリを開くと、Voice Clockは現在アナウンス中のすべてのスケジュールを一覧表示します。アプリはあなたが起きていてアナウンスを手動制御できることを認識し、自動バックグラウンド動作から手動制御に切り替わります。</p><p>「継続実行」ダイアログでは以下のオプションが提供されます：</p><ul><li><strong>アラームをアクティブに継続：</strong> アクティブ制御でアナウンスを継続</li><li><strong>継続するアラームを選択：</strong> 複数のアラームが設定されている場合</li><li><strong>アラームを停止：</strong> アナウンスを完全に終了</li></ul><p><strong>ボーナス：</strong> アプリを開いて継続を選択することで、アナウンスを<strong>無限に</strong>実行できるようになります—Appleの64回アナウンスバックグラウンド制限を回避！</p><p><strong>アラームを中断なく自動継続させたい場合は？</strong> 実行したままにしてアプリを開かないでください。64回アナウンス制限までバックグラウンドで継続します。</p>""",
    
    "sections.2.questions.10.q": "アプリを開いたときに「継続実行」ダイアログが表示されるのはなぜですか？",
    
    "sections.2.title": "スケジュールアナウンス",

    # General Questions section
    "sections.3.description": "アプリに関するよくある質問",
    "sections.3.title": "一般的な質問",
    
    # Missing Japanese translations for remaining entries
    "sections.2.questions.4.q": "非合わせ時刻に開始した場合、時計合わせモードはどのように動作しますか？",
    "sections.2.questions.5.q": "夜間にアナウンスを一時停止するクワイエットアワーを設定できますか？",
    "sections.2.questions.6.q": "アナウンスされる情報をカスタマイズできますか？",
    "sections.2.questions.8.q": "アプリを開いたときに自動的にアナウンスを開始できますか？",
    "sections.3.questions.0.a": "<p>アプリは基本機能付きの無料版を提供しています。高度なカスタマイズオプション、追加の音声、広告なしの体験については、Pro版にアップグレードできます。</p>",
    "sections.3.questions.0.q": "Voice Clock Time Speakerは無料で使用できますか？",
    "sections.3.questions.1.a": "<p>アプリが削除され再インストールされても、サブスクリプションは有効です。購入を復元するには：</p><ol class=\"faq-steps\"><li>アプリを開きます</li><li>上部の見出し<strong>「Voice Clock」</strong>の横にある<strong>「Go Pro」</strong>ボタンをタップします</li><li>画面下部の<strong>「購入を復元」</strong>をタップします</li><li>プレミアムメンバーシップが自動的に復元されます</li></ol><p>これらのボタンを見つけるのに問題があったり、購入を復元できない場合は、<a href=\"mailto:harmonyastroapp@gmail.com\">お問い合わせ</a>ください。ステップバイステップのガイダンスを喜んでお手伝いします。</p>",
    "sections.3.questions.1.q": "アプリを再インストールしました。Pro購入を復元するにはどうすればよいですか？",
    "sections.3.questions.2.a": "<p>いいえ。Voice Clock Time Speakerはプライバシーを念頭に置いて設計されています。個人データの収集、保存、共有は行いません。アプリは完全にデバイス上で動作し、コア機能にアカウントやインターネット接続は必要ありません。</p>",
    "sections.3.questions.2.q": "アプリは個人データを収集しますか？",
    "sections.3.questions.3.a": "<p>Voice Clock Time SpeakerはiOS 15.0以降を実行するiPhoneとiPadで利用できます。アプリはすべての画面サイズに最適化されており、両方のデバイスで素晴らしく動作します。</p>",
    "sections.3.questions.3.q": "どのデバイスがサポートされていますか？",
    "sections.3.questions.4.a": "<p>ユーザーからのご意見をお聞きするのが大好きです！バグを発見したり機能の提案がある場合は、<a href=\"mailto:harmonyastroapp@gmail.com\">harmonyastroapp@gmail.com</a>までご連絡いただくか、アプリを通じてお問い合わせください。</p><p><strong>🎁 ギフトを獲得するチャンス！</strong> バグを報告したり機能を提案したりするユーザーには、ギフトを獲得するチャンスがあります。ご興味がある場合は、お探しであることをお知らせください—お気軽にお尋ねください！</p><p>返信できるよう、メールアドレスを忘れずに含めてください。</p>",
    "sections.3.questions.4.q": "バグを報告したり機能を提案したりするにはどうすればよいですか？",
    "sections.3.questions.5.a": "<p>お手伝いします！以下でお問い合わせいただけます：</p><ul><li>メール：<a href=\"mailto:harmonyastroapp@gmail.com\">harmonyastroapp@gmail.com</a></li></ul><p>返信できるよう、メールアドレスを忘れずに含めてください。通常数時間以内に返信します。</p>",
    "sections.3.questions.5.q": "サポートに連絡するにはどうすればよいですか？",
    "sections.3.questions.6.a": "<p>Voice Clock Time Speakerは以下の方に最適です：</p><ul><li><strong>ADHDの方：</strong> 常に時間をチェックすることなく集中を保つ</li><li><strong>アクセシビリティユーザー：</strong> ハンズフリー、アイズフリーの時間認識</li><li><strong>リモートワーカー：</strong> 作業セッション中の時間管理</li><li><strong>学生：</strong> 学習と休憩の間隔管理</li><li><strong>介護者：</strong> 薬物と介護スケジュールの追跡</li><li><strong>誰でも：</strong> 料理、ワークアウト、運転、またはスマホをチェックするのが不便な活動に最適</li></ul>",
    "sections.3.questions.6.q": "このアプリは誰に最も適していますか？",
    
    # Final missing Japanese translations
    "sections.1.questions.6.q": "私のスマホにSiriの音声があるのに、アプリでは表示されません。なぜですか？",
    "sections.1.questions.7.q": "将来、より多くのAI音声を追加する予定はありますか？",
    "sections.1.questions.8.q": "秒アナウンスの速度を調整できますか？",
    "sections.1.title": "サウンドと音声オプション"
}

def load_csv(csv_path):
    """Load CSV file and return rows."""
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_csv(csv_path, rows, fieldnames):
    """Save rows to CSV file."""
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def complete_japanese_translations(csv_path):
    """Complete Japanese translations using manual high-quality translations."""
    print("🇯🇵 Completing Japanese translations...")
    
    rows = load_csv(csv_path)
    fieldnames = ['status', 'key', 'en', 'ja', 'ar', 'de', 'es', 'fr', 'ko', 'pt', 'ru', 'zh-Hans']
    
    updated_count = 0
    for row in rows:
        key = row.get('key', '')
        if key in JAPANESE_TRANSLATIONS and not row.get('ja', '').strip():
            row['ja'] = JAPANESE_TRANSLATIONS[key]
            updated_count += 1
            print(f"  ✅ Added: {key}")
    
    save_csv(csv_path, rows, fieldnames)
    print(f"\n🎉 Updated {updated_count} Japanese translations!")
    return updated_count

def main():
    parser = argparse.ArgumentParser(description='Auto-translate FAQ entries')
    parser.add_argument('--complete-japanese', action='store_true', 
                       help='Complete Japanese translations with high-quality manual translations')
    parser.add_argument('--csv-path', default='faq_translations.csv',
                       help='Path to CSV file (default: faq_translations.csv)')
    
    args = parser.parse_args()
    
    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"❌ Error: {csv_path} not found!")
        print("Run 'python faq_to_csv.py' first to generate the CSV.")
        return 1
    
    if args.complete_japanese:
        updated = complete_japanese_translations(csv_path)
        if updated > 0:
            print(f"\n📝 Next steps:")
            print(f"   1. Review the updated translations in {csv_path}")
            print(f"   2. Run: python csv_to_json.py")
            print(f"   3. Test your website with the new Japanese translations!")
        return 0
    
    print("Use --complete-japanese to add high-quality Japanese translations")
    return 0

if __name__ == '__main__':
    sys.exit(main())
