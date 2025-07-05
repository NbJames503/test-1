import requests
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 基础API URL
base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'

# 抓取前5页
pages = 5
all_news = []

# 用户设定的关键词列表
keywords = ['AI', '大模型']  # 用户可以修改这里的关键词

print(f'开始抓取新浪新闻前{pages}页...')

try:
    for page in range(1, pages + 1):
        print(f'\n正在抓取第{page}页...')
        
        # 1. 获取当前页新闻列表
        response = requests.get(base_url.format(page), headers=headers)
        response.raise_for_status()
        print(f'第{page}页获取成功，状态码: {response.status_code}')
        
        # 解析JSON数据
        data = json.loads(response.text)
        if data['result']['status']['code'] != 0:
            print(f'第{page}页API返回错误，跳过')
            continue
        
        # 获取当前页新闻
        news_list = data['result']['data']
        if not news_list:
            print(f'第{page}页新闻列表为空，跳过')
            continue
        
        # 过滤新闻，只保留包含关键词的新闻
        filtered_news = [news for news in news_list 
                        if any(keyword in news['title'] for keyword in keywords)]
        
        # 添加到总列表
        all_news.extend(filtered_news)
        print(f'第{page}页找到{len(filtered_news)}条匹配新闻，已添加到总列表')
        
        # 适当延迟，避免请求过于频繁
        time.sleep(1)
    
    print(f'\n共找到{len(all_news)}条匹配新闻:')
    print('='*50)
    for i, news in enumerate(all_news):
        print(f'{i+1}. {news["title"]}')
        print(f'   链接: {news["url"]}')
    print('='*50)
    
    # 保存所有结果到文件
    with open('all_pages_news.txt', 'w', encoding='utf-8') as f:
        f.write(f'新浪新闻前{pages}页匹配关键词的新闻({len(all_news)}条)\n\n')
        for news in all_news:
            f.write(f'{news["title"]}\n{news["url"]}\n\n')
    print(f'所有匹配新闻标题和链接已保存到 all_pages_news.txt')
    
except requests.exceptions.RequestException as e:
    print(f'请求出错: {e}')
except Exception as e:
    print(f'发生错误: {e}')