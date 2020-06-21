#!/usr/bin/env python3
import os
import utils

file_content = os.getenv("CERTBOT_VALIDATION")
file_name = os.getenv("CERTBOT_TOKEN")
validation_path = os.getenv("VALIDATION_PATH")

with open(file_name, "w") as f:
    f.write(file_content)

utils.cp_or_scp(file_name, validation_path)
