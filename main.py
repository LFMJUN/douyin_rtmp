import pyshark
import threading
import asyncio
import json

# 从文件中读取 JSON 数据
with open('config.json', 'r', encoding='utf-8') as file:
    json_data = file.read()

# 解析 JSON 数据
data = json.loads(json_data)

# 获取 tshark_path、display_filter 和 interface 字段的值
tshark_path = data["tshark_path"]
display_filter = data["display_filter"]
interface = data["interface"]

# # 替换 'interface' 为你要抓包的网络接口，如 'eth0'、'wlan0' 等
# interface = '以太网'
# # 替换 'display_filter' 为你的显示过滤器
# display_filter = '((rtmpt) && (_ws.col.info contains "connect")) || (_ws.col.info contains "releaseStream")'
# # 替换 'tshark_path' 为你的 tshark.exe 路径
# tshark_path = "F:\\Program Files\\Wireshark\\tshark.exe"


class PacketSniffer(threading.Thread):
    def __init__(self, interface, display_filter):
        super().__init__()
        self.interface = interface
        self.display_filter = display_filter

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())  # 创建并设置新的事件循环
        capture = pyshark.LiveCapture(interface=self.interface, display_filter=self.display_filter,
                                      tshark_path=tshark_path)
        for packet in capture.sniff_continuously():
            packet = str(packet)
            server = filter_strings(packet, "rtmp://")
            code = filter_strings(packet, "stream-")
            if server:
                print("服务器 ", server)
            else:
                print("推流码 ", code[1:-1]) # 去除引号


def filter_strings(input_str, target_str):
    words = input_str.split()  # 将字符串按空格分割成单词列表
    for word in words:
        if target_str in word:
            return word


sniffer = PacketSniffer(interface, display_filter)
sniffer.start()
sniffer.join()
