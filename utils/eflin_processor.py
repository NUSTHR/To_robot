def process_eflin_command(words):
    """
    处理提取的词语，按照新的规则赋值给各个变量。
    """
    # 初始化变量
    action1 = None
    action2 = None
    colour = None
    object1 = None
    direction = None
    object2 = None
    distance = None

    # 查找action1和action2
    for word in words:
        if word == '抓取' and action1 is None:
            action1 = word
        elif word == '放置' and action2 is None:
            action2 = word

    # 查找colour及其object1
    if action1 is not None:
        for i, word in enumerate(words):
            if '色' in word and words.index(action1) + 1 == i:
                colour = word
                # object1为colour后的第一个词
                if i + 1 < len(words):
                    object1 = words[i + 1]
                break

    # 如果action1存在且colour不存在，将action1后的第一个词存储在object1中
    if action1 is not None and colour is None:
        action1_index = words.index(action1)
        if action1_index + 1 < len(words):
            object1 = words[action1_index + 1]

    # 查找direction及其object2或distance
    if action2 is not None:
        for i, word in enumerate(words):
            # 检查是否包含方向词（“前”、“后”、“左”、“右”）
            if any(d in word for d in ['前', '后', '左', '右']) and words.index(action2) + 1 == i:
                direction = word
                # 检查下一个词是否包含距离单位（cm、厘米、mm、毫米）
                if i + 1 < len(words):
                    next_word = words[i + 1]
                    if any(unit in next_word for unit in ['cm', '厘米', 'mm', '毫米']):
                        distance = next_word
                    else:
                        # 如果下一个词不包含距离单位，则将其赋值给object2
                        object2 = next_word if next_word else None  # 确保空字符串被赋值为None
                break

    return {
        'action1': action1,
        'colour': colour,
        'object1': object1,
        'action2': action2,
        'direction': direction,
        'distance': distance,
        'object2': object2
    }