import os
from typing import List
from .node import Node
from .bus import Bus
import importlib
from loguru import logger


class Context:

    def __init__(self, config):
        self.nodes: List[Node] = []
        self.conf = config
        self.bus = Bus(self.conf.get("bus", {}))
        self.build()

    def build(self):
        # 产物存放目录
        prod_save_dir = self.conf['prod_save_dir']
        os.makedirs(prod_save_dir, exist_ok=True)

        nodes_conf = self.conf['nodes']
        for node in nodes_conf:
            logger.info(f"node => {node}")
            pkg = ".".join(str(node['cls']).split('.')[:-1])
            cls_name = node['cls'].split('.')[-1]
            md = importlib.import_module(pkg)
            node_cls = md.__dict__[cls_name]
            name = node['name']
            recv_from = node.get('recv_from', '')
            pipe = self.bus.register(name, recv_from)
            node_obj = node_cls(
                name=name,
                params=node.get('params', {}),
                config=node.get('config', {}),
                recv_from=recv_from,
                node_prod_dir=os.path.join(prod_save_dir, name),
                pipe=pipe)
            self.nodes.append(node_obj)

        self.bus.build()

    def start(self):
        logger.info('context start')
        for node in self.nodes:
            node.start()

        logger.info("start breathing")
        self.bus.start_breathing()
