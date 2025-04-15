import sys
import os
import threading
import time
import queue
import logging
from typing import List, Any

# 获取 CPS 模块所在的目录路径
cps_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SDK_connect'))
sys.path.append(cps_path)

# 导入 CPSClient 模块
from CPS import CPSClient

# 创建一个队列用于线程间通信
status_queue = queue.Queue()

# 初始化 CPSClient
cps = CPSClient()


# 状态确认函数
def check_status(result: List[Any]) -> bool:
    """
    打印所有状态，并根据条件判断机器是否达到状态。
    :param result: 机器人状态列表
    :return: 如果机器达到状态，返回 True；否则返回 False

    result[0] 运动中状态 string 0/1
        0：机器人不处于运动状态
        1：机器人运动中
    result[1] 已使能状态 string 0/1
        0：机器人未使能
        1：机器人已使能
    result[2] 错误状态 string 0/1
        0：未发生错误
        1：有错误发生
    result[12] 到位状态 string 0/1
        0：机器人实际位置还没有运动到命令位置
        1：运动到位(命令与实际位置基本没有误差)
    """
    # 检查状态是否符合条件
    if len(result) >= 3 and result[0] == '0' and result[1] == '1' and result[2] == '0':
        return True  # 符合条件
    return False  # 不符合条件

# 监听线程的任务函数
def listen_task():
    print("Listening thread started")
    while True:
        try:
            # 清空 result 列表
            result: List[Any] = []

            # 读取机器人状态
            nRet = cps.HRIF_ReadRobotState(0, 0, result)

            # 将状态信息放入队列
            status_queue.put(result)

            # 每隔一段时间读取一次状态
            time.sleep(1)  # 1 秒读取一次
        except Exception as e:
            logging.error(f"Error in listen_task: {e}")
            break

# 启动监听线程
def start_listener():
    listener_thread = threading.Thread(target=listen_task)
    listener_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    listener_thread.start()
    return status_queue  # 返回队列，供主线程使用