#!/usr/bin/env python3
import os
import utils

file_name = os.getenv("CERTBOT_TOKEN")
pfx_locations = os.getenv("PFX_LOCATIONS")
certbot_folder = os.getenv("CERTBOT_FOLDER")

os.remove(file_name)

pfx_location = os.path.join(certbot_folder, "config", "live", "certificate.pfx")

if pfx_locations is not None:
    copy_locations = pfx_locations.split(",")
    for copy_location in copy_locations:
        utils.cp_or_scp(pfx_location, copy_location)
