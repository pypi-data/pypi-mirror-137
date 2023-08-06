"""
ABSFUYU
-------
Configuration
"""



# Library
##############################################################
import json as __json
import os as __os


# Define
##############################################################
__here = __os.path.abspath(__os.path.dirname(__file__))



# Function
##############################################################
def __load_cfg():
    """Load configuration file"""
    with open(f"{__here}/config.json") as json_cfg:
        cfg = __json.load(json_cfg)
    return cfg

def __save_cfg(config):
    """Save config"""
    cfg = __json.dumps(config)
    with open(f"{__here}/config.json","w") as json_cfg:
        json_cfg.writelines(cfg)
    pass

def change_cfg(setting: str, value):
    """Change setting in config"""
    global CONFIG
    cfg = __load_cfg()
    if setting in cfg["setting"]:
        cfg["setting"][setting] = value
        __save_cfg(cfg)
    else:
        raise ValueError
    
    CONFIG = __load_cfg()

def reset_cfg():
    """Reset config to default value"""
    change_cfg("first-run", False)
    change_cfg("luckgod-mode", False)
    pass


def welcome():
    cfg = __load_cfg()
    if cfg["setting"]["first-run"]:
        change_cfg("first-run", False)
        # Do other stuff here


# Config
##############################################################
CONFIG = __load_cfg()