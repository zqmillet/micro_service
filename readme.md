# 微服务框架

## 简介

该微服务框架是基于 `tornado` 实现的，具有可以实现异步、更好利用多核的优点。但同时，`tornado` 本质上，每一次处理都是交给 `tornado.web.RequestHandler` 来处理，每次定义一个 api 接口都需要继承一个 `tornado.web.RequestHandler` 类，并做定制化，这就导致 `tornado` 的代码不是那么优雅，甚至是有些繁琐。我设计这个微服务框架的初衷就是为了在保留 `tornado` 优点的基础上，使得定制化更加的简洁、优雅、有调理。

## 目录说明

- `config` 文件夹用来存放微服务的配置文件；
- `constants` 文件夹用来存放微服务代码中出现的常量；
- `data` 文件夹用来存放微服务运行时需要的数据；
- `exceptions` 文件夹用来管理微服务中的各种异常；
- `log` 文件夹用来存放日志文件；
- `models` 文件夹用来存放训练好的模型；
- `resources` 文件夹用来存放微服务中各个子服务用到的公共变量；
- `scripts` 文件夹用来存放常用的控制台脚本；
- `services` 文件夹用来管理微服务对外提供的接口；
- `utilities` 文件夹用来存放非业务相关代码；
- `validations` 文件夹用来存放用于验证的代码。

## 配置

微服务的配置文件格式如下所示。

    [
        {
            "name":     "get_nearest_word_list",
            "enable":   true,
            "api_path": "/get_nearest_word_list",
            "function": "### from services.get_nearest_word_list import get_nearest_word_list; get_nearest_word_list",
            "methods":  ["get"]
        },
        {
            "name":     "get_word_vector",
            "enable":   true,
            "api_path": "/get_word_vector",
            "function": "### from services.get_word_vector import get_word_vector; get_word_vector",
            "methods":  ["get", "post"]
        },
        {
            "name":     "auto_complete",
            "enable":   true,
            "api_path": "/auto_complete",
            "function": "### from services.auto_complete import auto_complete; auto_complete",
            "methods":  ["get"]
        },
        {
            "name":     "word_split",
            "enable":   true,
            "api_path": "/word_split",
            "function": "### from services import word_split; word_split",
            "methods":  ["get"]
        },
        {
            "name":     "get_server_time",
            "enable":   true,
            "api_path": "/get_server_time",
            "function": "### from resources.time import time; time.__str__",
            "methods":  ["get"]
        },
        {
            "name":     "update_server_time",
            "enable":   true,
            "api_path": "/update_server_time",
            "function": "### from resources.time import time; time.update",
            "methods":  ["get"],
            "triggers": [{"trigger": "cron", "second": "0, 10, 20, 30, 40, 50"}]
        }
    ]

配置文件是 json 文件，

## 运行

