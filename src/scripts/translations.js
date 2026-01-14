const translations = {
    en: {
        nav: {
            features: "Features",
            download: "Download",
            contact: "Contact",
            privacy: "Privacy",
            faq: "FAQ"
        },
        hero: {
            subtitle: "Hands-Free Time Management",
            description: "Eyes free, hands free, stress free. Get time updates while focusing on what matters most. Perfect for ADHD, accessibility, multitasking, and everyday life scenarios.",
            downloadNow: "Download Now",
            learnMore: "Learn More"
        },
        benefits: {
            title: "How Voice Clock Time Speaker Enhances Your Day",
            adhdTitle: "For ADHD & Remote Workers",
            adhd1: "Stay focused without checking your phone",
            adhd2: "Time-block your work effectively",
            adhd3: "Never lose track of time again",
            accessibilityTitle: "For Accessibility Users",
            accessibility1: "Crystal clear voice announcements",
            accessibility2: "Hands-free time awareness",
            accessibility3: "15+ language options with native voices",
            everydayTitle: "For Everyday Life",
            everyday1: "Perfect for shower, cooking, or workouts",
            everyday2: "Stay on schedule while driving",
            everyday3: "Manage time during any activity",
            caregiversTitle: "For Students & Caregivers",
            caregivers1: "Track study sessions and breaks",
            caregivers2: "Manage patient care schedules",
            caregivers3: "Gentle time reminders without disruption"
        },
        features: {
            title: "Key Features",
            multilingual: {
                h3: "15+ Languages Support",
                p: "Multiple voice options with natural pronunciation in your preferred language"
            },
            smartModes: {
                h3: "Smart Announcement Modes",
                p: "Clock-aligned and interval-based announcements to fit your workflow"
            },
            efficiency: {
                h3: "Minimal Battery Usage",
                p: "Lightweight design with smooth background operation that won't drain your battery"
            },
            customization: {
                h3: "Completely Customizable",
                p: "Adjust intervals, quiet hours, voice settings, and time formats to match your needs"
            }
        },
        contact: {
            title: "Contact Us",
            description: "Have questions or feedback? We'd love to hear from you!",
            emailUs: "Email Us",
            followUs: "Follow Us"
        },
        privacy: {
            title: "Privacy Policy",
            commitment: "At Voice Clock Time Speaker, we are committed to protecting your privacy and ensuring complete transparency about our data practices.",
            intro: "Voice Clock Time Speaker respects your privacy. The app only requires:",
            audioPermission: "Audio permissions for announcements",
            backgroundPermission: "Background operation permission for continuous functionality",
            dataPolicy: "No personal data is collected or shared with third parties."
        }
    },
    ja: {
        nav: {
            features: "機能",
            download: "ダウンロード",
            contact: "お問い合わせ",
            privacy: "プライバシー",
            faq: "よくある質問"
        },
        hero: {
            subtitle: "ハンズフリー時間管理",
            description: "目も手も使わず、ストレスフリー。大切なことに集中しながら時間をお知らせ。ADHD、アクセシビリティ、マルチタスク、日常生活に最適。",
            downloadNow: "今すぐダウンロード",
            learnMore: "詳細を見る"
        },
        benefits: {
            title: "Voice Clock Time Speakerがあなたの一日をより良くする方法",
            adhdTitle: "ADHD・リモートワーカーの方へ",
            adhd1: "スマホを見ずに集中を維持",
            adhd2: "効果的な時間ブロッキング",
            adhd3: "時間を見失うことがなくなります",
            accessibilityTitle: "アクセシビリティユーザーの方へ",
            accessibility1: "クリスタルクリアな音声アナウンス",
            accessibility2: "ハンズフリーな時間認識",
            accessibility3: "15以上の言語でネイティブ音声対応",
            everydayTitle: "日常生活の方へ",
            everyday1: "シャワー、料理、ワークアウトに最適",
            everyday2: "運転中のスケジュール管理",
            everyday3: "あらゆる活動中の時間管理",
            caregiversTitle: "学生・介護者の方へ",
            caregivers1: "学習セッションと休憩の記録",
            caregivers2: "患者ケアスケジュールの管理",
            caregivers3: "邪魔にならない優しい時間リマインダー"
        },
        features: {
            title: "主な機能",
            multilingual: {
                h3: "15以上の言語サポート",
                p: "お好みの言語で自然な発音の複数音声オプション"
            },
            smartModes: {
                h3: "スマートアナウンスモード",
                p: "時計合わせとインターバルベースのアナウンスでワークフローに適応"
            },
            efficiency: {
                h3: "最小限のバッテリー使用",
                p: "バッテリーを消耗しないスムーズなバックグラウンド動作の軽量設計"
            },
            customization: {
                h3: "完全カスタマイズ可能",
                p: "インターバル、静音時間、音声設定、時間フォーマットをニーズに合わせて調整"
            }
        },
        contact: {
            title: "お問い合わせ",
            description: "ご質問やフィードバックをお待ちしております！",
            emailUs: "メールを送る",
            followUs: "フォローする"
        },
        privacy: {
            title: "プライバシーポリシー",
            commitment: "Voice Clock Time Speakerは、お客様のプライバシーを保護し、データ取り扱いについて完全な透明性を確保することを約束します。",
            intro: "Voice Clock Time Speakerはあなたのプライバシーを尊重します。アプリに必要な権限は以下のみです：",
            audioPermission: "アナウンスのための音声権限",
            backgroundPermission: "継続的な機能のためのバックグラウンド動作権限",
            dataPolicy: "個人データの収集や第三者との共有は行いません。"
        }
    }
};

// Language toggle function
function toggleLanguage() {
    const currentLang = document.documentElement.lang || 'en';
    const newLang = currentLang === 'en' ? 'ja' : 'en';
    
    // Update content with new language
    updateContent(newLang);
    
    // Update toggle button text
    const langToggle = document.getElementById('langToggle');
    if (langToggle) {
        langToggle.textContent = newLang === 'en' ? '日本語' : 'English';
    }
    
    // Save language preference
    localStorage.setItem('preferredLanguage', newLang);
}

// Content update function
function updateContent(lang) {
    if (!translations[lang]) {
        console.error(`Language ${lang} not found in translations`);
        return;
    }

    const content = translations[lang];
    
    // Update document language
    document.documentElement.lang = lang;
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (!key) return;

        try {
            const keys = key.split('.');
            let value = content;
            
            for (const k of keys) {
                value = value[k];
                if (value === undefined) throw new Error(`Translation not found for key: ${key}`);
            }
            
            if (element.tagName === 'INPUT') {
                element.placeholder = value;
            } else {
                element.textContent = value;
            }
        } catch (error) {
            console.error(`Error updating translation for key ${key}:`, error);
        }
    });
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLanguage') || 'en';
    
    // Initialize content with saved language
    updateContent(savedLang);
    
    // Update toggle button text
    const langToggle = document.getElementById('langToggle');
    if (langToggle) {
        langToggle.textContent = savedLang === 'en' ? '日本語' : 'English';
    }
    
    // Add click event listener to language toggle button
    const langToggleBtn = document.getElementById('langToggle');
    if (langToggleBtn) {
        langToggleBtn.addEventListener('click', toggleLanguage);
    }
});