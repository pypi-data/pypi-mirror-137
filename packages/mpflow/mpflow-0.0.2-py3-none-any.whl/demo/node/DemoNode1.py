from mpflow import Node
import time


class DemoNode1(Node):
    def on_execute(self):
        interval = self.params.get("interval", 2)
        time.sleep(interval)
        data = f"-{self.name}-{self.pid}-"

        self.send(data)
        self.log(f"send > {data}")
