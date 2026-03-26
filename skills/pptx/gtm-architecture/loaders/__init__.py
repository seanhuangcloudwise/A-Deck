"""装载器注册表和工厂"""

# 所有装载器都会在这里导入注册
# 格式: 'gm_XX': load_function

import sys
from pathlib import Path

# 这将在generate.py中被调用
# 例: loaders = load_all_loaders()
# 然后: for i, (name, load_func) in enumerate(loaders.items()):
#           load_func(ctx, data[name])

def register_loader(name, load_fn):
    """注册一个装载器"""
    pass


def get_loader(name):
    """获取指定装载器"""
    pass


def list_all_loaders():
    """列出所有已注册装载器"""
    pass
