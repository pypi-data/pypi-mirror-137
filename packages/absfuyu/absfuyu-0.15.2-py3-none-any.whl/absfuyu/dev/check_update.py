"""
Check Update Module
-------------------

"""

# import requests as __requests
# __ABSFUYU_RSS = "https://pypi.org/rss/project/absfuyu/releases.xml"
# def loadRSS(url: str):
#     rss = __requests.get(url)
#     return rss.content.decode()

# The try block lets you test a block of code for errors.
# The except block lets you handle the error.
# The else block lets you execute code when there is no error.
# The finally block lets you execute code, regardless of the result of the try- and except blocks.



# Define
##############################################################
DEV_MODE = False



# Library
##############################################################
import subprocess as __subprocess

try:
    import feedparser as __feedparser
except:
    print("This feature is in absfuyu[dev] package")
else:
    DEV_MODE = True

from absfuyu import __version__ as __ver



# Function
##############################################################
__ABSFUYU_RSS = "https://pypi.org/rss/project/absfuyu/releases.xml"

def __get_latest_version():
    """Load data from RSS"""
    if DEV_MODE:
        rss = __feedparser.parse(__ABSFUYU_RSS)
        return rss.entries[0]["title"]

def __get_update(package_name: str = "absfuyu"):
    """Run pip upgrade command"""
    cmd = f"pip install -U {package_name}".split()
    return __subprocess.run(cmd)

def check_for_update(force_update: bool = False):
    """Check for latest update"""
    if DEV_MODE:
        latest = __get_latest_version()
        current = __ver
        if current == latest:
            print("You are using the latest version")
        else:
            if force_update:
                print(f"Newer version ({latest}) available. Upgrading...")
                __get_update()
            else:
                print(f"Newer version ({latest}) available. Upgrade with:\npip install -U absfuyu")

# Run
##############################################################
if __name__ == "__main__":
    check_for_update()