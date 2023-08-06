""".dat maker - NOT A MODULE"""
import os
import zlib


here = os.path.abspath(os.path.dirname(__file__))

data = r"""
dummy data
"""

if __name__ == "__main__":
    compressed = zlib.compress(str(data).encode(),zlib.Z_BEST_COMPRESSION)
    with open(f"{here}\data.dat","wb") as file:
        file.write(compressed)
    pass