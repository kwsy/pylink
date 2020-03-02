"""
请在脚本里配置redis参数
"""

# Config_Redis = {"host":"101.201.225.172",
#                 "port":6379,
#                 "password":"zmh121100",
#                 "db":1,
# }

DICT_CONNECT_REDIS = {"host": "127.0.0.1",
                      "port":  6379,
                      "password": "zmh121100",
                      "db": 1,
}

NAME_QUEUE_REDIS = "zmh_url_queue"                # redis中定义的消息队列名称