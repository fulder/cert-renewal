import os
import re
import shutil

from paramiko import SSHClient
from scp import SCPClient


def scp(file_path, username, ip, port, remote_path):
    file_name = os.path.basename(file_path)
    print(f"Uploading file with name: {file_path}, to remote host: {ip}:{port} path: {remote_path}/{file_path}")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(ip, port=port, username=username)

    scp = SCPClient(ssh.get_transport())
    scp.put(file_name, remote_path=remote_path)
    scp.close()


def cp_or_scp(file_path, path):
    m = re.match(r"(\w+)@([^:]+):(\d+):(.+)", path)
    if m:
        username = m.group(1)
        ip = m.group(2)
        port = int(m.group(3))
        remote_path = m.group(4)

        scp(file_path, username, ip, port, remote_path)
    else:
        shutil.copy2(file_path, path)