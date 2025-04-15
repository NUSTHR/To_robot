def eflin_matcher(result, catch_list):
    """
    匹配 EFlin 指令并处理结果。

    参数:
        result (dict): 包含 EFlin 指令处理结果的字典。
        catch_list (dict): 抓取指令的映射字典。

    返回:
        list: 包含 catch_cmd, put_cmd, num 的列表。
    """
    catch_cmd = None
    put_cmd = [0, 0, 0, 0]

    # 检查是否有匹配的 EFlin 指令
    if not result:
        print("未找到匹配的EFlin指令。")
        return [catch_cmd, put_cmd, result.get('num', 0)]

    # 处理 action1, colour, object1
    action1 = result.get('action1')
    colour = result.get('colour')
    object1 = result.get('object1')

    # 将不为 None 的元素按顺序连接起来
    catch_key = ''.join(filter(None, [action1, colour, object1]))

    # 与 catch_list 中的键匹配
    if catch_key in catch_list:
        catch_cmd = catch_list[catch_key]

    # 处理 action2, direction, distance
    action2 = result.get('action2')
    direction = result.get('direction')
    distance = result.get('distance')

    if action2 is not None:
        put_cmd[0] = 1

    if direction is not None:
        if '前' in direction:
            put_cmd[1] = 1 #空间方向x,y参数
            put_cmd[2] = 1 #方向正负参数
        elif '后' in direction:
            put_cmd[1] = 1
            put_cmd[2] = 0
        elif '左' in direction:
            put_cmd[1] = 0
            put_cmd[2] = 1
        elif '右' in direction:
            put_cmd[1] = 0
            put_cmd[2] = 0

    if distance is not None:
        # 提取 distance 字符串中的数字
        try:
            put_cmd[3] = int(''.join(filter(str.isdigit, distance)))
        except ValueError:
            pass

    return [catch_cmd, put_cmd, result.get('num', 0)]