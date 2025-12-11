# -*- coding: utf-8 -*-
import os

class BaseConfig(object):
    """配置基类 - 支持环境变量覆盖"""

    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

    # JWT秘钥（生产环境必须通过环境变量设置）
    SECRET_KEY = os.getenv('SECRET_KEY', 'intramirror')

    # Linux.do OAuth配置
    LINUX_DO_CLIENT_ID = os.getenv('LINUX_DO_CLIENT_ID', '')
    LINUX_DO_CLIENT_SECRET = os.getenv('LINUX_DO_CLIENT_SECRET', '')
    LINUX_DO_REDIRECT_URI = os.getenv('LINUX_DO_REDIRECT_URI', '')

    # ==========================================
    # 数据库配置
    # ==========================================
    # 数据库类型: 'sqlite' 或 'mysql'
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')

    # SQLite配置
    SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', '../data/yprompt.db')

    # MySQL配置（当DB_TYPE='mysql'时使用）
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_NAME = os.getenv('DB_NAME', 'yprompt')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))

    # ==========================================
    # 默认管理员账号配置（仅首次初始化时使用）
    # ==========================================
    DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')
    DEFAULT_ADMIN_NAME = os.getenv('DEFAULT_ADMIN_NAME', '管理员')

    # 是否允许本地注册，默认关闭
    REGISTRATION_ENABLED = os.getenv('REGISTRATION_ENABLED', 'false').lower() == 'true'

    ACCESS_LOG = os.getenv('ACCESS_LOG', 'false').lower() == 'true'

    # 服务worker数量
    WORKERS = int(os.getenv('WORKERS', '1'))

    # 跨域相关
    # 是否启动跨域功能
    ENABLE_CORS = os.getenv('ENABLE_CORS', 'true').lower() == 'true'
    CORS_SUPPORTS_CREDENTIALS = True

    # redis配置
    REDIS_CON = os.getenv('REDIS_CON', 'redis://127.0.0.1:6379/2')

    # 日志配置，兼容sanic内置log库
    LOGGING_INFO_FILE = '../data/logs/backend/info.log'
    LOGGING_ERROR_FILE = '../data/logs/backend/error.log'
    BASE_LOGGING = {
        'version': 1,
        'loggers': {
            "sanic.root": {"level": "INFO", "handlers": ["console", 'info_file', 'error_file']},
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s | %(levelname)s | %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
            },
            'info_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_INFO_FILE,
                'maxBytes': (1 * 1024 * 1024),
                'backupCount': 10,
                'encoding': 'utf8',
                'level': 'INFO',
                'formatter': 'default',
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_ERROR_FILE,
                'maxBytes': (1 * 1024 * 1024),
                'backupCount': 10,
                'encoding': 'utf8',
                'level': 'ERROR',
                'formatter': 'default',
            },
        },
    }

    # 告警源和派生表映射关系
    S2T = {
        "apm": "apm",
        "rum": "rum",
        "ckafka": "mid",
        "mongodb": "mid",
        "redis": "mid",
        "cdb": "mid",
        "es": "mid",
        "cvm": "iaas",
        "ecs": "iaas",
        "cos": "iaas",
        "cls": "iaas",
        "sls": "iaas",
        "custom": "custom"
    }

    # 没有对应的分派策略的默认owner
    OWNER_DEFAULT = [{
        'workforceType': 4,
        'watchkeeperId': 833,
        'watchkeeperName': '朱威',
        'dingDingId': 4311207311543872874
    }]
    ARGS_DEFAULT = {
    'status': 0,
    'dingtalk_person': 0,
    'sms': 0,
    'dingtalk_group': 0
    }


    def __init__(self):
        if self.LOGGING_INFO_FILE:
            self.BASE_LOGGING['handlers']['info_file']['filename'] = self.LOGGING_INFO_FILE

        if self.LOGGING_ERROR_FILE:
            self.BASE_LOGGING['handlers']['error_file']['filename'] = self.LOGGING_ERROR_FILE
