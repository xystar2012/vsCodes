import os
import sys

path = sys.path[0]
for name in os.listdir(path):
    source = os.path.join(path, name)
    print(source)