import re

def extract_eflin_command(text):
    """
    提取EFlin指令中的词语和执行次数。
    """
    # 定义匹配模式，支持中文冒号和英文冒号
    pattern = r"好的，正在为您执行EFlin指令[：:](.*?)执行次数：'(.*?)'"
    match = re.search(pattern, text)
    if match:
        command_part = match.group(1)
        num = int(match.group(2))  # 将执行次数转换为整数
        # 使用正则表达式按空格分割词语，并去除可能的引号
        words = re.findall(r"'(.*?)'", command_part)
        return words, num
    else:
        return None, None