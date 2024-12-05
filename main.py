import pyshark
import json
import subprocess
import os

# 从文件中读取 JSON 数据
with open("config.json", "r", encoding="utf-8") as file:
    json_data = file.read()

# 解析 JSON 数据
data = json.loads(json_data)

# 获取 tshark_path、display_filter 和 interface 字段的值
tshark_path = data["tshark_path"]
display_filter = data["display_filter"]
interface = data["interface"]
obs_path = data["obs_path"]
obs_config_path = data["obs_config_path"]

# # 替换 'interface' 为你要抓包的网络接口，如 'eth0'、'wlan0' 等
# interface = '以太网'
# # 替换 'display_filter' 为你的显示过滤器
# display_filter = '((rtmpt) && (_ws.col.info contains "connect")) || (_ws.col.info contains "releaseStream")'
# # 替换 'tshark_path' 为你的 tshark.exe 路径
# tshark_path = "F:\\Program Files\\Wireshark\\tshark.exe"


def filter_strings(input_str, target_str):
    words = input_str.split()  # 将字符串按空格分割成单词列表
    for word in words:
        if target_str in word:
            return word


def extract_server_and_code():
    """从包中提取服务器地址和推流码"""
    capture = pyshark.LiveCapture(
        interface=interface,
        display_filter=display_filter,
        tshark_path=tshark_path,
    )
    server, code = None, None
    for packet in capture.sniff_continuously():
        packet = str(packet)

        server_tmp = filter_strings(packet, "rtmp://")
        if server_tmp:
            server = server_tmp

        code_tmp = filter_strings(packet, "stream-")
        if code_tmp:
            code = code_tmp[1:-1]

        if server and code:
            capture.close()
            capture.clear()
            return server, code  # 返回获取到的值


def modify_obs_config(file_path, server, code):
    """修改obs配置文件并启动"""
    # 打开并读取 JSON 文件
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 修改server属性
    if "server" in data["settings"]:
        data["server"] = server
    else:
        print(f"- 键 'server' 不存在于 JSON 数据中")

    # 修改key属性
    if "key" in data["settings"]:
        data["key"] = code
    else:
        print(f"- 键 'key' 不存在于 JSON 数据中")

    # 将修改后的数据保存回文件
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("* 修改obs推流码成功")


def start_obs(path):
    """启动obs"""
    obs_directory = os.path.dirname(path)
    # 检查文件是否存在
    if os.path.exists(path):
        try:
            # 启动指定路径下的进程并设置工作目录
            subprocess.Popen([path], cwd=obs_directory, shell=True)
            print(f"* 成功启动OBS: {path}")
        except Exception as e:
            print(f"* 启动OBS时出错: {e}")
    else:
        print(f"- 文件 {path} 不存在!")


def main():
    server, code = extract_server_and_code()  # 获取提取结果
    print("* 服务器: " + server)
    print("* 推流码: " + code)

    # 修改配置文件并启动
    if obs_config_path is not None and obs_config_path != "":
        modify_obs_config(obs_config_path, server, code)

    if obs_path is not None and obs_path != "":
        start_obs(obs_path)


if __name__ == "__main__":
    main()
