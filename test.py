import os
import yaml

x = {"a": 1, "b": 2, "c": 3}

with open("test.yml", "a+") as f:
    if os.stat("test.yml").st_size == 0:
        yaml.safe_dump(x, f)
    else:
        f.seek(0)
        data = yaml.safe_load(f)
        print(data)
