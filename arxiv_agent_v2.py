import google.generativeai as genai
import requests
import feedparser

# --- 配置区 ---
TELEGRAM_TOKEN = "8668004148:AAHi7Fo-x8mhmFwvFkvif0PKYt8ehjEOTjY"
CHAT_ID = "6220919563"
GEMINI_API_KEY = "AIzaSyAK5nQASX8eoC2XWwscaXGvHdj8c2-KPB8"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def evaluate_paper(title, summary):
    """
    逻辑校验：通过 LLM 判定论文是否属于底层技术突破
    """
    prompt = f"""
    你是一名 AI 首席科学家。请评估以下论文摘要的含金量。
    标题: {title}
    摘要: {summary}

    评价标准：
    1. 属于“底层技术突破”吗？（如：修改了 Transformer 架构、提出了新的优化器、证明了新的 Scaling Law）
    2. 仅是“行业新闻/应用”吗？（如：XX 模型在 XX 榜单第一、XX 公司发布了新 API）

    请严格按以下格式返回：
    【判定】：底层突破 / 行业应用
    【核心创新点】：一句话说明其数学或架构上的改动，禁止使用模糊形容词。
    【价值分数】：0-10分（8分以上代表必须立即阅读）
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"大脑下线: {e}"

def run_agent():
    import os

DB_FILE = "processed_papers.txt"

def load_processed_ids():
    if not os.path.exists(DB_FILE): return set()
    with open(DB_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_processed_id(paper_id):
    with open(DB_FILE, "a") as f:
        f.write(f"{paper_id}\n")

def run_agent():
    processed_ids = load_processed_ids()
    # 增加搜索深度，确保不漏掉深夜更新
    url = "http://export.arxiv.org/api/query?search_query=all:LLM&max_results=10&sortBy=submittedDate"
    feed = feedparser.parse(url)
    
    for entry in feed.entries:
        paper_id = entry.id.split('/')[-1] # 提取 arXiv ID
        
        if paper_id in processed_ids:
            continue # 逻辑门控：已读过的直接跳过，瞬间提速
            
        print(f"检测到新论文: {entry.title}")
        evaluation = evaluate_paper(entry.title, entry.summary)
        
        if "底层突破" in evaluation:
            # 推送逻辑...
            pass
            
        save_processed_id(paper_id) # 记录下来，下次不读了

if __name__ == "__main__":
    run_agent()