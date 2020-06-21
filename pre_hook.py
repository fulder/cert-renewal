#!/usr/bin/env python3
import os
import re
import shutil

import utils

file_content = os.getenv("CERTBOT_VALIDATION")
file_name = os.getenv("CERTBOT_TOKEN")
validation_path = os.getenv("VALIDATION_PATH")

with open(file_name, "w") as f:
    f.write(file_content)

# <username>@<IP>:<PORT>:<path>
m = re.match(r"(\w+)@([^:]+):(\d+):(.+)", validation_path)
if m:
    username = m.group(1)
    ip = m.group(2)
    port = int(m.group(3))
    remote_path = m.group(4)

    utils.scp(file_name, username, ip, port, remote_path)
else:
    shutil.copy2(file_name, validation_path)