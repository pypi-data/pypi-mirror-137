"""
absfuyu's current version
-------------------------
"""

# Module level
##############################################################
__all__ = [
    "__version__",
    "check_for_update",
]



# Library
##############################################################
import json as __json
import subprocess as __subprocess
from typing import Optional as __Optional
from urllib.error import URLError as __URLError
from urllib.request import Request as __Request
from urllib.request import urlopen as __urlopen

from . import config as __config


# Function
##############################################################
#__ABSFUYU_RSS = "https://pypi.org/rss/project/absfuyu/releases.xml"

def __get_latest_version_legacy(package_name: str = "absfuyu"):
    """
    Load data from PyPI's RSS -- OLD
    """
    rss = f"https://pypi.org/rss/project/{package_name}/releases.xml"
    req = __Request(rss)
    try:
        response = __urlopen(req)
    except __URLError as e:
        if hasattr(e, "reason"):
            print("Failed to reach server.")
            print("Reason: ", e.reason)
        elif hasattr(e, "code"):
            print("The server couldn\'t fulfill the request.")
            print("Error code: ", e.code)
    else:
        xml_file = response.read().decode()
        ver = xml_file[xml_file.find("<item>"):xml_file.find("</item>")]
        version = ver[ver.find("<title>")+len("<title>"):ver.find("</title>")]
        return version

def __load_data_from_json_api(api: str):
    """
    Load data from api then convert to json
    """
    req = __Request(api)
    try:
        response = __urlopen(req)
    except __URLError as e:
        if hasattr(e, "reason"):
            print("Failed to reach server.")
            print("Reason: ", e.reason)
        elif hasattr(e, "code"):
            print("The server couldn\'t fulfill the request.")
            print("Error code: ", e.code)
    else:
        json_file = response.read().decode()
        return __json.loads(json_file)

def __get_latest_version(package_name: str = "absfuyu"):
    """
    Get latest version from PyPI's API
    """
    api = f"https://pypi.org/pypi/{package_name}/json"
    ver = __load_data_from_json_api(api)
    return ver["info"]["version"]

def __get_update(
        package_name: str = "absfuyu",
        version: __Optional[str] = None
    ):
    """
    Run pip upgrade command
    """
    # python -m pip install -U {package_name}
    if version is None:
        cmd = f"pip install -U {package_name}".split()
    else:
        cmd = f"pip install -U {package_name}=={version}".split()
    # return __subprocess.run(cmd)
    try:
        return __subprocess.run(cmd)
    except:
        cmd = f"python -m pip install -U {package_name}=={version}"
        return __subprocess.run(cmd)

def check_for_update(
        package_name: str = "absfuyu",
        force_update: bool = False,
    ):
    """
    Check for latest update
    """
    latest = __get_latest_version(package_name)
    current = __version__
    if current == latest:
        print(f"You are using the latest version ({latest})")
    else:
        if force_update:
            print(f"Newer version ({latest}) available. Upgrading...")
            try:
                __get_update(package_name, version=latest)
            except:
                print(f"""
                Unable to perform update.
                Please update manually with:
                pip install -U {package_name}=={latest}
                """)
        else:
            print(f"Newer version ({latest}) available. Upgrade with:\npip install -U {package_name}=={latest}")

#######

def __get_ver_from_config(string_mode: bool = False):
    """get current version"""
    cfg = __config.__load_cfg()
    ver = cfg["version"]
    if string_mode:
        return ".".join([str(x) for x in ver.values()])
    else:
        return ver

def __bump_version(option: str = "patch"):
    """bump version"""
    global __version__
    bump_option = ["major", "minor", "patch"]

    if option not in bump_option:
        return None
    
    cfg = __config.__load_cfg()
    if option.startswith("major"):
        cfg["version"][option] += 1
        cfg["version"]["minor"] = 0
        cfg["version"]["patch"] = 0
    elif option.startswith("minor"):
        cfg["version"][option] += 1
        cfg["version"]["patch"] = 0
    else:
        cfg["version"][option] += 1
    __config.__save_cfg(cfg)

    __version__ = __get_ver_from_config(string_mode=True)


def __release_to_pypi(
        option:str = "patch",
        safety_lock_off: bool = False,
        debug: bool = False,
    ):
    """
    Not intended for end-user
    
    Developer only!
    """

    bump_option = ["major", "minor", "patch"]

    if option not in bump_option:
        return None

    if safety_lock_off:

        if debug:
            print("Bumping version...")
        
        __bump_version(option=option)

        if debug:
            print(f"Version bumped. Current verion: {__version__}")
            print("Initialize building package")
        
        cmd1 = "python -m build".split()
        cmd2 = "twine upload dist/*".split()
        try:
            __subprocess.run(cmd1)
            try:
                __subprocess.run(cmd2)
                print("Release published!")
            except:
                return None
        except:
            return None
        else:
            return None
    else:
        return None



##############################################################
__version__ = __get_ver_from_config(string_mode=True)