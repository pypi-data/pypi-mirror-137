import time
from multiprocessing import Pipe
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, AnyStr
from collections import defaultdict
import re


class RecvData:
    """
    接收数据
    从各个节点中recv得到的数据
    """

    _data = defaultdict(str)
    _consumed_by = defaultdict(set)

    def __repr__(self):
        return self._data

    def set(self, key, val):
        self._data[key] = val
        self._clear_consume(key)

    def get(self, key):
        return self._data[key]

    def _clear_consume(self, key):
        """
        清空消费记录
        :param key:
        :return:
        """
        self._consumed_by[key].clear()

    def consume(self, key: str, target: str):
        """
        数据消费
        :param key:
        :param target:
        :return:
        """
        self._consumed_by[key].add(target)

    def batch_consume(self, key_set: set, target: str):
        """
        批量数据消费
        :param key_set:
        :param target:
        :return:
        """
        if len(key_set) == 0:
            return False
        for key in key_set:
            if self.is_consumed(key, target):
                return False
        for key in key_set:
            self.consume(key, target)
        return True

    def is_consumed(self, key, target: str):
        """
        检查结果是否被消费
        :param key:
        :param target:
        :return:
        """
        return target in self._consumed_by[key]


class Bus:
    """
    数据总线
    """
    bus: Dict[AnyStr, Pipe] = {}
    _name_recv_from_dict = {}
    # 获取到的数据
    _recv_data = RecvData()
    # 依赖结构
    dpd_structure = {}

    def __init__(self, conf={}):
        self.bus_conf = conf

    def register(self, name: str, recv_from: str = ""):
        if name in self.bus.keys():
            raise Exception(f"{name} is already registered on bus")

        r, s = Pipe()
        self.bus[name] = s
        self._name_recv_from_dict[name] = recv_from
        return r

    def recv(self, name):
        """
        接收数据
        :param name:
        :return:
        """
        if name not in self.bus:
            raise Exception(f"{name} is not registered on bus")
        p = self.bus.get(name)
        data = p.recv()
        # print(f"recv: {name} => {data}")
        return data

    def send(self, name, data):
        """
        发送数据
        :param name:
        :param data:
        :return:
        """
        # print(f"send: {name} => {data}")
        if name not in self.bus:
            raise Exception(f"{name} is not registered on bus")
        p = self.bus.get(name)
        p.send(data)

    def start_breathing(self):
        """
        收集数据 分发数据
        :return:
        """
        # --- recv : 此阶段会产生阻塞，阻塞时间等于最长耗时节点发出数据的时间
        with ThreadPoolExecutor(max_workers=len(self.dpd_structure.keys()) + 1) as pool:
            for name in self.dpd_structure.keys():
                pool.submit(self._inhale, name)
            # --- send
            pool.submit(self._exhale)

    def _inhale(self, name):
        """
        接收数据（单条）
        :param name:
        :return:
        """
        while True:
            self._recv_data.set(name, self.recv(name))

    def _exhale(self):
        """
        发送数据
        :return:
        """
        while True:
            # 每次发送数据 加少许间隔 防止吃满CPU
            time.sleep(self.bus_conf.get("exhale_interval", 0.01))
            for name in self.dpd_structure.keys():
                data = {}
                for name2 in self.dpd_structure.get(name):
                    data[name2] = self._recv_data.get(name2)
                # data 的数据 发送到了name节点下
                # data.keys() 的数据 都被 name 消费掉了
                if self._recv_data.batch_consume(data.keys(), name):
                    self.send(name, data)

    def build(self):
        """
        构建数据依赖关系
        :return:
        """
        names = self._name_recv_from_dict.keys()
        dpd_data = defaultdict(list)
        for name in names:
            dpd_data[name] = []

            recv_from_str: str = self._name_recv_from_dict[name]
            if recv_from_str:
                for s in recv_from_str.split("|"):
                    for name2 in names:
                        if name == name2:
                            continue
                        match_obj = re.search(s, name2, re.M | re.I)
                        if match_obj:
                            dpd_data[name].append(name2)
        self.dpd_structure = dpd_data
