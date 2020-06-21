#!/usr/bin/env python3
import os
import re

from paramiko import SSHClient
from scp import SCPClient

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
    path = m.group(4)

    print(f"Uploading file with name: {file_name}, to remote host: {ip}:{port} path: {path}/{file_name}")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(ip, port=port)

    scp = SCPClient(ssh.get_transport())
    scp.put(file_name, remote_path=path)
    scp.close()
