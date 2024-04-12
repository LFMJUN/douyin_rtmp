# douyin_rtmp
抖音直播伴侣一键获取服务器与推流码

### 安装依赖

需要自行安装[Wireshark](https://www.wireshark.org/)

```pip install pyshark```

### 需要修改的地方

```
# 替换 'interface' 为你要抓包的网络接口，如 'eth0'、'wlan0' 等
interface = '以太网'
# 替换 'display_filter' 为你的显示过滤器
display_filter = '((rtmpt) && (_ws.col.info contains "connect")) || (_ws.col.info contains "releaseStream")'
# 替换 'tshark_path' 为你的 tshark.exe 路径
tshark_path = "F:\\Program Files\\Wireshark\\tshark.exe"
```

过滤器一般不需要修改，默认即可，更改interface和tshark_path即可

### 已知问题

目前直接退出程序会报错OSError，初步判定为异步循环问题，不影响使用

### 更新日志

20240412 项目发布

