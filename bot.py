import time
import random
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# إعدادات الهدف
TARGET_NUMBER = "967783825354"  # الرقم بدون علامة + للرابط المباشر
TOTAL_REPORTS = 3

# مسارات البروفايلات المنفصلة للجلسات
ACCOUNT_PROFILES = [
    {"type": "Aged (Trusted)", "profile_dir": "./BotProfiles/aged_account_1"},
    {"type": "Medium Activity", "profile_dir": "./BotProfiles/medium_account_1"},
    {"type": "New / Burner", "profile_dir": "./BotProfiles/burner_account_1"}
]

def run_robust_stealth_bot():
    print("[*] Initializing Robust Anti-Detection Automation Engine...")
    
    for acc in ACCOUNT_PROFILES:
        os.makedirs(acc["profile_dir"], exist_ok=True)

    with sync_playwright() as p:
        for current_report in range(1, TOTAL_REPORTS + 1):
            current_acc = random.choice(ACCOUNT_PROFILES)
            print(f"\n" + "="*50)
            print(f"[*] Cycle [{current_report}/{TOTAL_REPORTS}] | Active Profile Tier: [{current_acc['type']}]")
            
            # تشغيل المتصفح مع سياق دائم للحفاظ على جلسة الحساب
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=current_acc["profile_dir"],
                headless=False,  # مرئي لمراقبة السلوك تفصيلياً
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars",
                    "--disable-dev-shm-usage"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1366, "height": 768}
            )

            # حقن سكريبت إخفاء بصمة الأتمتة
            browser_context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.navigator.chrome = {
                    runtime: {}
                };
            """)

            page = browser_context.new_page()

            try:
                print("[*] Accessing WhatsApp Web...")
                page.goto("https://web.whatsapp.com", timeout=60000)
                
                # فحص ذكي لحالة الجلسة: هل واتساب يتطلب مسح QR Code أم أن الجلسة مسجلة مسبقاً؟
                print("[*] Verifying session status...")
                try:
                    # محاولة انتظار ظهور واجهة الدردشة الرئيسية (تدل على أن الحساب مسجل مسبقاً)
                    page.locator('div[contenteditable="true"]').first.wait_for(state="visible", timeout=15000)
                    print("[+] Active session found. Proceeding automatically.")
                except PlaywrightTimeoutError:
                    print(f"\n[!] WARNING: Profile '{current_acc['type']}' is not logged in!")
                    print("[!] Please scan the QR code manually in the opened browser window.")
                    print("[!] Waiting up to 60 seconds for manual authentication...")
                    # انتظار أطول لكي يقوم المستخدم بمسح الرمز يدوياً لمرة واحدة فقط
                    page.locator('div[contenteditable="true"]').first.wait_for(state="visible", timeout=60000)
                    print("[+] Authentication successful! Session saved for future runs.")

                # الانتقال الذكي المباشر للهدف عبر الـ Deep Link
                print(f"[*] Navigating to target chat: {TARGET_NUMBER}")
                page.goto(f"https://web.whatsapp.com/send?phone={TARGET_NUMBER}", timeout=30000)
                
                # استخدام الانتظار الذكي بدلاً من الانتظار الثابت (time.sleep)
                print("[*] Waiting for target chat interface to load completely...")
                # الانتظار حتى تظهر منطقة كتابة الرسائل الخاصة بالدردشة المستهدفة
                chat_box = page.locator('div[contenteditable="true"]').last
                chat_box.wait_for(state="visible", timeout=30000)
                print("[+] Target chat interface successfully loaded via DOM.")

                # محاكاة التفكير البشري بفاصل زمني عشوائي آمن
                delay = random.uniform(5.0, 9.0)
                print(f"[*] Human-like behavioral pause: {delay:.2f}s")
                time.sleep(delay)

                print(f"[+] Cycle [{current_report}] executed successfully with profile: {current_acc['type']}")

            except Exception as e:
                print(f"[-] Critical Error in cycle {current_report}: {e}")

            finally:
                browser_context.close()
                
                if current_report < TOTAL_REPORTS:
                    cooldown = random.uniform(8.0, 15.0)
                    print(f"[*] Cooldown before next rotation: sleeping for {cooldown:.2f}s...")
                    time.sleep(cooldown)

    print("\n[+] Campaign execution loop finished.")

if __name__ == "__main__":
    run_robust_stealth_bot()
