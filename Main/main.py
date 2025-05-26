from Main.youtube_scraper import fetch_youtube_trending
from Main.excel_writer import save_videos_to_excel

# กำหนด keywords สำหรับแยกหมวดหมู่
keywords_trend = ['กระแส', 'viral', 'trend', 'เทรนด์', 'ยอดนิยม', 'ไวรัล']
keywords_music = ['เพลง', 'mv', 'มิวสิก', 'ร้องเพลง', 'music', 'เพลงใหม่']
keywords_game = ['เกม', 'rov', 'game', 'เกมส์', 'gta', 'roblox', 'minecraft']
keywords_movie = ['หนัง', 'ภาพยนตร์', 'movie', 'ซีรี่ส์', 'series', 'ละคร']

def categorize(title, channel):
    text = (title + " " + channel).lower()
    if any(k in text for k in keywords_trend):
        return 'กระแส'
    elif any(k in text for k in keywords_music):
        return 'เพลง'
    elif any(k in text for k in keywords_game):
        return 'เกม'
    elif any(k in text for k in keywords_movie):
        return 'ภาพยนตร์'
    else:
        return 'อื่น ๆ'

def views_to_number(views_str):
    views_str = views_str.replace('การดู', '').replace('ครั้ง', '').strip()
    number = 0
    try:
        if 'ล้าน' in views_str:
            number = float(views_str.replace('ล้าน', '').strip()) * 1_000_000
        elif 'แสน' in views_str:
            number = float(views_str.replace('แสน', '').strip()) * 100_000
        else:
            number = float(views_str.replace(',', '').strip())
    except:
        number = 0
    return number

def main():
    print("กำลังดึงข้อมูล...")
    videos = fetch_youtube_trending(limit=50)
    
    print(f"ดึงข้อมูลมาได้ {len(videos)} รายการ")
    
    for v in videos:
        v['category'] = categorize(v['title'] or '', v['channel'] or '')
        v['views_num'] = views_to_number(v['views'] or '0')
    
    # เรียงตามวิว
    videos_sorted = sorted(videos, key=lambda x: x['views_num'], reverse=True)
    
    print("กำลังบันทึกลงไฟล์ Excel...")
    save_videos_to_excel(videos_sorted, filename='youtube_trending_categorized.xlsx')
    
    print("เสร็จสิ้น! ไฟล์บันทึกที่ youtube_trending_categorized.xlsx")

if __name__ == "__main__":
    main()
