from .SDK_connect.connect import connect
from .SDK_connect.thread import start_listener
from .services.ollama_service import call_ollama_local_model
from .utils.eflin_extractor import extract_eflin_command
from .utils.eflin_processor import process_eflin_command
from .utils.eflin_matcher import eflin_matcher
import time

catch_list = {"抓取白色寿司": "Func_1", "抓取黄色寿司": "Func_2", "抓取绿色寿司": "Func_3", "抓取蓝色寿司": "Func_4"} #抓取函数集

def ollama_to_function(user_prompt):
    start_time=time.time()
    # 调用 Ollama 的 local_model
    try:
        # ollama_output = call_ollama_local_model(user_prompt)
        ollama_output = user_prompt
        #for test
        # ollama_output="好的，正在为您执行EFlin指令：'抓取' '白色' '寿司' '放置' '左边' '1cm'。执行次数：'2'。"

        # print("Ollama 输出:", ollama_output)
    
        # 在 Ollama 的输出中提取 EFlin 指令
        words, num = extract_eflin_command(ollama_output)
        if words:
            # 处理命令词语
            result = process_eflin_command(words)
            # 添加执行次数到结果中
            result['num'] = num
            # 打印结果
            print("提取的变量:", result)

            # 调用 eflin_matcher 模块
            catch_cmd, put_cmd, num = eflin_matcher(result, catch_list)
            print("匹配结果 - catch_cmd:", catch_cmd)
            print("匹配结果 - put_cmd:", put_cmd)  #put_cmd[0]代表放置指令是否存在，put_cmd[1]代表方向，put_cmd[2]代表距离，如果为0则为容器
            print("匹配结果 - num:", num)

            end_time=time.time()
            print(f"\n运行时长为: {end_time-start_time}s")

            # command_show=f"您要执行的抓取指令为{str(result['action1'])+str(result['colour'])+str(result['object1'])}：{catch_cmd}\n放置指令为{str(result['action2'])+str(result['direction'])+str(result['distance'])+str(result['object2'])}：{put_cmd}\n执行次数：{res[2]}"

            return [catch_cmd, put_cmd, num]

            # return [catch_cmd, put_cmd, num, command_show]


        else:
            print("\n未找到匹配的EFlin指令。")

            end_time=time.time()
            print(f"\n运行时长为: {end_time-start_time}s")

            return None

    except Exception as e:
        print("发生错误:", str(e))
 

# 主线程中的函数，用于读取监听线程的状态信息
def status_to_action(status_queue,action_func:callable):
    # print("11111111111111111")
    while True:
        try:
            result = status_queue.get()# 从队列中获取状态信息
            print(f"状态码为{result}")
        except Exception as e:
            print(f"获取状态信息时发生错误: {e}")
            # continue
            inp_status=input("输入y再次尝试获取状态信息")
            if inp_status=='y':
                continue
            else:
                return -1

        if len(result)>=2 and result[1]=='1':#检查机器人是否使能
        # 检查状态是否符合条件
            if len(result)>=3 and result[2]=='0':#检查机器人是否存在错误
                m_timelimit=5 #设置判断运动状态的时间段
                m_starttime=time.time() #时间开始
                m_status=0

                #注意这里是假设如果机器人五秒内都没有返回任何运动状态，则完全停止运动
                #如果机器人在某些任务中需要停止五秒，那么会出bug

                while True:
                    try:
                        result=status_queue.get()
                    except Exception as e:
                        print("状态码获取失败")
                        inp_status=input("输入y再次尝试获取状态信息")
                        if inp_status=='y':
                            continue
                        else:
                            return -1

                    if time.time()-m_starttime>m_timelimit:
                        break
                    
                    if len(result)>=1 and result[0]=='1':
                        m_status=1
                        break
                    
                # if len(result)>=1 and result[0]=='0': #确认机器人处于未运动状态
                if m_status==0:
                    print("状态符合条件，准备执行动作函数...")
                    try:
                        func_res=action_func()  #执行动作函数，并接受返回值，注意此处假设返回值为列表，且执行失败，列表中必有-1
                    # action_function()  # 执行动作函数
                    # time.sleep(2)
                    except Exception as e:
                        print("动作函数返回异常")
                        return -1
                    if -1 in func_res:
                        print(f"因为函数执行失败，后续状态检查取消")
                        print("当前状态码为：",result)
                        return -1
                    else:
                        print(f"程序显示函数调用成功，函数返回值为{func_res}")
                        break 
                else:
                    time.sleep(1)
            else:
                if len(result)>=4:
                    print(f"机器人发生错误，错误码为{result[3]}")
                    print("状态码为：",result)
                    return -1
                else:
                    print("未接收到错误码，请核查程序状态")
                    print("状态码为：",result)
                    return -1
        else:
            print("状态码为：",result)
            print("状态检查显示机器人未连接或未使能，请先连接或使能")
            return -1     
        
    return 0


def ToRobot(response):
    cnn = connect()
    
    # Initialize status_queue outside the if block
    status_queue = None
    
    if cnn.cps.HRIF_IsConnected(0):
        print("机器人已连接")
    else:
        cnn.CPS_connect()
        status_queue = start_listener()  # This now modifies the outer variable
    
    # Ensure status_queue exists before using it
    if status_queue is None:
        status_queue = start_listener()  # Create if not already created
    
    #调用大模型，并处理模型输出，提取信号
    # 用户输入的提示
    res=ollama_to_function(response)    #最后给SDK的返回值

    #for test
    # res=["Func_move_blue_to_left",[0,1,1,1],4]
    if res:
            for i in range(0,res[2]):
                if i==0:
                    print("注意您的操作会引起机器臂变化，请注意安全")
                    
                    # inp=input("取消执行，请输入\"n\":\n")
                    # if inp.lower()=='n':
                    #     print("指令已取消")
                    #     break
                
                if res[0]:
                    r1 = status_to_action(status_queue,lambda: cnn.common_func([10,20,30],res[0]))
                    if r1==-1:
                        print("因为函数执行发生异常，后续动作函数将不再进行")
                        break

                if res[1][0]!=0:
                    if res[1][3]==0:
                        res[1][3]==50
                    r2 = status_to_action(status_queue,lambda: cnn.move_place_func(res[1][1],res[1][2],res[1][3],1)) #执行平移动作函数
                    if r2==-1:
                        print("因为函数执行发生异常，后续动作函数将不再进行")
                        break
                    r3 = status_to_action(status_queue,lambda: cnn.common_func([10,20,30],"Func_2"
                    )) #执行放置函数
                    if r3==-1:
                        print("因为函数执行发生异常，后续动作函数将不再进行")
                        break

    else:
        print("注意此次操作不引起机器臂任何变化\n")


# if __name__ == "__main__":
#     #连接系统
#     cnn=connect()
#     cnn.CPS_connect()

#     # 启动监听线程并获取队列

#     status_queue = start_listener()
    
#     #调用大模型，并处理模型输出，提取信号
#     while True:
#         user_prompt = input("请输入您的指令: ")
#         if user_prompt == "exit":
#             print("您已安全退出对话")
#             break
#         # 用户输入的提示
        
#         res=ollama_to_function(user_prompt)    #最后给SDK的返回值

#         #for test
#         # res=["Func_move_blue_to_left",[0,1,1,1],4]
#         if res:
#                 for i in range(0,res[2]):
#                     if i==0:
#                         print("注意您的操作会引起机器臂变化，请注意安全")
#                         # print(res[3])
#                         inp=input("取消执行，请输入\"n\":\n")
#                         if inp.lower()=='n':
#                             print("指令已取消")
#                             break
                    
#                     if res[0]:
#                         r1 = status_to_action(status_queue,lambda: cnn.common_func([10,20,30],res[0]))
#                         if r1==-1:
#                             print("因为函数执行发生异常，后续动作函数将不再进行")
#                             break

#                     if res[1][0]!=0:
#                         if res[1][3]==0:
#                             res[1][3]==50
#                         r2 = status_to_action(status_queue,lambda: cnn.move_place_func(res[1][1],res[1][2],res[1][3],1)) #执行平移动作函数
#                         # r2 = status_to_action(status_queue,lambda: cnn.move_place_func(1,1,10,1))
#                         if r2==-1:
#                             print("因为函数执行发生异常，后续动作函数将不再进行")
#                             break
#                         r3 = status_to_action(status_queue,lambda: cnn.common_func([10,20,30],"Func_2"
#                         )) #执行放置函数
#                         if r3==-1:
#                             print("因为函数执行发生异常，后续动作函数将不再进行")
#                             break

#         else:
#             print("注意此次操作不引起机器臂任何变化\n")
#             continue



        



