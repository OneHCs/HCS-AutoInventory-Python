import os
import shutil

for root, dirs, files in os.walk("."):
    for dir_name in dirs:
        if dir_name == "__pycache__":
            shutil.rmtree(os.path.join(root, dir_name))