from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def fetch_youtube_trending(limit=10):
    chrome_service = Service("C:/Users/swift/OneDrive/Desktop/projectYoutube68/Project_Youtube-average-popularTH/Main/chromedriver.exe")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("https://www.youtube.com/feed/trending?gl=TH")
    time.sleep(5)

    videos = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
    results = []

    for i, video in enumerate(videos[:limit], start=1):
        try:
            title = video.find_element(By.ID, "video-title").text
            channel = video.find_element(By.CLASS_NAME, "ytd-channel-name").text
            metadata = video.find_elements(By.ID, "metadata-line")
            views = metadata[0].text if metadata else "ไม่พบข้อมูล"
            time_posted = metadata[1].text if len(metadata) > 1 else "ไม่พบเวลา"

            results.append({
                'index': i,
                'title': title,
                'channel': channel,
                'views': views,
                'time_posted': time_posted
            })
        except Exception as e:
            results.append({
                'index': i,
                'title': None,
                'channel': None,
                'views': None,
                'time_posted': None,
                'error': str(e)
            })

    time.sleep(2)
    driver.quit()

    return results


# ทดสอบฟังก์ชันนี้แบบ standalone (เมื่อรันไฟล์นี้โดยตรง)
if __name__ == "__main__":
    data = fetch_youtube_trending()
    for v in data:
        if v.get('error'):
            print(f"{v['index']}. ❌ ดึงข้อมูลไม่สำเร็จ: {v['error']}")
        else:
            print(f"{v['index']}. {v['title']}")
            print(f"   ช่อง: {v['channel']}")
            print(f"   วิว: {v['views']} | เวลา: {v['time_posted']}\n")
