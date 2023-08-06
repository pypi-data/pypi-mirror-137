import abc
import json
import os
from multiprocessing import Process, Pipe
from abc import abstractmethod
from loguru import logger
import time
import uuid
from datetime import datetime
import psutil
import traceback


class Node(Process, abc.ABC):
    """
    节点模块
    """
    # 节点名称
    name: str
    # 节点参数
    params: dict
    # 当前节点配置
    config: dict = {}
    # 当前节点输出数据
    data: {}
    # 当前节点处理速度
    _fps: float = 0

    _recv_from: str
    _pipe: Pipe

    def __init__(self, name, params: dict, config: dict, recv_from: str, node_prod_dir: str, pipe: Pipe):
        super().__init__()
        self.name = name
        self.params = params
        self.config = config
        # 产物存放目录
        self.prod_dir = node_prod_dir
        self._recv_from = recv_from
        self._pipe = pipe
        # 用于统计计算
        self._window = [0, 0, 0, 0, 0]
        self._p = psutil.Process(self.pid)

        os.makedirs(self.prod_dir, exist_ok=True)

    def send(self, data):
        wd = self._wrap_data(data)
        self._pipe.send(wd)
        if self.config.get("save_result", False):
            self.on_save_result(wd)

    def recv(self):
        return self._pipe.recv()

    def run(self):
        self.on_init()
        while True:
            try:
                _t = time.monotonic()
                self.on_execute()
                # 当前执行耗时
                _cost = time.monotonic() - _t

                self._window.pop(0)
                self._window.append(_cost)
                self._fps = len(self._window) / sum(self._window)

            except Exception as e:
                self.log(e, "ERROR")
                self.log(traceback.format_exc(), "ERROR")
                self.on_execute_exception(e)

    @abstractmethod
    def on_execute(self):
        pass

    def log(self, message, level="info"):
        """
        log函数封装
        :param message:
        :param level:
        :return:
        """
        if self.config.get("print_log", True):
            if level.lower() == "info":
                logger.info(f"{self.name}: " + str(message))
            elif level.lower() == "error":
                logger.error(f"{self.name}: " + str(message))
            else:
                logger.info(f"{self.name}: " + str(message))

    def _wrap_data(self, data):
        """
        对发送数据进行二次包装
        :param data:
        :return:
        """
        _create_at = time.time()
        return {
            "meta": {
                "name": self.name,
                "uuid": str(uuid.uuid4()),
                "create_at": _create_at,
                "create_at_fmt": datetime.fromtimestamp(_create_at).strftime('%Y/%m/%d %H:%M:%S.%f'),
            },
            "status": {
                "fps": self._fps,
                "pid": self.pid,
                "memory_percent": f"{self._p.memory_percent():.2f}%",
                "cpu_percent": f"{self._p.cpu_percent():.2f}%"
            },
            "data": data
        }

    def on_save_result(self, data):
        """
        结果保存逻辑
        各个节点可以根据自己的保存逻辑来重写此方法
        :param data:
        :return:
        """
        fn = f"{time.time()}.json"
        fp = os.path.join(self.prod_dir, fn)
        with open(fp, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def on_init(self):
        """
        初始化回调
        :return:
        """
        pass

    def on_execute_exception(self, e):
        """
        执行时 异常回调
        :param e:
        :return:
        """
        pass
