import requests
from ..config import OLLAMA_API_URL, OLLAMA_MODEL_NAME

def call_ollama_local_model(user_input):
    """
    调用 Ollama 的 local_model 模型，并返回其输出。
    """
    # # 构造符合模板结构的提示词
    # prompt = f"""### Question:
    # {user_input}

    # ### Response:
    # """
    # 请求体
    payload = {
        "model": OLLAMA_MODEL_NAME,  # 模型名称
        "prompt": user_input,            # 构造好的提示词
        "stream": False              # 禁用流式输出
    }
    # 发送请求
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"调用 Ollama 失败: {response.status_code} - {response.text}")