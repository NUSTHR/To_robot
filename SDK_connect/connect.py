import sys
import os
# from thread import start_listener

# 获取 CPS 模块所在的目录路径
cps_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SDK_connect'))
sys.path.append(cps_path)

from CPS import CPSClient


from CPS import CPSClient  # 导入CPSClient模块
import logging
from typing import List, Any

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class connect:
    def __init__(self):
        # 设置主机地址和端口
        self.host = '10.20.40.45'
        # self.host = '192.168.0.10'
        self.port = 10003
        # 初始化一个空的结果列表
        self.result = []
        # 创建CPSClient实例 
        self.cps = CPSClient()

    def CPS_connect(self):
        # 使用HRIF_Connect方法连接到指定的主机和端口
        ret = self.cps.HRIF_Connect(0, self.host, self.port)

        # 使用HRIF_ReadCurFSM方法读取当前状态机并将结果存储在结果列表中
        self.cps.HRIF_ReadCurFSM(0, 1, self.result)

        #  打印连接返回值和结果列表
        print(ret)
        print(self.result)

    def common_func(self,params: List[Any],func_name) -> List[Any]:
        """
        运行指定函数并返回结果。

        :param func_name: 函数名
        :param params: 输入参数（列表）
        :param cps: CPSClient 实例，用于调用 HRIF_RunFunc 函数
        :return: 函数返回值（列表）

        """
        result = []
        # func_name=guijiliudong.main()
        # print("func_name is ",func_name)
        # 参数检查
        # if func_name==-1:
        #     print("欢迎您下次再来")
        #     result.append(-1)
        #     return  result
        if not func_name:
            # raise ValueError("注意：因为您输入的指令无效，传回给机器的函数是空，所以此次并未执行任何指令")
             print("注意：func_name为空，请您检查输入")
             return [-1]
        if not isinstance(params, list):
            raise TypeError("输入参数必须是一个列表")
        if not isinstance(self.cps, CPSClient):
            raise TypeError("cps 必须是 CPSClient 类型")
        if not isinstance(func_name, str):
            raise TypeError("func_name 必须是字符串类型")
        
        try:
            # 调用函数
            nRet = self.cps.HRIF_RunFunc(0,  func_name, params, result)
            if nRet == 0:
                logging.info(f"函数 {func_name} 执行成功，返回值: {result}")
            else:
                logging.error(f"函数 {func_name} 执行失败，错误码: {nRet}")
                return [-1]
        except Exception as e:
            logging.error(f"发生异常: {e}")
        print(result)
        return result
    
    def move_place_func(self,nAxis=1, nDirection=1, nDistance=1, nToolMotion=1):
        """
        执行相对空间平移运动。

        :param cps: CPSClient 实例
        :param nAxis: 轴 ID（默认值为 1）
        :param nDirection: 运动方向（默认值为 1）
        :param nDistance: 运动距离（默认值为 1）
        :param nToolMotion: 运动坐标类型（默认值为 1）
        :return: HRIF_MoveRelL 的返回值
        """
        result=[]
            # 参数验证
        if not isinstance(self.cps, CPSClient):
            print("错误：参数 cps 必须是 CPSClient 类型")
            return [-1]
        if not isinstance(nAxis, int) or nAxis < 0 or nAxis >=6:
            print("错误：参数 nAxis 必须是小于等于5正整数或0")
            return [-1]
        if nDirection not in [1, 0]:
            print("错误：参数 nDirection 必须是 1 或 0")
            return [-1]
        if not isinstance(nDistance, (int, float)):
            print("错误：参数 nDistance 必须是整数或浮点数")
            return [-1]
        if nToolMotion not in [0, 1]:
            print("错误：参数 nToolMotion 必须是 0 或 1")
            return [-1]
        
        try:
            # 调用 HRIF_MoveRelL 接口
            nRet1 = self.cps.HRIF_MoveRelL(0, 0, nAxis, nDirection, nDistance, nToolMotion)
            if nRet1 == 0:
                print("相对空间运动执行成功")
            else:
                print(f"相对空间运动执行失败，错误码: {nRet1}，后续操作取消")
                return [-1]
            # return nRet
        except Exception as e:
            print(f"发生异常: {e}")
            return [-1]  # 表示异常状态
        
        # try:
        #     res_c=self.common_func([10,20,30],"Func_1")
        #     if -1 in res_c:
        #         print("Func_place 执行失败")
        #         return [-1]
        #     else:
        #         print("Func_place 执行成功")            
        # except Exception as e:
        #     print(f"发生异常: {e}")
        #     return [-1]

        return result
        

if __name__=="__main__":
    cnn=connect()
    cnn.CPS_connect()
    # sq=start_listener()
    # i=0
    # func_test="Func_move_blue_to_left"
    # while True:
    #     i=i+1
    #     print(sq.get())
    #     # time.sleep(1)
    #     if i==1:
    #         # res=cnn.move_place_func(2,0,40,1)
    #         res=cnn.common_func([10,20,30],"Func_夹爪开")
    #         if -1 in res:
    #             print(f"执行失败，错误码为{res[0]}")




