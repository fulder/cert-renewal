#!/usr/bin/env python3
import os

file_name = os.getenv("CERTBOT_TOKEN")


os.remove(file_name)
