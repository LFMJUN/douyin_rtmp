# douyin_rtmp
抖音直播伴侣一键获取服务器与推流码

## 安装依赖

需要自行安装[Wireshark](https://www.wireshark.org/)

```pip install pyshark```

如果不想自行安装python环境的可以去[Releases](https://github.com/LFMJUN/douyin_rtmp/releases)下载已经打包好的main.exe文件和config.json，只需要自行安装[Wireshark](https://www.wireshark.org/)即可

## 需要修改的地方

### config.json

```
{
    "tshark_path": "F:\\\\Program Files\\\\Wireshark\\\\tshark.exe",
    "display_filter": "((rtmpt) && (_ws.col.info contains \"connect\")) || (_ws.col.info contains \"releaseStream\")",
    "interface": "以太网"
}
```

display_filter一般不需要修改，默认即可，更改interface和tshark_path即可

替换 'tshark_path' 为你的 tshark.exe 路径

替换 'interface' 为你要抓包的网络接口，如 'eth0'、'wlan0' 等

config.json文件需要与程序放在同一目录

## 已知问题

目前直接退出程序会报错OSError，初步判定为异步循环问题，不影响使用

需要在打开游戏之前执行抓包操作，否则有可能被识别为作弊程序

## 更新日志

20240412 项目发布

20240412 支持通过json文件修改路径、网卡、筛选器

## Demo

![](https://cdn.jsdelivr.net/gh/lfmjun/ilovekg@main/20240412191646.png)


## Star History

<a href="https://star-history.com/#LFMJUN/douyin_rtmp&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=LFMJUN/douyin_rtmp&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=LFMJUN/douyin_rtmp&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=LFMJUN/douyin_rtmp&type=Date" />
 </picture>
</a>