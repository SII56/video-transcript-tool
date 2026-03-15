import os
import requests

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

def deepseek_punctuate(text: str) -> str:
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    请给下面的中文语音识别文本进行补充标点并合理分句。
    
    要求：
    1. 不要改变原意
    2. 不要删除信息
    3. 不要总结
    4. 输出简体中文
    5. 需要修正那些明显识别错误的词语，无法修正则保留原文
    
    文本：
    {text}
    """

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个中文文本整理助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    return result["choices"][0]["message"]["content"]