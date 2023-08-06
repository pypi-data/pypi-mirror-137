from mpflow import Node
import time


class DemoNode2(Node):
    def on_execute(self):
        interval = self.params.get("interval", 2)
        time.sleep(interval)
        data = f"-{self.name}-{self.pid}-"
        # 接收数据
        recv_data = self.recv()
        self.log(f"recv < {recv_data}")
        # 发送数据
        self.send(data)
        self.log(f"send > {data}")
