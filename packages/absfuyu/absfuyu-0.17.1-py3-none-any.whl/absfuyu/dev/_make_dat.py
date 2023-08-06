""".dat maker - NOT A MODULE"""
import os
import zlib


here = os.path.abspath(os.path.dirname(__file__))
data = r"""

"""
name = "data"


def _make_dat(data: str, name: str = "data", destination: str = ""):
    compressed = zlib.compress(str(data).encode(),zlib.Z_BEST_COMPRESSION)
    with open(f"{destination}\{name}.dat","wb") as file:
        file.write(compressed)
    pass

if __name__ == "__main__":
    _make_dat(data,name,here)