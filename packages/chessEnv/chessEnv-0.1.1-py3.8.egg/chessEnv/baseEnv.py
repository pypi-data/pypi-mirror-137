#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@Time    :2022/1/12 15:20
# !@Author  : murInj
# !@Filer    : .py
import traceback


class baseEnv:
    def __init__(self):
        self.__board = None  # 设置空棋盘的形状格式
        self.__turn = None  # 设置回合方
        self.buffer = None  # 设置行棋历史
        self.done = False
        self.winner = None
        self.AI1 = None
        self.AI2 = None
        self.__terminalInfo = None
        self.bufferUnit = None

    def getActionSpace(self):
        """
        获取行动空间
        :return: 行动空间
        """
        raise Exception("未重写getActionSpace")

    def getObserveSpace(self):
        """
        获取观测空间
        :return: 观测空间
        """
        raise Exception("未重写getObserveSpace")

    def getAction(self, team1_action, team2_action):
        """
        采取行动
        :return:返回行动值
        """
        return None

    def step(self, action=None):
        """
        行动一步
        :param action: 行动
        :return: 行动后的状态
        """
        raise Exception("未重写step")


    def gender(self, genderMethod=None):
        """
        用于显示棋局,可自定义用UI或者命令行
        :param genderMethod: 显示方法,默认None则为不显示
        :return:
        """
        pass

    def reset(self):
        """
        重置棋局
        :return: None
        """
        raise Exception("未重写reset")

    def beforeUpdate(self):
        """
        采取行动前的棋盘更新
        :return:
        """
        pass

    def afterUpdate(self):
        pass

    def gameoverUpdate(self):
        """
        一轮棋局结束后的处理函数
        :return:
        """
        pass

    def addBuffer(self):
        """
        添加行棋记录
        :return:
        """
        pass

    def oneRound(self):
        """
        完整的进行一轮棋局
        :return: 返回终局信息
        """
        try:
            self.reset()
            while not self.done:
                self.beforeUpdate()
                action = self.getAction(self.AI1, self.AI2)
                self.step(action)
                self.gender()
                self.addBuffer()
                self.afterUpdate()
            self.gameoverUpdate()
            # return self.__terminalInfo
        except Exception as result:
            print(result)
            traceback.print_exc()
